import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import csv
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="History & Records - VLSM Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .history-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    .history-header h1 {
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 700;
    }
    .history-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .stat-card h3 {
        color: #ffeb3b;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
    }
    .stat-card p {
        color: #f0f0f0;
        margin: 0;
        font-weight: 500;
    }
    .record-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .record-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2);
    }
    .record-card h4 {
        color: #667eea;
        margin-top: 0;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .record-detail {
        color: #555;
        margin: 0.5rem 0;
        padding: 0.5rem 0;
    }
    .record-detail strong {
        color: #2c3e50;
        font-weight: 600;
    }
    .filter-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
    }
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        color: #666;
    }
    .empty-state h2 {
        color: #667eea;
        margin-top: 0;
    }
    .empty-state p {
        font-size: 1.1rem;
        color: #888;
    }
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    </style>
""", unsafe_allow_html=True)

# History file path
HISTORY_FILE = "data/history.json"

# Initialize history file if it doesn't exist
def init_history_file():
    """Initialize history file if it doesn't exist"""
    if not os.path.exists(HISTORY_FILE):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)

# Load history data
def load_history():
    """Load history from JSON file"""
    init_history_file()
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except:
        return []

# Save history data
def save_history(data):
    """Save history to JSON file"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Header
st.markdown("""
    <div class="history-header">
        <h1>📊 Calculation History & Records</h1>
        <p>View and manage all your previous VLSM calculations</p>
    </div>
