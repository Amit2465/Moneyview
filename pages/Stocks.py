import streamlit as st
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from streamlit_extras.colored_header import colored_header
import plotly.graph_objects as go
import os



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
        label="Stocks",
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

# get stock information
def get_stock_info(stock_name):
    stock_urls = {
        "TCS": "https://www.google.com/finance/quote/TCS:NSE"
    }

    url = stock_urls.get(stock_name)
    if not url:
        return f"Stock name {stock_name} not found in dictionary."

    information = []
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve data for {stock_name}. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all(class_="P6K39c")
    
    for i in data:
        information.append(i.text.replace(",", ""))

    if len(information) < 8:
        return f"Failed to retrieve complete data for {stock_name}. Check the structure of the webpage."

    previous_close = information[0]
    day_range = information[1]
    year_range = information[2]
    market_cap = information[3]
    average_volume = information[4]
    PE_ratio = information[5]
    dividend_yield = information[6]
    primary_exchange = information[7]
    
    return previous_close, day_range, year_range, market_cap, average_volume, PE_ratio, dividend_yield, primary_exchange



def get_stock_info1(stock_name):
    stock_urls = {
        "TCS": "https://www.google.com/finance/quote/TCS:NSE"
    }

    url = stock_urls.get(stock_name)
    if not url:
        return f"Stock name {stock_name} not found in dictionary."

    information = []
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve data for {stock_name}. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all(class_="P6K39c")
    
    for i in data:
        information.append(i.text.replace(",", ""))

    if len(information) < 8:
        return f"Failed to retrieve complete data for {stock_name}. Check the structure of the webpage."
    
    ceo = information[9]
    founded = information[10]
    employee = information[12]
    
    return ceo, founded, employee
    
    
    
    

# get stock price
def get_stock_price(stock_name):
    stock_urls = {
        "TCS": "https://www.google.com/finance/quote/TCS:NSE"
    }

    url = stock_urls.get(stock_name)
    if not url:
        return f"Stock name {stock_name} not found in dictionary."
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract current price
    price_elem = soup.find(class_="YMlKec fxKbKc")
    if price_elem:
        price = float(price_elem.text.strip()[1:].replace(",", ""))
    else:
        price = None
    
    # Extract previous close
    prev_close_elem = soup.find(class_="P6K39c")
    if prev_close_elem:
        prev_close = float(prev_close_elem.text.strip()[1:].replace(",", ""))
    else:
        prev_close = None
    
    # Calculate change in price and percentage change
    if price is not None and prev_close is not None:
        change_price = price - prev_close
        changes_per = round((change_price * 100) / price, 2)
    else:
        change_price = None
        changes_per = None
    
    return price, f"{changes_per}%" 


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


def update_metrics(stock_name):
    stock_price , stock_exchang = get_stock_price(stock_name)
    # stored fetch value in session state
    st.session_state.stock_price = stock_price
    st.session_state.stock_exchang = stock_exchang



def company_info(stock_name):
    ceo, founded, employees = get_stock_info1(stock_name)
    container4 = st.container(border=True)
    container4.write("Info")
    container4.markdown("<hr style='margin-top: 1px; margin-bottom: 12px;'>", unsafe_allow_html=True)
    container4.markdown(f"<b>CEO: </b> <span style='font-weight:bold; font-size:larger; color:green'>{ceo}</span>", unsafe_allow_html=True)
    container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    container4.markdown(f"<b>Founded: </b> <span style='font-weight:bold; font-size:larger; color:green'>{founded}</span>", unsafe_allow_html=True)
    container4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    container4.markdown(f"<b>Employees: </b> <span style='font-weight:bold; font-size:larger; color:green'>{employees}</span>", unsafe_allow_html=True)
    
    container3 = st.container(border=True)
    container3.write("About")
    container3.markdown("<hr style='margin-top: 0.7px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    if stock_name == "TCS":
        container3.caption(
            '''TCS (Tata Consultancy Services) is a leading global IT services, consulting, and
            business solutions provider headquartered in Mumbai, India. Part of the Tata Group, 
            TCS offers a wide range of services, including software development, systems integration, 
            cloud computing, and consulting. Established in 1968, the company serves clients across 
            various industries and is renowned for its innovation, extensive global reach, and strong
            focus on digital transformation. TCS is a major player in the IT sector, known for its
            robust delivery model and commitment to driving business growth through technology.'''
        ) 
    

def company_info2(stock_name):
    pc , dr, yr, mc, av, pe, de, pre = get_stock_info(stock_name)
    cont4 = st.container(border=True)
    cont4.write("Stock")
    cont4.markdown("<hr style='margin-top: 1px; margin-bottom: 12px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Previous Close: </b> <span style='font-weight:bold; font-size:larger; color:green'>{pc}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Day range: </b> <span style='font-weight:bold; font-size:larger; color:green'>{dr}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Year range: </b> <span style='font-weight:bold; font-size:larger; color:green'>{yr}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Market cap: </b> <span style='font-weight:bold; font-size:larger; color:green'>{mc}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Average volume: </b> <span style='font-weight:bold; font-size:larger; color:green'>{av}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>P/E ratio: </b> <span style='font-weight:bold; font-size:larger; color:green'>{pe}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Dividend yield: </b> <span style='font-weight:bold; font-size:larger; color:green'>{de}</span>", unsafe_allow_html=True)
    cont4.markdown("<hr style='margin-top: 0.7px; margin-bottom: 4px;'>", unsafe_allow_html=True)
    cont4.markdown(f"<b>Primary Exchange: </b> <span style='font-weight:bold; font-size:larger; color:green'>{pre}</span>", unsafe_allow_html=True)
    cont4.markdown("</br>", unsafe_allow_html=True)
        


def main():
    page_title()
    # Initialize the session state for metrics and interval
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 0
    if 'stock_exchange' not in st.session_state:
        st.session_state.stock_exchang = 0
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    if 'interval' not in st.session_state:
        st.session_state.interval = 'Year'    
        
    stock_name = st.selectbox("Select a stock", ["TCS"])    
    interval = st.session_state.interval    
    
    if st.button("Refresh"):
        update_metrics(stock_name)
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()
    
    col1 , col2 = st.columns([1,4])
    with col1:
        container1 = st.container(border=True)    
        container1.metric(label=f"{stock_name}", value=st.session_state.stock_price, delta=st.session_state.stock_exchang)
    with col2:
        pass    
    
    get_index_data(stock_name, interval)
    
    col3, col4 = st.columns(2)
    with col3:
        company_info(stock_name)
    with col4:
        company_info2(stock_name)    
    
    # Automatically refresh the data every 10 seconds
    if time.time() - st.session_state.last_refresh > 10:
        update_metrics(stock_name)
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()    
 


main()        