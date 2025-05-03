import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1.2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📈 Stock Market Dashboard")
st.markdown("Enter a stock symbol to view its financial data and performance.")

# Input for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL, MSFT)", "AAPL").upper()

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("End Date", datetime.now())

try:
    # Fetch stock data
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    
    # Get company info
    info = stock.info
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${info.get('currentPrice', 'N/A'):.2f}")
    with col2:
        st.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A'):.2f}")
    with col3:
        st.metric("52 Week Low", f"${info.get('fiftyTwoWeekLow', 'N/A'):.2f}")
    with col4:
        st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,.0f}")
    
    # Create price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        title=f"{symbol} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional financial information
    st.subheader("Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Key Statistics")
        st.markdown(f"""
        - **Sector:** {info.get('sector', 'N/A')}
        - **Industry:** {info.get('industry', 'N/A')}
        - **P/E Ratio:** {info.get('trailingPE', 'N/A')}
        - **Dividend Yield:** {info.get('dividendYield', 'N/A')*100:.2f}%
        """)
    
    with col2:
        st.markdown("### Financial Metrics")
        st.markdown(f"""
        - **Revenue:** ${info.get('totalRevenue', 'N/A'):,.0f}
        - **Profit Margin:** {info.get('profitMargins', 'N/A')*100:.2f}%
        - **Debt to Equity:** {info.get('debtToEquity', 'N/A'):.2f}
        - **Beta:** {info.get('beta', 'N/A'):.2f}
        """)

except Exception as e:
    st.error(f"Error fetching data for {symbol}. Please check the stock symbol and try again.")
    st.error(str(e)) 