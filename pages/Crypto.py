import streamlit as st
import requests
import time
import pandas as pd
import os
from bs4 import BeautifulSoup
from streamlit_extras.colored_header import colored_header
import plotly.graph_objects as go



# Custom CSS for background color of the container
custom_css = """
<style>
.st-emotion-cache-qcpnpn { /* Targeting the specific container class */
    background-color: #262730; /* Change to your desired background color */
}
</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)


def page_title():
    
    colored_header(
        label="Crypto",
        description="Here you can explore our real-time stock market dashboard, providing live updates on market indices and breaking news alerts. Stay informed with curated insights into market developments and company news.",
        color_name="violet-70",  
    )
    
    
@st.cache_data
def load_data(file_name):
    try:
        # Construct the path to the data file
        file_path = os.path.join("Index_data", f"{file_name}.csv")
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            return None
        
        # Load the data
        data = pd.read_csv(file_path, header=0)
        return data
    
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None


def get_index_info(index_name):
    dict_index = {
        "Bitcoin": "https://www.google.com/finance/quote/BTC-INR",
        "Ethereum": "https://www.google.com/finance/quote/ETH-INR",
        "Cardano": "https://www.google.com/finance/quote/ADA-INR",
        "Dogecoin": "https://www.google.com/finance/quote/DOGE-INR"
    }
    
    url = dict_index.get(index_name)
    if not url:
        return None, None
        
    information = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find_all(class_="P6K39c")
        for i in data:
            information.append(i.text.replace(",", ""))
    
    return information 





def index_scraper(index_name):
    dict_index = {
        "Bitcoin": "https://www.google.com/finance/quote/BTC-INR",
        "Ethereum": "https://www.google.com/finance/quote/ETH-INR",
        "Cardano": "https://www.google.com/finance/quote/ADA-INR",
        "Dogecoin": "https://www.google.com/finance/quote/DOGE-INR"
    }
    
    url = dict_index.get(index_name)
    if not url:
        return None, None
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        price_elem = soup.find(class_="YMlKec fxKbKc")
        if price_elem:
            price = float(price_elem.text.replace(",", ""))
        else:
            price = None
        
        prev_close_elem = soup.find(class_="P6K39c")
        if prev_close_elem:
            prev_close = float(prev_close_elem.text.replace(",", ""))
        else:
            prev_close = None
        
        if price is not None and prev_close is not None:
            change_price = price - prev_close
            changes_per = round((change_price * 100) / price, 2)
        else:
            changes_per = None
    
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        price = None
        changes_per = None
    
    return price, changes_per


def plot_line_chart(x_axis, y_axis, index_name, interval):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=y_axis, mode='lines+markers', name='Price'))
    fig.update_layout(
        title=f'{index_name}',
        xaxis_title=f'{interval}',
        yaxis_title='Price',
        hovermode='x unified',  
        template='plotly_white'  
    )    
    return fig


def get_index_data(index_name, interval):
    data = load_data(index_name)
    x_axis, y_axis = filter_data(data, interval)
    fig = plot_line_chart(x_axis, y_axis, index_name, interval)
    
    # Display the plot and interval buttons in the same container    
    container = st.container( border=True)
    with container:
        
        # Buttons for interval selection
        col1, col2, col3, col4 = st.columns([1,1.3,1,8])
        with col1:
            if st.button("Day"):
                st.session_state.interval = 'Day'
                st.experimental_rerun()
        with col2:
            if st.button("Month"):
                st.session_state.interval = 'Month'
                st.experimental_rerun()
        with col3:
            if st.button("Year"):
                st.session_state.interval = 'Year'
                st.experimental_rerun()
        with col4:
            pass  
        # Plot the chart
        st.plotly_chart(fig)
        
    # Display additional index info
    col1 , col2 = st.columns([1,1])
    with col1:
        container3 = st.container(border=True)
        container3.write("About")
        container3.markdown("<hr style='margin-top: 0.7px; margin-bottom: 10px;'>", unsafe_allow_html=True)
        if index_name == "Bitcoin":
            container3.caption(
                '''Bitcoin, introduced in 2009 by the mysterious Satoshi Nakamoto, is the first 
                decentralized digital currency. It was designed as a peer-to-peer electronic cash 
                system that allows for secure, borderless transactions without the need for a central
                authority. Bitcoin operates on a blockchain, a public ledger that records all
                transactions, ensuring transparency and security. Its primary use is as a store of value
                and medium of exchange, often referred to as "digital gold" due to its limited supply 
                and deflationary nature.'''
            )
        elif index_name == "Ethereum":
            container3.caption(
                '''Ethereum, launched in 2015 by Vitalik Buterin, revolutionized the blockchain space
                by introducing the concept of smart contracts. These are self-executing contracts with
                the terms directly written into code, enabling automated, trustless transactions and
                applications. Ethereum's blockchain serves as a platform for decentralized applications 
                (dApps), which has spurred innovation in areas like decentralized finance (DeFi) and
                non-fungible tokens (NFTs). Unlike Bitcoin, which focuses primarily on value transfer,
                Ethereum provides a versatile foundation for a wide array of blockchain-based solutions 
                and services.'''
            )
                
    with col2:    
        container4 = st.container(border=True)
        container4.write("Index")
        container4.markdown("<hr style='margin-top: 1px; margin-bottom: 12px;'>", unsafe_allow_html=True)
        
        info = get_index_info(index_name)
        container4.markdown(f"<b>Previous close: </b> <span style='font-weight:bold; font-size:larger; color:green'>{info[0]}</span>", unsafe_allow_html=True)
        container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
        container4.markdown("<b>Day range: </b> <span style='font-weight:bold; font-size:larger; color:green'>N/A</span>", unsafe_allow_html=True)
        container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
        container4.markdown("<b>Year range: </b> <span style='font-weight:bold; font-size:larger; color:green'>N/A</span>", unsafe_allow_html=True)
        container4.markdown("</br>", unsafe_allow_html=True)



def filter_data(data, interval):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %H:%M:%S')
    df.set_index('Date', inplace=True)

    if interval == "Day":
        df_resampled = df.resample('D').mean().reset_index()
    elif interval == "Month":
        df_resampled = df.resample('M').mean().reset_index()
    elif interval == "Year":
        df_resampled = df.resample('Y').mean().reset_index()
    
    return df_resampled['Date'].tolist(), df_resampled['Close'].tolist()


    

def update_metrics():
    DJ_price, DJ_changes = index_scraper("Bitcoin")
    SP_price, SP_changes = index_scraper("Ethereum")
    NASDAQ_price, NASDAQ_changes = index_scraper("Cardano")
    Russell_price, Russell_changes = index_scraper("Dogecoin")
    
    # Store fetched values in session state
    st.session_state.DJ_price = DJ_price
    st.session_state.DJ_changes = DJ_changes
    st.session_state.SP_price = SP_price
    st.session_state.SP_changes = SP_changes
    st.session_state.NASDAQ_price = NASDAQ_price
    st.session_state.NASDAQ_changes = NASDAQ_changes
    st.session_state.Russell_price = Russell_price
    st.session_state.Russell_changes = Russell_changes


def main():
    page_title()  
    st.markdown("</br>", unsafe_allow_html=True)
    
    # Initialize session state for metrics and interval
    if 'DJ_price' not in st.session_state:
        st.session_state.DJ_price = 0.0
        st.session_state.DJ_changes = 0.0
        st.session_state.SP_price = 0.0
        st.session_state.SP_changes = 0.0
        st.session_state.NASDAQ_price = 0.0
        st.session_state.NASDAQ_changes = 0.0
        st.session_state.Russell_price = 0.0
        st.session_state.Russell_changes = 0.0      
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    if 'interval' not in st.session_state:
        st.session_state.interval = 'Year'         
                
    # Add a button to manually update the metrics
    if st.button("Refresh"):
        update_metrics()
        st.experimental_rerun()  
        
         
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cont1 = st.container(border=True)
        cont1.metric("Bitcoin (BTC/INR)", st.session_state.DJ_price, st.session_state.DJ_changes)
    with col2:
        cont2 = st.container(border=True)
        cont2.metric("Ethereum (ETH/INR)", st.session_state.SP_price, st.session_state.SP_changes)
    with col3:
        cont3 = st.container(border=True)
        cont3.metric("Cardano (ADA/INR)", st.session_state.NASDAQ_price, st.session_state.NASDAQ_changes)
    with col4:
        cont4 = st.container(border=True)
        cont4.metric("Dogecoin (DOGE/INR)", st.session_state.Russell_price, st.session_state.Russell_changes)
    
    st.markdown("<hr>", unsafe_allow_html=True)    
    selected_index = st.selectbox("Select an index", ["Bitcoin", "Ethereum"], key="index")
    interval = st.session_state.interval

    get_index_data(selected_index, interval)
    
    # Automatically refresh the data
    last_refresh = st.session_state.get('last_refresh', 0)
    if time.time() - last_refresh > 10:
        update_metrics()
        st.session_state.last_refresh = time.time()
        st.experimental_rerun() 
    
    
    

main()


