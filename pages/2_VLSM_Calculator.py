import streamlit as st
import pandas as pd
import json
import os
import ipaddress
from io import BytesIO
from datetime import datetime
from core.vlsm_engine import calculate_vlsm

# Page configuration
st.set_page_config(
    page_title="VLSM Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# History file path
HISTORY_FILE = "data/history.json"

# Utility functions

def init_history_file():
    if not os.path.exists(HISTORY_FILE):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_history():
    init_history_file()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def add_to_history(base_network, results):
    history = load_history()
    sanitized_subnets = []
    for item in results:
        sanitized_subnets.append({
            "Network ID": item.get("Network", ""),
            "Network Address": str(item.get("Network Address", "")),
            "Subnet Mask": str(item.get("Subnet Mask", "")),
            "CIDR": item.get("CIDR", ""),
            "First Host": str(item.get("First Host", "")),
            "Last Host": str(item.get("Last Host", "")),
            "Broadcast": str(item.get("Broadcast Address", "")),
            "Number of Hosts": int(item.get("Total Usable", 0))
        })
    history.append({
        "base_network": base_network,
        "timestamp": datetime.now().isoformat(),
        "subnets": sanitized_subnets
    })
    save_history(history)


def suggest_prefix(hosts):
    if hosts <= 0:
        return "N/A"
    required_bits = 0
    while (2 ** required_bits - 2) < hosts:
        required_bits += 1
    prefix = 32 - required_bits
    return f"/{prefix}"


def create_copy_button(copy_text, key):
    safe_text = json.dumps(copy_text, ensure_ascii=False)
    return f"""
        <div style='margin-top: 0.5rem;'>
            <button onclick='navigator.clipboard.writeText({safe_text})' style='background:#4caf50; color:white; border:none; padding:0.55rem 0.85rem; border-radius:8px; cursor:pointer;'>Copy Result</button>
        </div>
    """


def create_pdf_bytes(df, base_network):
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "VLSM Calculation Results", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Base Network: {base_network}", ln=True)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    for col in df.columns:
        pdf.cell(30, 8, str(col), border=1)
    pdf.ln()
    pdf.set_font("Arial", "", 11)
    for _, row in df.iterrows():
        for col in df.columns:
            pdf.cell(30, 8, str(row[col]), border=1)
        pdf.ln()
    return pdf.output(dest="S").encode("latin-1")


def build_results(df_results):
    df_results = df_results.copy()
    if "CIDR" not in df_results.columns and "Subnet Mask" in df_results.columns and "Network Address" in df_results.columns:
        df_results["CIDR"] = df_results.apply(lambda row: f"/{ipaddress.ip_network(f'{row['Network Address']}/{row['Subnet Mask']}', strict=False).prefixlen}", axis=1)
    df_results = df_results.rename(columns={
        "Network": "Network ID",
        "Total Usable": "Number of Hosts",
        "Broadcast Address": "Broadcast",
        "Network Address": "Network Address",
        "First Host": "First Host",
        "Last Host": "Last Host",
        "Subnet Mask": "Subnet Mask"
    })
    columns = ["Network ID", "Network Address", "First Host", "Last Host", "Broadcast", "Subnet Mask", "CIDR", "Number of Hosts"]
    return df_results[[col for col in columns if col in df_results.columns]]


def render_chart(subnets):
    chart_df = pd.DataFrame({
        "Network": [item["Network ID"] for item in subnets],
        "Hosts": [int(item["Number of Hosts"]) for item in subnets]
    })
    chart_df = chart_df.set_index("Network")
    st.bar_chart(chart_df)


# Theme toggle
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)

if dark_mode:
    page_bg = "#0f172a"
    card_bg = "#111827"
    text_color = "#f8fafc"
    border_color = "#2563eb"
    accent_bg = "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)"
else:
    page_bg = "#f8fafc"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    border_color = "#6366f1"
    accent_bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

