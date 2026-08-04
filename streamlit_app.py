import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SQL AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:5000"
REQUEST_TIMEOUT = 120

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Success/Error boxes */
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    /* Chat input */
    .stChatInput {
        border-radius: 10px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0
    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"
    if "db_stats" not in st.session_state:
        st.session_state.db_stats = {}

initialize_session_state()

# ============================================================================
# API FUNCTIONS
# ============================================================================

def check_api_health() -> Dict[str, Any]:
    """Check API health status."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"success": False, "data": {"status": "unavailable"}}
    except:
        return {"success": False, "data": {"status": "unavailable"}}

def make_query_request(question: str) -> Optional[Dict[str, Any]]:
    """Make API request to process question."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/getAnswer",
            json={"question": question},
            timeout=REQUEST_TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            st.session_state.request_count += 1
            return response.json()
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            st.error(f"❌ API Error {response.status_code}: {error_data.get('message', 'Unknown error')}")
            return None
    
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None
    
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Please ensure the backend is running on port 5000.")
        return None
    
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        return None

def get_database_stats() -> Optional[Dict[str, Any]]:
    """Get database statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/getStats", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# ============================================================================
# UI HELPER FUNCTIONS
# ============================================================================

def display_sql_result(data: Dict[str, Any]):
    """Display SQL query results."""
    query = data.get("query", "")
    query_result = data.get("query_result")
    summary = data.get("summary")
    
    st.success("✅ Query executed successfully")
    
    # Display SQL Query
    with st.expander("📝 Generated SQL Query", expanded=True):
        st.code(query, language="sql")
        
        # Copy button simulation
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("📋 Copy", key=f"copy_{hash(query)}"):
                st.toast("Query copied to clipboard!")
    
    # Display Results
    if query_result is not None:
        with st.expander("📊 Query Results", expanded=True):
            if isinstance(query_result, list):
                if len(query_result) > 0:
                    try:
                        # Convert to DataFrame
                        df = pd.DataFrame(query_result)
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Rows", len(df))
                        with col2:
                            st.metric("Total Columns", len(df.columns))
                        with col3:
                            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                        
                        st.dataframe(df, use_container_width=True, height=400)
                        
                        # Download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name=f"query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.warning(f"Could not convert to DataFrame: {str(e)}")
                        st.json(query_result)
                else:
                    st.info("✨ Query executed successfully but returned no results.")
            else:
                st.write(query_result)
    
    # Display Summary
    if summary:
        with st.expander("💡 AI Summary", expanded=True):
            st.markdown(f"**{summary}**")

def display_error(data: Dict[str, Any]):
    """Display error messages."""
    error = data.get("error", "Unknown error")
    query = data.get("query", "")
    
    st.error("❌ An error occurred while processing your request")
    
    # Show query if available
    if query:
        with st.expander("📝 Generated SQL Query", expanded=False):
            st.code(query, language="sql")
    
    with st.expander("⚠️ Error Details", expanded=True):
        st.error(error)
        
        # Provide helpful suggestions
        st.markdown("**💡 Suggestions:**")
        st.markdown("- Check if the table/column names are correct")
        st.markdown("- Verify your database connection")
        st.markdown("- Try rephrasing your question")

def display_normal_response(data: Dict[str, Any]):
    """Display normal text response."""
    result = data.get("result", "")
    
    if result:
        st.info("💬 Response")
        with st.expander("📄 Details", expanded=True):
            st.markdown(result)
    else:
        st.markdown("""
        ### 🤖 Welcome to SQL AI Agent!
        
        I can help you query your database using natural language. Here's what I can do:
        
        - 📊 Generate SQL queries from your questions
        - 🔍 Retrieve and analyze data
        - 📈 Provide summaries and insights
        
        **Try asking me something!** 👇
        """)

def create_message_dict(role: str, content: str, **kwargs) -> Dict[str, Any]:
    """Create a standardized message dictionary."""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        **kwargs
    }
    return message

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bot.png", width=80)
    st.title("SQL AI Agent")
    
    st.divider()
    
    # API Health Status
    st.subheader("🔌 System Status")
    health_data = check_api_health()
    
    if health_data.get("success"):
        services = health_data.get("data", {}).get("services", {})
        
        col1, col2 = st.columns(2)
        with col1:
            api_status = services.get("api", "unknown")
            if api_status == "operational":
                st.success("✅ API")
            else:
                st.error("❌ API")
        
        with col2:
            db_status = services.get("database", "unknown")
            if db_status == "operational":
                st.success("✅ Database")
            else:
                st.error("❌ Database")
    else:
        st.error("❌ System Offline")
    
    st.divider()
    
    # Database Statistics
    st.subheader("📊 Database Stats")
    stats_data = get_database_stats()
    
    if stats_data and stats_data.get("success"):
        stats = stats_data.get("data", {}).get("statistics", {})
        for table, count in stats.items():
            st.metric(table.capitalize(), f"{count:,}")
    else:
        st.info("Stats unavailable")
    
    st.divider()
    
    # Session Statistics
    st.subheader("📈 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.request_count)
    with col2:
        st.metric("Messages", len(st.session_state.messages))
    
    st.divider()
    
    # Example Questions
    st.subheader("💡 Example Questions")
    
    examples = [
        "Show all customers",
        "List active customers",
        "Top 5 expensive products",
        "Count total orders",
        "Average order value",
        "Products with low stock",
        "Recent orders this month"
    ]
    
    for example in examples:
        if st.button(f"💬 {example}", key=f"ex_{example}", use_container_width=True):
            st.session_state.example_clicked = example
    
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.request_count = 0
        st.rerun()
    
    st.divider()
    
    # Footer
    st.caption("Built with ❤️ using Streamlit & Flask")
    st.caption(f"Version 1.0.0 | {datetime.now().strftime('%Y')}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title("🤖 SQL AI Agent")
st.caption("💬 Ask questions about your database in natural language")

# ============================================================================
# CHAT HISTORY DISPLAY
# ============================================================================

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant":
            # Error Response
            if message.get("has_error"):
                display_error(message)
            
            # SQL Success Response
            elif message.get("has_query"):
                display_sql_result(message)
            
            # Normal Response
            else:
                display_normal_response(message)

# ============================================================================
# HANDLE EXAMPLE CLICKS
# ============================================================================

if hasattr(st.session_state, 'example_clicked'):
    prompt = st.session_state.example_clicked
    delattr(st.session_state, 'example_clicked')
else:
    prompt = st.chat_input("💭 Ask a question about your database...")

# ============================================================================
# USER INPUT PROCESSING
# ============================================================================

if prompt:
    # Display user message
    user_message = create_message_dict("user", prompt)
    st.session_state.messages.append(user_message)
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("🔄 Processing your question..."):
            response_data = make_query_request(prompt)
            
            if response_data and response_data.get("success"):
                # Determine response type
                has_query = response_data.get("has_query", False)
                has_error = response_data.get("has_error", False)
                
                # Create assistant message
                if has_error:
                    content = "❌ Error occurred"
                    display_error(response_data)
                elif has_query:
                    content = "✅ Query executed successfully"
                    display_sql_result(response_data)
                else:
                    content = "💬 Response"
                    display_normal_response(response_data)
                
                # Save to session state
                assistant_message = create_message_dict(
                    "assistant",
                    content,
                    **response_data
                )
                st.session_state.messages.append(assistant_message)
            
            elif response_data and not response_data.get("success"):
                # API returned error
                error_content = "❌ Request failed"
                st.error(response_data.get("error", "Unknown error"))
                
                assistant_message = create_message_dict(
                    "assistant",
                    error_content,
                    has_error=True,
                    error=response_data.get("message", "Unknown error")
                )
                st.session_state.messages.append(assistant_message)
            
            else:
                # No response from API
                error_content = "❌ Failed to connect to API"
                st.error("Please check if the backend server is running.")
                
                assistant_message = create_message_dict(
                    "assistant",
                    error_content,
                    has_error=True,
                    error="Connection failed"
                )
                st.session_state.messages.append(assistant_message)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("💡 **Tip:** Click example questions in the sidebar")
with col2:
    st.caption("🔍 **Pro Tip:** Be specific in your questions")
with col3:
    st.caption(f"⏰ Last updated: {datetime.now().strftime('%H:%M:%S')}")