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
        label="USA",
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
        "DOW Jones": "https://www.google.com/finance/quote/.DJI:INDEXDJX",
        "S&P 500": "https://www.google.com/finance/quote/.INX:INDEXSP",
        "NASDAQ": "https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ",
        "Russell 2000": "https://www.google.com/finance/quote/RUT:INDEXRUSSELL"
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
        "DOW Jones": "https://www.google.com/finance/quote/.DJI:INDEXDJX",
        "S&P 500": "https://www.google.com/finance/quote/.INX:INDEXSP",
        "NASDAQ": "https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ",
        "Russell 2000": "https://www.google.com/finance/quote/RUT:INDEXRUSSELL"
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
        if index_name == "DOW Jones":
            container3.caption(
                '''The Dow Jones Industrial Average (DJIA), often referred to simply as "the Dow," 
                is one of the oldest and most widely recognized stock market indices in the world.
                Established in 1896 by Charles Dow and Edward Jones, it tracks 30 large, publicly-owned
                companies trading on the New York Stock Exchange (NYSE) and the NASDAQ. The DJIA is a 
                price-weighted index, meaning that the stocks with higher prices have a greater 
                influence on the index's performance. It includes well-known companies like Apple,
                Boeing, and Goldman Sachs. The DJIA serves as a barometer for the overall health of the
                U.S. economy and is often used by investors and analysts to gauge market trends.'''
            )
        elif index_name == "S&P 500":
            container3.caption(
                '''The S&P 500, or Standard & Poor's 500, is a market-capitalization-weighted index
                that includes 500 of the largest publicly traded companies in the United States.
                Launched in 1957, it is one of the most commonly followed equity indices. The S&P 500
                represents approximately 80% of the total market value of U.S. stocks, making it a key
                indicator of overall market performance. Companies in the S&P 500 are selected based on 
                their market size, liquidity, and industry grouping, and include giants like Microsoft,
                Amazon, and Johnson & Johnson. The index is widely used as a benchmark for mutual
                funds and other investment vehicles.'''
            )
        
        elif index_name == "NASDAQ":
            container3.caption(
                '''The NASDAQ Composite is a stock market index that includes almost all the stocks 
                listed on the NASDAQ stock exchange, totaling over 3,000 stocks. Established in 1971, 
                the NASDAQ Composite is heavily weighted towards technology and internet-related 
                companies, making it a good indicator of the performance of the tech sector. Some of
                the most notable companies in the NASDAQ Composite include Apple, Amazon, Google, and
                Facebook. Unlike the DJIA, the NASDAQ Composite is a market-capitalization-weighted 
                index, meaning the largest companies have the greatest impact on the index's 
                performance.'''
            )
                
        elif index_name == "Russell 2000":
            container3.caption(
                '''The Russell 2000 is a stock market index that measures the performance of the
                2,000 smallest companies in the Russell 3000 Index, which is made up of the 3,000 
                largest U.S. stocks. Introduced in 1984, the Russell 2000 is a widely used benchmark
                for small-cap stocks in the United States. It includes companies from various sectors, 
                providing a broad perspective on the performance of smaller, domestically-focused firms.
                The index is market-capitalization-weighted and serves as a key performance indicator
                for small-cap mutual funds and other investment products focused on smaller companies.'''
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
    DJ_price, DJ_changes = index_scraper("DOW Jones")
    SP_price, SP_changes = index_scraper("S&P 500")
    NASDAQ_price, NASDAQ_changes = index_scraper("NASDAQ")
    Russell_price, Russell_changes = index_scraper("Russell 2000")
    
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
    
    st.caption("Please hit refresh button to get the latest data")     
        
         
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cont1 = st.container(border=True)
        cont1.metric("DOW Jones", st.session_state.DJ_price, st.session_state.DJ_changes)
    with col2:
        cont2 = st.container(border=True)
        cont2.metric("S&P 500", st.session_state.SP_price, st.session_state.SP_changes)
    with col3:
        cont3 = st.container(border=True)
        cont3.metric("NASDAQ", st.session_state.NASDAQ_price, st.session_state.NASDAQ_changes)
    with col4:
        cont4 = st.container(border=True)
        cont4.metric("Russell 2000", st.session_state.Russell_price, st.session_state.Russell_changes)
    
    st.markdown("<hr>", unsafe_allow_html=True)    
    selected_index = st.selectbox("Select an index", ["DOW Jones", "S&P 500", "NASDAQ", "Russell 2000"], key="index")
    interval = st.session_state.interval

    get_index_data(selected_index, interval)
    
    # Automatically refresh the data
    last_refresh = st.session_state.get('last_refresh', 0)
    if time.time() - last_refresh > 10:
        update_metrics()
        st.session_state.last_refresh = time.time()
        st.experimental_rerun() 
    
    
    

main()