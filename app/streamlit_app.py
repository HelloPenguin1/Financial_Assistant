import streamlit as st
import sys
import os
import time

# Ensure root path access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from graph.builder import workflow
    from tools.vectorstore import clear_vectorstore
except ImportError:
    st.error("Could not import required modules. Please check your path configuration.")

# Page Configuration
st.set_page_config(
    page_title="SEC-Insight",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Professional Light Theme
st.markdown("""
    <style>
    /* Times New Roman / Professional Serif Font */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Times New Roman', Times, serif !important;
        color: #1a202c;
    }

    .main {
        background-color: #ffffff;
    }

    /* Professional Header Style */
    .header-style {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
        text-align: left;
    }

    .sub-header {
        color: #4a5568;
        font-size: 0.95rem;
        text-align: left;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1a202c !important;
        border-radius: 4px !important;
        border: 1px solid #cbd5e0 !important;
        padding: 8px !important;
        font-size: 0.9rem !important;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: background-color 0.2s;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Secondary/Clear Button */
    .clear-btn > div.stButton > button {
        background-color: #ef4444 !important;
        width: 100%;
    }
    .clear-btn > div.stButton > button:hover {
        background-color: #dc2626 !important;
    }

    /* Result Card Styling */
    .result-card {
        background-color: #fdfdfd;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        margin-top: 15px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #718096;
        text-align: center;
        padding: 8px;
        font-size: 0.75rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .footer span {
        color: #2563eb;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Project Overview")
    st.markdown("""
    **SEC-Insight** is a multi-agent financial analysis platform. 
    It leverages autonomous agents to:
    - **Decompose** complex financial queries.
    - **Fetch & Process** real-time SEC-EDGAR filings.
    - **Analyze** data across multiple companies.
    - **Synthesize** comprehensive reports.
    
    *Powered by LangGraph & Groq.*
    """)
    st.divider()
    st.markdown("### Database Management")
    if st.button("Clear Vectorstore", key="clear_vs"):
        msg = clear_vectorstore()
        st.success(msg)

# Main Header
st.markdown('<h1 class="header-style">SEC-Insight: An Agent Workflow for Financial Analysis with SEC-EDGAR Filings</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional multi-agent system for corporate disclosure analysis and financial intelligence.</p>', unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input Section
query = st.text_input("Analyze SEC Data", placeholder="e.g. Compare revenue growth of Apple and Microsoft for 2023", label_visibility="collapsed")
if st.button("Run Analysis"):
    if query:
        # Progress Tracking
        progress_bar = st.progress(0, text="Initializing workflow...")
        status_text = st.empty()
        
        # Approximate node count for progress estimation
        nodes = ["query_decomposer", "constructdb", "orchestrator", "retriever", "llm_call", "synthesizer", "llm_response"]
        
        try:
            # Stream the workflow to track nodes
            current_step = 0
            final_result = None
            
            # Using stream to track nodes
            for step in workflow.stream({"query": query}):
                current_step += 1
                progress = min(current_step / len(nodes), 0.95)
                
                # Get the node name from the step dictionary
                node_name = list(step.keys())[0]
                status_text.text(f"Currently visiting node: {node_name}")
                progress_bar.progress(progress, text=f"Processing {node_name}...")
                
                # Capture the final result state
                final_result = step[node_name]
                time.sleep(0.1) # Smoothness
            
            progress_bar.progress(1.0, text="Analysis Complete!")
            status_text.empty()
            
            # Extract output from the final state update
            output = None
            if "final_response" in final_result:
                output = final_result["final_response"]
            elif "final_report" in final_result:
                output = final_result["final_report"]
            else:
                # Fallback to the whole result if keys are missing
                output = final_result

            # Save history
            st.session_state.history.append({
                "query": query,
                "output": output
            })
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            progress_bar.empty()
    else:
        st.warning("Please enter a query.")

# Display latest result
if st.session_state.history:
    latest = st.session_state.history[-1]
    
    st.markdown("### 📊 Analysis Result")
    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        if isinstance(latest["output"], str):
            st.markdown(latest["output"])
        else:
            st.json(latest["output"])
        st.markdown('</div>', unsafe_allow_html=True)

# History Section (Collapsible)
if len(st.session_state.history) > 1:
    with st.expander("🕒 Recent Queries"):
        for item in reversed(st.session_state.history[:-1]):
            st.markdown(f"**Query:** {item['query']}")
            if isinstance(item['output'], str):
                st.markdown(f"{item['output'][:300]}...")
            st.markdown("---")

# Footer
st.markdown(
    """
    <div class="footer">
        Tools Used: <span>Langgraph, Langchain, ChromaDB, Groq Inference, OpenAI Embeddings, Streamlit, Langsmith, SEC-EDGAR Data</span>
    </div>
    """,
    unsafe_allow_html=True
)