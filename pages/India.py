import streamlit as st
import requests
import pandas as pd
import time
import random
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


def index_scraper(index_name):
    if index_name == "SENSEX":
        url = f"https://www.google.com/finance/quote/{index_name}:INDEXBOM"
    else:
        url = f"https://www.google.com/finance/quote/{index_name}:INDEXNSE"
        
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find price and previous close
        price_elem = soup.find(class_="YMlKec fxKbKc")
        prev_close_elem = soup.find(class_="P6K39c")
        
        if price_elem and prev_close_elem:
            try:
                price = float(price_elem.text.replace(",", ""))
                prev_close = float(prev_close_elem.text.replace(",", ""))
                
                change_price = round(price - prev_close, 2)
                changes_per = round((change_price * 100) / price, 2)                
                return price, f"{changes_per}%"
            except ValueError:
                st.error(f"Error converting price data for {index_name}")
                return None
        else:
            st.error(f"Could not find required elements for {index_name}")
            return None
    else:
        st.error(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None 


    

def get_index_info(index_name):
    index_name_underscore = index_name.replace(" ", "_")
    if index_name_underscore == "SENSEX":
        url = f"https://www.google.com/finance/quote/{index_name_underscore}:INDEXBOM"
    else:
        url = f"https://www.google.com/finance/quote/{index_name_underscore}:INDEXNSE"
        
    information = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find_all(class_="P6K39c")
        for i in data:
            information.append(i.text.replace(",", ""))
    
    return information 




def generate_unique_key():
    return str(time.time()).replace(".", "")    
        
        
def generate_stock_key():
    key = random.randint(1, 10000000000000)
    return str(key + time.time()).replace(".", "")
                 
    
def page_title():
    
    colored_header(
        label="India",
        description="Here you can explore our real-time stock market dashboard, providing live updates on market indices and breaking news alerts. Stay informed with curated insights into market developments and company news.",
        color_name="violet-70",
    )

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
        if index_name == "SENSEX":
            container3.caption(
                '''The SENSEX is a stock market index comprising 30 of the largest and most actively
                traded stocks on the Bombay Stock Exchange (BSE). It is widely considered to be a 
                benchmark of the Indian stock market's performance. The SENSEX was introduced in 1986
                and has become one of the oldest and most well-known indices in India. It represents
                various sectors of the economy, providing a snapshot of the overall economic health 
                and investor sentiment in India.'''
            )
        elif index_name == "NIFTY 50":
            container3.caption(
                '''The NIFTY 50 is a stock market index that represents the performance of the 50 largest 
                and most liquid Indian companies listed on the National Stock Exchange (NSE). It is one of 
                the leading stock market indices in India and is widely used by investors and analysts to 
                track the performance of the Indian equity market. The NIFTY 50 is known for its diversified 
                composition, covering various sectors of the economy.'''
            )
        
        elif index_name == "NIFTY BANK":
            container3.caption(
                '''The NIFTY Bank Index is a stock market index that tracks the performance of the banking 
                sector in India. It comprises the most liquid and large-cap banking stocks listed on the 
                National Stock Exchange (NSE). The NIFTY Bank Index is widely used by investors and analysts 
                to gauge the performance of the banking sector and the overall health of the Indian economy.'''
            )
                
        elif index_name == "NIFTY IT":
            container3.caption(
                '''The NIFTY IT Index is a stock market index that tracks the performance of the information 
                technology (IT) sector in India. It comprises the most liquid and large-cap IT stocks listed on 
                the National Stock Exchange (NSE). The NIFTY IT Index is widely used by investors and analysts to 
                monitor the performance of the IT sector and the overall technology landscape in India.'''
            )
                
    with col2:    
        container4 = st.container(border=True)
        container4.write("Index")
        container4.markdown("<hr style='margin-top: 1px; margin-bottom: 12px;'>", unsafe_allow_html=True)
        
        info = get_index_info(index_name)
        container4.markdown(f"<b>Previous close: </b> <span style='font-weight:bold; font-size:larger; color:green'>{info[0]}</span>", unsafe_allow_html=True)
        container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
        container4.markdown(f"<b>Day range: </b> <span style='font-weight:bold; font-size:larger; color:green'>{info[1]}</span>", unsafe_allow_html=True)
        container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
        container4.markdown(f"<b>Year range: </b> <span style='font-weight:bold; font-size:larger; color:green'>{info[2]}</span>", unsafe_allow_html=True)
        container4.markdown("</br>", unsafe_allow_html=True)
        

 


def update_metrics():
    # Fetch index data
    DJ_price, DJ_changes = index_scraper("SENSEX")
    SP_price, SP_changes = index_scraper("NIFTY_50")
    NASDAQ_price, NASDAQ_changes = index_scraper("NIFTY_BANK")
    Russell_price, Russell_changes = index_scraper("NIFTY_IT")
    
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
    
    if 'interval' not in st.session_state:
        st.session_state.interval = 'Year'
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()    
    
    # Add a button to manually update the metrics
    if st.button("Refresh"):
        update_metrics()
        st.experimental_rerun()  

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cont1 = st.container(border=True)
        cont1.metric("SENSEX", st.session_state.DJ_price, st.session_state.DJ_changes)
    with col2:
        cont2 = st.container(border=True)
        cont2.metric("NIFTY 50", st.session_state.SP_price, st.session_state.SP_changes)
    with col3:
        cont3 = st.container(border=True)
        cont3.metric("NIFT BANK", st.session_state.NASDAQ_price, st.session_state.NASDAQ_changes)
    with col4:
        cont4 = st.container(border=True)
        cont4.metric("NIFTY IT", st.session_state.Russell_price, st.session_state.Russell_changes)
    
    st.markdown("<hr>", unsafe_allow_html=True)    

    # Selectbox for choosing index
    selected_index = st.selectbox("Select an Index", ["SENSEX", "NIFTY 50", "NIFTY BANK", "NIFTY IT"])
    interval = st.session_state.interval

    get_index_data(selected_index, interval)

    # Automatically refresh the data
    last_refresh = st.session_state.get('last_refresh', 0)
    if time.time() - last_refresh > 10:
        update_metrics()
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()   
           
 
main()
    