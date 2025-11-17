"""
Streamlit UI for Data Insights App - Chat with Data Capstone Project
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging
from database import get_db_connection, get_table_info, execute_query, create_database
from agent import DataInsightsAgent
import os

# Configure logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Data Insights App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db_info" not in st.session_state:
    st.session_state.db_info = None

# Initialize database
DB_PATH = "sales_data.db"
# Auto-initialize database if it doesn't exist
if not os.path.exists(DB_PATH):
    logger.info("Database not found. Creating new database...")
    create_database(DB_PATH)
    logger.info("Database created successfully")

try:
    if st.session_state.db_info is None:
        st.session_state.db_info = get_table_info(DB_PATH)
except Exception as e:
    logger.error(f"Error loading database info: {e}")
    st.session_state.db_info = {}


def initialize_agent():
    """Initialize the AI agent."""
    try:
        if st.session_state.agent is None:
            st.session_state.agent = DataInsightsAgent()
            logger.info("Agent initialized successfully")
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        logger.error(f"Agent initialization error: {e}")
        return False


def get_sample_queries():
    """Get sample queries for users."""
    return [
        "What are the top 5 products by total sales?",
        "Show me sales by region",
        "Which customer has the highest total spending?",
        "What is the average order value?",
        "Show sales trends over the last 6 months",
        "Which sales rep has the most sales?",
        "What are the best selling categories?",
        "Show me all sales from North America"
    ]


def display_business_info():
    """Display business information dashboard."""
    st.sidebar.header("📊 Business Overview")
    
    if st.session_state.db_info:
        total_sales = st.session_state.db_info.get("sales", {}).get("row_count", 0)
        total_customers = st.session_state.db_info.get("customers", {}).get("row_count", 0)
        
        st.sidebar.metric("Total Sales Records", total_sales)
        st.sidebar.metric("Total Customers", total_customers)
        
        # Get aggregated data
        try:
            conn = get_db_connection(DB_PATH)
            
            # Total revenue
            revenue_df = pd.read_sql_query(
                "SELECT SUM(total_amount) as total_revenue FROM sales",
                conn
            )
            total_revenue = revenue_df.iloc[0]['total_revenue']
            st.sidebar.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            # Top products
            top_products_df = pd.read_sql_query("""
                SELECT product, SUM(total_amount) as revenue
                FROM sales
                GROUP BY product
                ORDER BY revenue DESC
                LIMIT 5
            """, conn)
            
            if not top_products_df.empty:
                st.sidebar.subheader("Top 5 Products")
                for idx, row in top_products_df.iterrows():
                    st.sidebar.text(f"{idx+1}. {row['product']}: ${row['revenue']:,.2f}")
            
            # Sales by region chart
            region_df = pd.read_sql_query("""
                SELECT region, SUM(total_amount) as revenue
                FROM sales
                GROUP BY region
                ORDER BY revenue DESC
            """, conn)
            
            if not region_df.empty:
                fig_region = px.pie(
                    region_df,
                    values='revenue',
                    names='region',
                    title="Sales by Region"
                )
                st.sidebar.plotly_chart(fig_region, use_container_width=True)
            
            conn.close()
        except Exception as e:
            logger.error(f"Error loading business info: {e}")
            st.sidebar.error("Error loading business information")


def display_sample_queries():
    """Display sample queries."""
    st.sidebar.header("💡 Sample Queries")
    sample_queries = get_sample_queries()
    for query in sample_queries:
        if st.sidebar.button(query, key=f"sample_{query}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()


def display_contact_info():
    """Display contact information."""
    st.sidebar.header("📧 Contact")
    st.sidebar.info(
        "Need help? Ask the agent to create a support ticket, "
        "or contact support@datainsights.com"
    )


def main():
    """Main application."""
    st.title("📊 Data Insights App")
    st.markdown("**Chat with your data using AI-powered insights**")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        
        if st.button("🔄 Reset Chat", use_container_width=True):
            if st.session_state.agent:
                st.session_state.agent.reset_conversation()
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        display_business_info()
        st.divider()
        display_sample_queries()
        st.divider()
        display_contact_info()
    
    # Initialize agent
    if not initialize_agent():
        st.stop()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with Data")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about the sales data..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.agent.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.header("📈 Quick Insights")
        
        try:
            conn = get_db_connection(DB_PATH)
            
            # Sales trend chart
            trend_df = pd.read_sql_query("""
                SELECT date, SUM(total_amount) as daily_revenue
                FROM sales
                GROUP BY date
                ORDER BY date
            """, conn)
            
            if not trend_df.empty:
                trend_df['date'] = pd.to_datetime(trend_df['date'])
                fig_trend = px.line(
                    trend_df,
                    x='date',
                    y='daily_revenue',
                    title="Sales Trend Over Time",
                    labels={'daily_revenue': 'Revenue ($)', 'date': 'Date'}
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            
            # Category distribution
            category_df = pd.read_sql_query("""
                SELECT category, SUM(total_amount) as revenue
                FROM sales
                GROUP BY category
                ORDER BY revenue DESC
            """, conn)
            
            if not category_df.empty:
                fig_category = px.bar(
                    category_df,
                    x='category',
                    y='revenue',
                    title="Revenue by Category",
                    labels={'revenue': 'Revenue ($)', 'category': 'Category'}
                )
                st.plotly_chart(fig_category, use_container_width=True)
            
            # Top customers table
            customers_df = pd.read_sql_query("""
                SELECT customer, SUM(total_amount) as total_spent, COUNT(*) as order_count
                FROM sales
                GROUP BY customer
                ORDER BY total_spent DESC
                LIMIT 10
            """, conn)
            
            if not customers_df.empty:
                st.subheader("Top 10 Customers")
                st.dataframe(
                    customers_df.style.format({
                        'total_spent': '${:,.2f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            conn.close()
        except Exception as e:
            logger.error(f"Error loading quick insights: {e}")
            st.error("Error loading insights")


if __name__ == "__main__":
    main()

