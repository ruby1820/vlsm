import streamlit as st

st.set_page_config(page_title="VLSM Calculator App", page_icon="📘", layout="wide")

st.markdown("""
    <style>
    .hero-card {
        background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 100%);
        color: white;
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.2);
        margin-bottom: 2rem;
    }
    .hero-card h1 {
        margin: 0;
        font-size: 3rem;
    }
    .hero-card p {
        margin: 0.8rem 0 0 0;
        opacity: 0.95;
        line-height: 1.7;
        max-width: 820px;
    }
    .feature-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.4rem;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .feature-card h3 {
        margin-top: 0;
        color: #111827;
    }
    .feature-card p {
        color: #4b5563;
    }
    .pill {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #1d4ed8;
        border-radius: 999px;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.3rem;
        color: #1d4ed8;
    }
    .metric-card p {
        margin: 0.5rem 0 0 0;
        color: #6b7280;
    }
    .button-primary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #1d4ed8;
        color: white;
        padding: 0.85rem 1.5rem;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 700;
        margin-right: 0.75rem;
        margin-bottom: 0.75rem;
    }
    .button-secondary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #1d4ed8;
        border: 2px solid #1d4ed8;
        padding: 0.85rem 1.5rem;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .button-group {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: center;
    }
    .contact-card {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #1e40af;
        color: white;
    }
    .contact-card h3 {
        margin-top: 0;
        color: #f8fafc;
    }
    .contact-card p {
        color: #e0f2fe;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <h1>About the VLSM Calculator App</h1>
    <p>This application helps network engineers and students calculate Variable Length Subnet Masking (VLSM) quickly and accurately.
    It provides clear subnet allocation, history tracking, report exports, and a responsive interface for modern IP planning.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Application Overview")
    st.markdown("""
    **Version:** 1.0.0  
    **Developer:** Mohamed Ruby  
    **Project Description:** A lightweight IP subnet calculator designed to simplify VLSM planning.
    It calculates subnet ranges, suggests CIDR prefixes, exports results, and stores history for later review.
    """)
    st.markdown("### Features")
    st.markdown("""
    - Fast VLSM calculation using Python networking logic  
    - Export reports as CSV, Excel, and PDF  
    - Save calculation history locally  
    - Responsive and clean UI for desktop and mobile  
    """)
    st.markdown("### Technologies Used")
    st.markdown("""
    <span class='pill'>Python</span>
    <span class='pill'>Streamlit</span>
    <span class='pill'>ipaddress</span>
    <span class='pill'>Pandas</span>
    <span class='pill'>FPDF</span>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>Quick Facts</h3>
        <p>Learn the main app capabilities and how it supports subnet design, reporting, and data saving.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='metric-card'>
        <h2>Fast</h2>
        <p>Rapid VLSM calculation and subnet sorting.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='metric-card'>
        <h2>Reliable</h2>
        <p>Accurate IP planning with history and export support.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### GitHub & Contact")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class='contact-card'>
        <h3>Contact</h3>
        <p>If you have questions, feedback, or suggestions, feel free to reach out.</p>
        <p><strong>Email:</strong> alroby5200@gmail.com</p>
        <p><strong>Phone:</strong> +201064764317</p>
        <p><strong>Feedback:</strong> Use the form to send your comments directly.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='button-group'>
        <a href='https://github.com/ruby1820' target='_blank' class='button-primary'>GitHub</a>
        <a href='mailto:alroby5200@gmail.com' class='button-secondary'>Contact</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Feedback Form")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email Address")
    feedback = st.text_area("Feedback / Suggestions")
    submitted = st.form_submit_button("Submit Feedback")
    if submitted:
        st.success("Thank you! Your feedback has been submitted.")
        st.info("We will review your message and respond soon.")
