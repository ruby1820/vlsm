import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Home - VLSM Calculator",
    page_icon="🏠",
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
    .welcome-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    .welcome-header h1 {
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 700;
        letter-spacing: 1px;
    }
    .welcome-header p {
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 300;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #4c51bf;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        color: white;
    }
    .feature-box h3 {
        color: #ffffff;
        margin-top: 0;
        font-weight: 600;
    }
    .feature-box p {
        color: #f0f0f0;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .info-box {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #0077aa;
        box-shadow: 0 4px 12px rgba(0, 153, 204, 0.3);
        color: white;
    }
    .info-box p {
        color: #ffffff;
        margin: 0.5rem 0;
        line-height: 1.7;
    }
    .info-box strong {
        color: #fffacd;
        font-weight: 700;
    }
    .info-box ul {
        list-style: none;
        padding-left: 0;
    }
    .info-box li {
        color: #ffffff;
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    .step-box {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1565c0;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
        color: white;
    }
    .step-box h3 {
        color: #ffeb3b;
        margin-top: 0;
        font-weight: 600;
        font-size: 1.3rem;
    }
    .step-box p {
        color: #ffffff;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .step-box strong {
        color: #ffeb3b;
        font-weight: 700;
    }
    .benefit-card {
        background: linear-gradient(135deg, #4c51bf 0%, #667eea 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        margin: 0.5rem;
        border: 2px solid #5a67d8;
        color: white;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .benefit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);
    }
    .benefit-card h4 {
        color: #ffeb3b;
        margin-top: 0;
        font-weight: 600;
    }
    .benefit-card p {
        color: #f0f0f0;
        margin: 0;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        font-weight: 700;
    }
    h3 {
        color: #34495e;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("""
    <div class="welcome-header">
        <h1>🎉 Welcome to VLSM Calculator</h1>
        <p>Your Complete Solution for Variable Length Subnet Masking Calculations</p>
    </div>
""", unsafe_allow_html=True)

# العمودين الرئيسيان
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📖 What is VLSM Calculator?")
    st.markdown("""
    <div class="info-box">
    <p>
    <strong>VLSM</strong> (Variable Length Subnet Masking) is a modern networking technique that divides
    networks more efficiently than traditional Classful Subnetting.
    </p>
    <p>
    This application helps you:
    <ul>
    <li>✅ Divide large networks into smaller subnets</li>
    <li>✅ Calculate IP address ranges automatically</li>
    <li>✅ Conserve resources and use them efficiently</li>
    <li>✅ Manage IP addresses in an advanced way</li>
    </ul>
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("## 🎯 Key Benefits")
    
    benefits = [
        ("🔢", "Accurate Calculation", "Reliable and verified results"),
        ("⚡", "Fast & Efficient", "Calculate in seconds"),
        ("📊", "Easy Interface", "User-friendly for everyone"),
        ("💾", "Save History", "Keep your previous calculations"),
    ]
    
    for icon, title, desc in benefits:
        st.markdown(f"""
        <div class="benefit-card">
        <h4>{icon} {title}</h4>
        <p style="margin:0; color:#666;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Divider
st.markdown("---")

# How to use
st.markdown("## 📚 How to Use the Application")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-box">
    <h3>Step 1️⃣</h3>
    <p><strong>Enter Base Network</strong></p>
    <p>Enter the base network address with its subnet mask
    <br>(Example: 192.168.1.0/24)</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-box">
    <h3>Step 2️⃣</h3>
    <p><strong>Specify Number of Subnets</strong></p>
    <p>Define how many subnets you want to
    <br>divide the base network into</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-box">
    <h3>Step 3️⃣</h3>
    <p><strong>Enter Number of Hosts</strong></p>
    <p>Specify the number of hosts required in each
    <br>subnet</p>
    </div>
    """, unsafe_allow_html=True)

# Additional features
st.markdown("## ⭐ Application Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
    <h3>🧮 Advanced VLSM Calculations</h3>
    <p>Calculate different IP network divisions based on your needs,
    with support for all network classes (Class A, B, C)</p>
    </div>
    
    <div class="feature-box">
    <h3>📋 Clear Result Tables</h3>
    <p>Display all results in organized and easy-to-understand tables
    with all important information included</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
    <h3>💾 Save History & Records</h3>
    <p>Save all your previous calculations and access them
    anytime from the history page</p>
    </div>
    
    <div class="feature-box">
    <h3>📤 Export Results</h3>
    <p>Save your results in different file formats
    (CSV, Excel, and more)</p>
    </div>
    """, unsafe_allow_html=True)

# Divider
st.markdown("---")

# Additional information
st.markdown("## 💡 Important Tips")

tip_col1, tip_col2 = st.columns(2)

with tip_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #4c51bf; color: white; margin-bottom: 1rem;">
    <p style="color: #ffeb3b; font-weight: 700; margin: 0 0 0.5rem 0;">💼 Tip 1:</p>
    <p style="color: #f0f0f0; margin: 0; line-height: 1.6;">When entering the base network, make sure to use the correct format (Example: 10.0.0.0/8 or 172.16.0.0/12)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #0077aa; color: white;">
    <p style="color: #fffacd; font-weight: 700; margin: 0 0 0.5rem 0;">📐 Tip 2:</p>
    <p style="color: #f0f0f0; margin: 0; line-height: 1.6;">Sorting subnets by number of hosts in descending order helps you get the best results</p>
    </div>
    """, unsafe_allow_html=True)

with tip_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #c62828; color: white; margin-bottom: 1rem;">
    <p style="color: #ffeb3b; font-weight: 700; margin: 0 0 0.5rem 0;">⚠️ Warning:</p>
    <p style="color: #f0f0f0; margin: 0; line-height: 1.6;">Make sure the total number of required hosts does not exceed the number of available addresses in the base network</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2e7d32; color: white;">
    <p style="color: #fffacd; font-weight: 700; margin: 0 0 0.5rem 0;">✅ Note:</p>
    <p style="color: #f0f0f0; margin: 0; line-height: 1.6;">You can use the calculator at any time and save the results for future reference</p>
    </div>
    """, unsafe_allow_html=True)

# Divider
st.markdown("---")

# Get Started Now
st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 2rem 0; box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4); color: white;">
    <h2 style="color: white; border-bottom: 3px solid #ffeb3b; margin-top: 0;">🚀 Ready to Get Started?</h2>
    <p style="font-size: 1.1rem; color: #f0f0f0; font-weight: 500;">
    Go to the <strong style="color: #ffeb3b;">VLSM Calculator</strong> page and start your calculations now!
    </p>
    </div>
""", unsafe_allow_html=True)

# Footer with application information
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white;">
    <h3 style="color: #ffeb3b; margin-top: 0;">ℹ️ About the Application</h3>
    <p style="color: #f0f0f0; line-height: 1.6;">An advanced web application for calculating IP networks using modern VLSM technology</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 1.5rem; border-radius: 10px; color: white;">
    <h3 style="color: #fffacd; margin-top: 0;">🔗 Main Sections</h3>
    <p style="color: #f0f0f0; margin: 0.5rem 0; line-height: 1.6;">
    🏠 Home Page<br>
    🧮 VLSM Calculator<br>
    📊 History & Records
    </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); padding: 1.5rem; border-radius: 10px; color: white;">
    <h3 style="color: #ffeb3b; margin-top: 0;">📅 Information</h3>
    <p style="color: #f0f0f0; margin: 0.5rem 0; line-height: 1.6;">
    📝 Last Update: {datetime.now().strftime('%m/%d/%Y')}<br>
    📦 Version: 1.0.0<br>
    🟢 Status: Running normally
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #ffffff; padding: 1.5rem; background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); border-radius: 10px;">
<p style="font-weight: 600; margin: 0; font-size: 1rem;">VLSM Calculator App © 2026 | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
