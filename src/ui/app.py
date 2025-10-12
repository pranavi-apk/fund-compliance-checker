"""
Streamlit Web Application for Investment Fund Compliance Checker
Clean black-themed UI for Hong Kong regulatory compliance analysis
"""
import streamlit as st
import os
import json
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core import ComplianceChecker
import plotly.graph_objects as go
import time

# Page configuration
st.set_page_config(
    page_title="Fund Compliance Checker",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean CSS for black theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E0E0E;
        color: #FFFFFF;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Better spacing for containers */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Cleaner cards */
    .stExpander {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    
    /* Success/Error states */
    .stSuccess {
        background-color: #1A3A1A;
        border: 1px solid #2D5A2D;
        border-radius: 6px;
    }
    
    .stError {
        background-color: #3A1A1A;
        border: 1px solid #5A2D2D;
        border-radius: 6px;
    }
    
    .stWarning {
        background-color: #3A3A1A;
        border: 1px solid #5A5A2D;
        border-radius: 6px;
    }
    
    /* Clean buttons */
    .stButton > button {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #404040;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3A3A3A;
        border-color: #505050;
        transform: translateY(-1px);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #404040;
        border-radius: 8px;
        padding: 2rem;
        background-color: #1A1A1A;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #FFFFFF;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #CCCCCC;
    }
    
    /* Clean tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1A1A1A;
        border-radius: 6px 6px 0 0;
        padding: 0.75rem 1.5rem;
        color: #999999;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2A2A2A;
        color: #FFFFFF;
    }
    
    /* Better spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Clean code blocks */
    code {
        background-color: #1A1A1A;
        color: #00FF00;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'knowledge_base_built' not in st.session_state:
    st.session_state.knowledge_base_built = False
if 'checker' not in st.session_state:
    st.session_state.checker = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar - Clean Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("---")
    
    # Model selection
    st.subheader("AI Model")
    llm_model = st.selectbox(
        "Select Model",
        ["llama3.1:8b", "llama2:latest", "llama3.2"],
        help="Choose the language model for analysis"
    )
    
    st.markdown("---")
    
    # Regulatory documents
    st.subheader("📚 Regulatory Documents")
    
    regulatory_docs = [
        "data/pdfs/fund manager code of conduct.pdf",
        "data/pdfs/Code_on_MPF_Investment_Funds.pdf"
    ]
    
    for doc in regulatory_docs:
        if os.path.exists(doc):
            st.success(f"✓ {os.path.basename(doc)}")
        else:
            st.error(f"✗ {os.path.basename(doc)}")
    
    # Build knowledge base
    if st.button("🔨 Build Knowledge Base", use_container_width=True):
        with st.spinner("Building regulatory knowledge base..."):
            try:
                checker = ComplianceChecker(
                    regulatory_pdfs=regulatory_docs,
                    llm_model=llm_model
                )
                checker.build_knowledge_base(cache_path="knowledge_base_cache.json")
                st.session_state.checker = checker
                st.session_state.knowledge_base_built = True
                st.success("Knowledge base ready!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if st.session_state.knowledge_base_built:
        st.success("✅ Knowledge base built")
    
    st.markdown("---")
    st.caption("Built for Klares.io • Hong Kong Regulatory Standards")

# Main Content
st.title("📋 Fund Compliance Checker")
st.markdown("### AI-Powered Hong Kong Regulatory Analysis")
st.markdown("---")

# Status Section
if not st.session_state.knowledge_base_built:
    st.info("👈 Configure and build knowledge base to begin analysis")
    
    # Clean metrics layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Regulatory Documents", "2")
    with col2:
        st.metric("Compliance Areas", "3")
    with col3:
        st.metric("Status", "Ready")
else:
    # File Upload Section
    st.subheader("📄 Upload Prospectus")
    
    uploaded_file = st.file_uploader(
        "Drag and drop PDF file here",
        type=['pdf'],
        help="Upload investment fund prospectus for compliance analysis"
    )
    
    # Quick Test Files
    st.markdown("**Sample prospectuses:**")
    col1, col2, col3 = st.columns(3)
    
    test_files = {
        "E Fund ETF": "data/pdfs/20230504163240_1872.pdf",
        "ChinaAMC Global": "data/pdfs/E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf",
        "BlackRock Premier": "data/pdfs/blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf"
    }
    
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    
    with col1:
        if st.button("📊 E Fund ETF", use_container_width=True):
            st.session_state.selected_file = test_files["E Fund ETF"]
    with col2:
        if st.button("📊 ChinaAMC Global", use_container_width=True):
            st.session_state.selected_file = test_files["ChinaAMC Global"]
    with col3:
        if st.button("📊 BlackRock Premier", use_container_width=True):
            st.session_state.selected_file = test_files["BlackRock Premier"]
    
    st.markdown("---")
    
    # File Selection Status
    prospectus_path = None
    if uploaded_file:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        prospectus_path = temp_path
        st.session_state.selected_file = prospectus_path
    elif st.session_state.selected_file and os.path.exists(st.session_state.selected_file):
        prospectus_path = st.session_state.selected_file
    
    if prospectus_path:
        st.success(f"✅ **Selected:** {os.path.basename(prospectus_path)}")
        
        # Analysis Button
        if st.button("🔍 Analyze Compliance", type="primary", use_container_width=True):
            if not os.path.exists(prospectus_path):
                st.error("File not found")
                st.stop()
            
            # Analysis Progress
            with st.status("Analyzing compliance...", expanded=True) as status:
                st.write("📝 Extracting document text...")
                time.sleep(1)
                
                st.write("🧠 Running AI analysis...")
                if st.session_state.checker is None:
                    st.session_state.checker = ComplianceChecker(
                        regulatory_pdfs=regulatory_docs,
                        llm_model=llm_model
                    )
                    st.session_state.checker.build_knowledge_base(cache_path="knowledge_base_cache.json")
                
                violations = st.session_state.checker.check_prospectus(prospectus_path)
                
                st.write("📊 Generating report...")
                report = st.session_state.checker.generate_report(prospectus_path, violations)
                
                st.session_state.analysis_results = {
                    'violations': violations,
                    'report': report,
                    'prospectus_name': os.path.basename(prospectus_path),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                status.update(label="Analysis complete!", state="complete")
    
    # Display Results
    if st.session_state.analysis_results:
        st.markdown("## 📊 Analysis Results")
        
        results = st.session_state.analysis_results
        violations = results['violations']
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        critical_count = sum(1 for v in violations if v.severity == 'CRITICAL')
        warning_count = sum(1 for v in violations if v.severity == 'WARNING')
        
        with col1:
            st.metric("Total Issues", len(violations))
        with col2:
            st.metric("Critical", critical_count)
        with col3:
            st.metric("Warnings", warning_count)
        with col4:
            st.metric("Document", results['prospectus_name'][:15] + "...")
        
        st.markdown("---")
        
        # Visualizations
        if violations:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Issues by Type")
                type_counts = {}
                for v in violations:
                    type_counts[v.check_type] = type_counts.get(v.check_type, 0) + 1
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(type_counts.keys()),
                        y=list(type_counts.values()),
                        marker_color='#666666'
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='#0E0E0E',
                    paper_bgcolor='#0E0E0E',
                    font_color='#FFFFFF',
                    height=300,
                    margin=dict(t=30, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### ⚠️ Severity Breakdown")
                severity_counts = {'CRITICAL': critical_count, 'WARNING': warning_count}
                colors = ['#FF4444', '#FFAA44']
                
                fig = go.Figure(data=[
                    go.Pie(
                        labels=list(severity_counts.keys()),
                        values=list(severity_counts.values()),
                        marker=dict(colors=colors)
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='#0E0E0E',
                    paper_bgcolor='#0E0E0E',
                    font_color='#FFFFFF',
                    height=300,
                    margin=dict(t=30, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Findings
        st.markdown("### 🔍 Detailed Findings")
        
        if not violations:
            st.success("✅ No compliance issues detected")
        else:
            for i, violation in enumerate(violations, 1):
                with st.expander(f"{'🔴' if violation.severity == 'CRITICAL' else '⚠️'} {violation.check_type} - Page {violation.location_page}", expanded=i==1):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Severity", violation.severity)
                    with col2:
                        st.metric("Page", violation.location_page)
                    
                    st.markdown("**Issue**")
                    st.info(violation.issue)
                    
                    st.markdown("**Regulation**")
                    st.code(violation.regulation_citation)
                    
                    st.markdown("**Context**")
                    st.text(violation.location_text[:500] + "..." if len(violation.location_text) > 500 else violation.location_text)
        
        # Actions
        st.markdown("---")
        st.markdown("### 📤 Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Report",
                data=results['report'],
                file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                st.session_state.analysis_results = None
                st.session_state.selected_file = None
                st.rerun()

# Footer
st.markdown("---")
st.caption("Investment Fund Compliance Checker • Built for Klares.io • Powered by AI Analysis")