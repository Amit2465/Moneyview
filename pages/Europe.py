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
        label="Europe",
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
        "DAX": "https://www.google.com/finance/quote/DAX:INDEXDB",
        "FTSE 100": "https://www.google.com/finance/quote/UKX:INDEXFTSE",
        "CAC 40": "https://www.google.com/finance/quote/PX1:INDEXEURO",
        "IBEX 35": "https://www.google.com/finance/quote/INDI:INDEXBME"
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
        "DAX": "https://www.google.com/finance/quote/DAX:INDEXDB",
        "FTSE 100": "https://www.google.com/finance/quote/UKX:INDEXFTSE",
        "CAC 40": "https://www.google.com/finance/quote/PX1:INDEXEURO",
        "IBEX 35": "https://www.google.com/finance/quote/INDI:INDEXBME"
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
        if index_name == "DAX":
            container3.caption(
                '''The DAX (Deutscher Aktienindex) is a stock market index consisting of the 40 largest
                and most liquid German companies trading on the Frankfurt Stock Exchange. Established
                in 1988, it serves as a key indicator of the performance of the German economy. Major
                companies in the DAX include Volkswagen, Siemens, and SAP. The index is
                market-capitalization-weighted and is one of the most followed indices in Europe.'''
            )
        elif index_name == "FTSE 100":
            container3.caption(
                '''The FTSE 100 (Financial Times Stock Exchange 100 Index) tracks the 100 largest
                companies listed on the London Stock Exchange by market capitalization. Launched in 1984
                , it is a crucial measure of the health of the UK economy. Prominent constituents 
                include HSBC, BP, and Unilever. The FTSE 100 is widely used by investors as a benchmark 
                for British equities.'''
            )
        
        elif index_name == "CAC 40":
            container3.caption(
                '''The CAC 40 (Cotation Assistée en Continu) represents the 40 largest companies on 
                the Euronext Paris exchange. Introduced in 1987, it is a benchmark for the French stock
                market and reflects the economic condition of France. Key companies in the CAC 40
                include L'Oréal, TotalEnergies, and Airbus. The index is market-capitalization-weighted 
                and is a primary gauge of French stock performance.'''
            )
                
        elif index_name == "IBEX 35":
            container3.caption(
                '''The IBEX 35 is a stock market index comprising the 35 most liquid stocks on the
                Bolsa de Madrid in Spain. Launched in 1992, it provides insight into the Spanish economy
                's performance. Major companies in the IBEX 35 include Banco Santander, Telefónica,
                and Inditex. The index is market-capitalization-weighted and is an important benchmark 
                for Spanish equities.'''
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
    Dax_price, Dax_changes = index_scraper("DAX")
    ftse_price, ftse_changes = index_scraper("FTSE 100")
    cac_price, cac_changes = index_scraper("CAC 40")
    ibex_price, ibex_changes = index_scraper("IBEX 35")
    
    # Store fetched values in session state
    st.session_state.Dax_price = Dax_price
    st.session_state.Dax_changes = Dax_changes
    st.session_state.ftse_price = ftse_price
    st.session_state.ftse_changes = ftse_changes
    st.session_state.cac_price = cac_price
    st.session_state.cac_changes = cac_changes
    st.session_state.ibex_price = ibex_price
    st.session_state.ibex_changes = ibex_changes


def main():
    page_title()  
    st.markdown("</br>", unsafe_allow_html=True)
    
    # Initialize session state for metrics and interval
    if 'Dax_price' not in st.session_state:
        st.session_state.Dax_price = 0.0
        st.session_state.Dax_changes = 0.0
        st.session_state.ftse_price = 0.0
        st.session_state.ftse_changes = 0.0
        st.session_state.cac_price = 0.0
        st.session_state.cac_changes = 0.0
        st.session_state.ibex_price = 0.0
        st.session_state.ibex_changes = 0.0      
    
    
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
        cont1.metric("DAX", st.session_state.Dax_price, st.session_state.Dax_changes)
    with col2:
        cont2 = st.container(border=True)
        cont2.metric("FTSE 100", st.session_state.ftse_price, st.session_state.ftse_changes)
    with col3:
        cont3 = st.container(border=True)
        cont3.metric("CAC 40", st.session_state.cac_price, st.session_state.cac_changes)
    with col4:
        cont4 = st.container(border=True)
        cont4.metric("IBEX 35", st.session_state.ibex_price, st.session_state.ibex_changes)
    
    st.markdown("<hr>", unsafe_allow_html=True)    
    selected_index = st.selectbox("Select an index", ["DAX", "FTSE 100", "CAC 40", "IBEX 35"], key="index1")
    interval = st.session_state.interval

    get_index_data(selected_index, interval)
    
    # Automatically refresh the data
    last_refresh = st.session_state.get('last_refresh', 0)
    if time.time() - last_refresh > 10:
        update_metrics()
        st.session_state.last_refresh = time.time()
        st.rerun() 
    
    
    

main()  