st.markdown(f"""
    <style>
    .page-style {{ background: {page_bg}; color: {text_color}; }}
    .top-card {{ background: {accent_bg}; color: white; border-radius: 18px; padding: 2rem; box-shadow: 0 18px 36px rgba(15, 23, 42, 0.15); margin-bottom: 1.5rem; }}
    .top-card h1 {{ margin: 0; font-size: 2.9rem; }}
    .top-card p {{ margin: 0.75rem 0 0 0; opacity: 0.9; }}
    .quick-button {{ background: rgba(255,255,255,0.15); color: white; border: 1px solid rgba(255,255,255,0.2); padding: 0.9rem 1.1rem; border-radius: 12px; margin-right: 0.5rem; text-decoration: none; display: inline-block; }}
    .card {{ background: {card_bg}; color: {text_color}; border-radius: 16px; padding: 1.5rem; border: 1px solid {border_color}; box-shadow: 0 12px 24px rgba(0,0,0,0.08); }}
    .card h3 {{ margin-top: 0; }}
    .metric-card {{ background: {card_bg}; color: {text_color}; border-radius: 16px; padding: 1.2rem; border: 1px solid {border_color}; }}
    .metric-card h2 {{ margin: 0; font-size: 2rem; }}
    .metric-card p {{ margin: 0.5rem 0 0 0; opacity: 0.8; }}
    .diagram-card {{ background: {card_bg}; padding: 1.5rem; border-radius: 16px; border: 1px solid {border_color}; }}
    .diagram-box {{ width: 100%; height: 260px; border-radius: 16px; background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.12) 100%); display: flex; align-items: center; justify-content: center; color: {text_color}; }}
    .diagram-box ul {{ list-style: none; padding: 0; margin: 0; width: 100%; }}
    .diagram-box li {{ margin: 0.75rem 0; display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.08); }}
    .diagram-box strong {{ font-size: 0.95rem; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-style'>", unsafe_allow_html=True)

# Header section
st.markdown(f"""
    <div class='top-card'>
        <h1>🧮 VLSM Calculator</h1>
        <p>Smart subnet planning with auto suggestions, quick export, and visual subnet mapping.</p>
        <div style='margin-top: 1.5rem;'>
            <span class='quick-button'>Start Calculating</span>
            <span class='quick-button'>View History</span>
            <span class='quick-button'>Learn VLSM</span>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Welcome to the most intuitive VLSM tool")
    st.markdown("This page helps you split your network into efficient subnets and prepares the calculation details you need for fast deployment.")
    st.markdown("### Why use this app?")
    st.markdown("- Automatic subnet sorting from largest to smallest.\n- Quick prefix suggestions for host counts.\n- Export results as PDF, CSV, or Excel.\n- Visual subnet diagram to understand allocation.")

with col2:
    st.markdown("""
    <div class='card'>
        <h3>Network & Server</h3>
        <p>Use the fast IP planner to build scalable subnets for your systems and servers.</p>
        <div style='display:flex; gap:0.8rem; margin-top:1rem;'>
            <span style='font-size:2rem;'>🖧</span>
            <span style='font-size:2rem;'>🖥️</span>
            <span style='font-size:2rem;'>☁️</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Input panel
st.markdown("### Input Data")
inputs_col1, inputs_col2 = st.columns(2)

with inputs_col1:
    network_ip = st.text_input("Network IP", "192.168.1.0")
    cidr = st.slider("Subnet Mask / CIDR", 0, 32, 24)
    num_subnets = st.number_input("Number of Required Subnets", min_value=1, max_value=20, value=3, step=1)

with inputs_col2:
    st.markdown("#### Host requirements")
    host_requirements = []
    for i in range(int(num_subnets)):
        hosts = st.number_input(
            f"Hosts for subnet {i+1}",
            min_value=1,
            max_value=65000,
            value=2 ** (8 - i) if i < 4 else 10,
            step=1,
            key=f"vlsm_host_{i}"
        )
        suggestion = suggest_prefix(hosts)
        st.caption(f"Suggested prefix for {hosts} hosts: {suggestion}")
        host_requirements.append(hosts)

st.markdown("---")

result = None
error_message = None

def build_base_network(ip, prefix):
    return f"{ip}/{prefix}"

base_network = build_base_network(network_ip, cidr)

calculate_btn = st.button("🚀 Start Calculating")

if calculate_btn:
    try:
        result = calculate_vlsm(base_network, host_requirements)
    except Exception as exc:
        error_message = str(exc)

if error_message:
    st.error(f"Calculation failed: {error_message}")

if result:
    # Add CIDR field and format results
    for item in result:
        prefix = ipaddress.ip_network(f"{item['Network Address']}/{item['Subnet Mask']}", strict=False).prefixlen
        item["CIDR"] = f"/{prefix}"

    df = pd.DataFrame(result)
    df = df.rename(columns={
        "Network": "Network ID",
        "Total Usable": "Number of Hosts",
        "Broadcast Address": "Broadcast",
        "Network Address": "Network Address"
    })
    df = df[["Network ID", "First Host", "Last Host", "Broadcast", "Subnet Mask", "CIDR", "Number of Hosts"]]

    st.markdown("### Results")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    with stats_col1:
        st.metric("Saved Operations", len(load_history()))
    with stats_col2:
        st.metric("Last Calculation", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with stats_col3:
        st.metric("Calculated Subnets", len(result))
    with stats_col4:
        total_hosts = df["Number of Hosts"].sum()
        st.metric("Total Hosts", int(total_hosts))

    st.markdown("---")
    st.markdown("### Visual Subnet Diagram")
    diagram_subnets = [
        {"Network ID": item["Network"], "Hosts": int(item.get("Total Usable", 0))}
        for item in result
    ]
    chart_df = pd.DataFrame(diagram_subnets).set_index("Network ID")
    st.bar_chart(chart_df)

    st.markdown("---")
    st.markdown("### Export Options")

    export_col1, export_col2, export_col3 = st.columns(3)

    with export_col1:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"vlsm_{network_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with export_col2:
        buffer = BytesIO()
        try:
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="VLSM")
            buffer.seek(0)
            st.download_button(
                label="Download Excel",
                data=buffer.read(),
                file_name=f"vlsm_{network_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception:
            st.warning("Excel export requires openpyxl or xlsxwriter package.")

    with export_col3:
        pdf_data = create_pdf_bytes(df, base_network)
        if pdf_data:
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name=f"vlsm_{network_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("PDF export available when the 'fpdf' package is installed.")

    st.markdown("---")
    st.markdown("### Copy Individual Subnet Results")
    for idx, row in df.iterrows():
        cols = st.columns([4, 1])
        with cols[0]:
            st.write(f"**{row['Network ID']}** → {row['Subnet Mask']} {row['CIDR']} | Hosts: {row['Number of Hosts']}")
        with cols[1]:
            row_text = json.dumps(row.to_dict(), ensure_ascii=False, default=str)
            st.markdown(create_copy_button(row_text, f"copy_{idx}"), unsafe_allow_html=True)

    add_to_history(base_network, result)

# Help section
st.markdown("---")
st.markdown("### How to use this page")
st.markdown(
    "1. Enter the base network IP and choose a CIDR mask.\n"
    "2. Set how many subnets you need and the host count for each.\n"
    "3. Press Start Calculating to see sorted subnet allocation.\n"
    "4. Export or copy the subnet results at once."
)

st.markdown("</div>", unsafe_allow_html=True)