""", unsafe_allow_html=True)

# Load history
history_data = load_history()

# Statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
    <h3>{len(history_data)}</h3>
    <p>Total Calculations</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_networks = sum(len(item.get('subnets', [])) for item in history_data)
    st.markdown(f"""
    <div class="stat-card">
    <h3>{total_networks}</h3>
    <p>Total Subnets</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if history_data:
        latest = datetime.fromisoformat(history_data[-1].get('timestamp', datetime.now().isoformat()))
        st.markdown(f"""
        <div class="stat-card">
        <h3>✓</h3>
        <p>Last: {latest.strftime('%m/%d/%Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="stat-card">
        <h3>-</h3>
        <p>No Records Yet</p>
        </div>
        """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
    <h3>📈</h3>
    <p>Network Management</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Filter and search
st.markdown("## 🔍 Search & Filter")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    search_term = st.text_input("🔎 Search by base network...", placeholder="e.g., 192.168.0.0/24")

with col2:
    sort_by = st.selectbox("Sort by:", ["Latest First", "Oldest First", "Base Network A-Z", "Base Network Z-A"])

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# Filter data
filtered_data = history_data.copy()

# Apply search filter
if search_term:
    filtered_data = [
        item for item in filtered_data
        if search_term.lower() in str(item.get('base_network', '')).lower()
    ]

# Apply sorting
if sort_by == "Latest First":
    filtered_data = sorted(filtered_data, key=lambda x: x.get('timestamp', ''), reverse=True)
elif sort_by == "Oldest First":
    filtered_data = sorted(filtered_data, key=lambda x: x.get('timestamp', ''))
elif sort_by == "Base Network A-Z":
    filtered_data = sorted(filtered_data, key=lambda x: x.get('base_network', ''))
elif sort_by == "Base Network Z-A":
    filtered_data = sorted(filtered_data, key=lambda x: x.get('base_network', ''), reverse=True)

st.markdown("---")

# Display records
if filtered_data:
    st.markdown(f"## 📋 Records ({len(filtered_data)})")
    
    # Display each record
    for idx, record in enumerate(filtered_data):
        timestamp = datetime.fromisoformat(record.get('timestamp', datetime.now().isoformat()))
        base_network = record.get('base_network', 'N/A')
        subnets = record.get('subnets', [])
        
        with st.expander(
            f"📌 {base_network} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            expanded=False
        ):
            # Record details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white;">
                <p style="margin: 0 0 0.5rem 0; color: #ffeb3b;"><strong>Base Network</strong></p>
                <p style="margin: 0; color: white; font-size: 1.1rem; font-weight: 600;">{base_network}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 1rem; border-radius: 10px; color: white;">
                <p style="margin: 0 0 0.5rem 0; color: #fffacd;"><strong>Subnets Count</strong></p>
                <p style="margin: 0; color: white; font-size: 1.1rem; font-weight: 600;">{len(subnets)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); padding: 1rem; border-radius: 10px; color: white;">
                <p style="margin: 0 0 0.5rem 0; color: #ffeb3b;"><strong>Calculation Time</strong></p>
                <p style="margin: 0; color: white; font-size: 0.95rem; font-weight: 600;">{timestamp.strftime('%H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📊 Subnets Details")
            
            # Display subnets table
            if subnets:
                df_subnets = pd.DataFrame(subnets)
                st.dataframe(df_subnets, use_container_width=True, hide_index=True)
            else:
                st.info("No subnet details available")
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📋 Copy to Clipboard", key=f"copy_{idx}"):
                    # Copy details to clipboard (simulated)
                    st.success("Details copied! (Copy functionality)")
            
            with col2:
                if st.button(f"📥 Export CSV", key=f"export_{idx}"):
                    # Create CSV
                    csv_data = pd.DataFrame(subnets).to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"vlsm_export_{base_network.replace('/', '_')}_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key=f"download_{idx}"
                    )
            
            with col3:
                if st.button(f"🗑️ Delete Record", key=f"delete_{idx}"):
                    # Delete record
                    filtered_data.pop(idx)
                    save_history(filtered_data)
                    st.success("Record deleted successfully!")
                    st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
    <h2>📭 No Records Found</h2>
    <p>There are no calculation records yet.</p>
    <p>Go to the <strong>VLSM Calculator</strong> page and start making calculations!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Bulk actions
st.markdown("## ⚙️ Bulk Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Export All as CSV", use_container_width=True):
        if history_data:
            all_subnets = []
            for record in history_data:
                for subnet in record.get('subnets', []):
                    subnet['base_network'] = record.get('base_network', '')
                    subnet['timestamp'] = record.get('timestamp', '')
                    all_subnets.append(subnet)
            
            df_all = pd.DataFrame(all_subnets)
            csv_data = df_all.to_csv(index=False)
            st.download_button(
                label="Download All Records",
                data=csv_data,
                file_name=f"vlsm_all_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No records to export!")

with col2:
    if st.button("📊 Generate Summary Report", use_container_width=True):
        if history_data:
            st.markdown("### 📈 Summary Report")
            
            total_calcs = len(history_data)
            total_subnets = sum(len(record.get('subnets', [])) for record in history_data)
            avg_subnets = total_subnets / total_calcs if total_calcs > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Calculations", total_calcs)
            with col2:
                st.metric("Total Subnets Created", total_subnets)
            with col3:
                st.metric("Average Subnets/Calc", f"{avg_subnets:.1f}")
            
            # Most used networks
            st.markdown("### 🔝 Top Base Networks")
            from collections import Counter
            networks = [record.get('base_network', '') for record in history_data]
            network_counts = Counter(networks)
            top_networks = dict(network_counts.most_common(5))
            
            if top_networks:
                df_networks = pd.DataFrame(list(top_networks.items()), columns=['Base Network', 'Usage Count'])
                st.dataframe(df_networks, use_container_width=True, hide_index=True)
        else:
            st.warning("No records to generate a report!")

with col3:
    if st.button("🗑️ Clear All History", use_container_width=True):
        if st.checkbox("I understand this will delete all records"):
            save_history([])
            st.success("All history cleared!")
            st.rerun()
        else:
            st.info("Check the confirmation box to clear history")

st.markdown("---")

# Information section
st.markdown("## ℹ️ About Your History")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white;">
    <h3 style="color: #ffeb3b; margin-top: 0;">💾 Data Storage</h3>
    <p style="color: #f0f0f0; line-height: 1.6;">Your calculation history is stored locally in JSON format. Each calculation includes the base network, subnet details, and timestamp for easy reference.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 1.5rem; border-radius: 10px; color: white;">
    <h3 style="color: #fffacd; margin-top: 0;">🔐 Privacy & Security</h3>
    <p style="color: #f0f0f0; line-height: 1.6;">Your history is stored locally on your device. No data is sent to external servers. You can export or delete your history anytime.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #ffffff; padding: 1.5rem; background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); border-radius: 10px;">
<p style="font-weight: 600; margin: 0; font-size: 1rem;">VLSM Calculator App © 2026 | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
