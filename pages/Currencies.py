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
        label="Currency Exchange",
        description='''Here you can explore our real-time currency exchange dashboard, offering
        live updates on currency rates from around the world. Monitor fluctuations and trends with
        detailed charts and analytics. Stay informed with comprehensive insights into currency market
        movements and global financial dynamics.''',
        color_name="violet-70",  
    )
    
    
@st.cache_data
def load_data(file_name):
    try:
        # Replace any slashes in the file name with spaces
        sanitized_file_name = file_name.replace("/", " ")
        
        # Construct the path to the data file
        file_path = os.path.join("Index_data", f"{sanitized_file_name}.csv")
        
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
        "USD/INR": "https://www.google.com/finance/quote/USD-INR",
        "EUR/INR": "https://www.google.com/finance/quote/EUR-INR",
        "GBP/INR": "https://www.google.com/finance/quote/GBP-INR",
        "AUD/INR": "https://www.google.com/finance/quote/AUD-INR"
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
        "USD/INR": "https://www.google.com/finance/quote/USD-INR",
        "EUR/INR": "https://www.google.com/finance/quote/EUR-INR",
        "GBP/INR": "https://www.google.com/finance/quote/GBP-INR",
        "AUD/INR": "https://www.google.com/finance/quote/AUD-INR"
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
                st.rerun()
        with col2:
            if st.button("Month"):
                st.session_state.interval = 'Month'
                st.rerun()
        with col3:
            if st.button("Year"):
                st.session_state.interval = 'Year'
                st.rerun()
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
        if index_name == "USD/INR":
            container3.caption(
                '''This pair shows the exchange rate between the US Dollar (USD) and the Indian Rupee 
                (INR). It indicates how many Indian Rupees are required to purchase one US Dollar. As
                one of the most traded currency pairs, it reflects the economic relationship between
                the world's largest economy and India.'''
            )
        elif index_name == "EUR/INR":
            container3.caption(
                '''This pair represents the exchange rate between the Euro (EUR) and the Indian Rupee 
                (INR). It tells you how many Indian Rupees are needed to buy one Euro. This rate is 
                important for trade and investment between the Eurozone and India, reflecting the
                economic dynamics between these regions.'''
            )
        elif index_name == "GBP/INR":
            container3.caption(
                '''This pair denotes the exchange rate between the British Pound Sterling (GBP) and 
                the Indian Rupee (INR). It indicates how many Indian Rupees are required to obtain one
                British Pound. The GBP/INR rate is significant for trade, financial transactions, and
                investments involving the UK and India.'''
            )
        elif index_name == "AUD/INR":
            container3.caption(
                ''' This pair shows the exchange rate between the Australian Dollar (AUD) and the Indian
                Rupee (INR). It reflects how many Indian Rupees are needed to acquire one Australian
                Dollar. This rate is essential for trade and economic interactions between Australia
                and India, influencing business decisions and financial strategies.'''
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
    DJ_price, DJ_changes = index_scraper("USD/INR")
    SP_price, SP_changes = index_scraper("EUR/INR")
    NASDAQ_price, NASDAQ_changes = index_scraper("GBP/INR")
    Russell_price, Russell_changes = index_scraper("AUD/INR")
    
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
        st.rerun()  
        
    st.caption("Please hit refresh button to get the latest data")    
         
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cont1 = st.container(border=True)
        cont1.metric("USD/INR", st.session_state.DJ_price, st.session_state.DJ_changes)
    with col2:
        cont2 = st.container(border=True)
        cont2.metric("EUR/INR", st.session_state.SP_price, st.session_state.SP_changes)
    with col3:
        cont3 = st.container(border=True)
        cont3.metric("GBP/INR", st.session_state.NASDAQ_price, st.session_state.NASDAQ_changes)
    with col4:
        cont4 = st.container(border=True)
        cont4.metric("AUD/INR)", st.session_state.Russell_price, st.session_state.Russell_changes)
    
    st.markdown("<hr>", unsafe_allow_html=True)    
    selected_index = st.selectbox("Select an index", ["USD/INR", "EUR/INR", "GBP/INR", "AUD/INR"], key="index")
    interval = st.session_state.interval

    get_index_data(selected_index, interval)
    
    # Automatically refresh the data
    last_refresh = st.session_state.get('last_refresh', 0)
    if time.time() - last_refresh > 10:
        update_metrics()
        st.session_state.last_refresh = time.time()
        st.rerun() 
    
    
    

main()