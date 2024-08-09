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
    

def download_data(file_name):
    try:
        # Construct the path to the data file
        file_path = os.path.join("Index_data", f"{file_name}.csv")
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            return
        
        # Load the data into a DataFrame
        data = pd.read_csv(file_path)

        # Convert DataFrame to CSV for download
        csv_data = data.to_csv(index=False)
        
        # Provide download button
        st.download_button(
            label='Download',
            data=csv_data,
            file_name=f'{file_name}.csv',
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
     
    

# get stock information
def get_stock_info(stock_name):
    stock_urls = {
        "TCS": "https://www.google.com/finance/quote/TCS:NSE",
        "BlackRock": "https://www.google.com/finance/quote/BLK:NYSE",
        "Meta": "https://www.google.com/finance/quote/META:NASDAQ",
        "Google": "https://www.google.com/finance/quote/GOOG:NASDAQ",
        "Amazon": "https://www.google.com/finance/quote/AMZN:NASDAQ",
        "Nividia": "https://www.google.com/finance/quote/NVDA:NASDAQ",
        "Apple": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "SAP": "https://www.google.com/finance/quote/SAP:ETR",
        "Infosys": "https://www.google.com/finance/quote/INFY:NSE",
        "Tesla": "https://www.google.com/finance/quote/TSLA:NASDAQ",
        "HDFC bank": "https://www.google.com/finance/quote/HDFCBANK:NSE"
        
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
        "TCS": "https://www.google.com/finance/quote/TCS:NSE",
        "BlackRock": "https://www.google.com/finance/quote/BLK:NYSE",
        "Meta": "https://www.google.com/finance/quote/META:NASDAQ",
        "Google": "https://www.google.com/finance/quote/GOOG:NASDAQ",
        "Amazon": "https://www.google.com/finance/quote/AMZN:NASDAQ",
        "Nividia": "https://www.google.com/finance/quote/NVDA:NASDAQ",
        "Apple": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "SAP": "https://www.google.com/finance/quote/SAP:ETR",
        "Infosys": "https://www.google.com/finance/quote/INFY:NSE",
        "Tesla": "https://www.google.com/finance/quote/TSLA:NASDAQ",
        "HDFC bank": "https://www.google.com/finance/quote/HDFCBANK:NSE"
        
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
    
    if stock_name == "Tesla":
        employee = 140473
        founded = "Jul 1, 2003"
        ceo = "Elon Musk"
        return employee, founded, ceo
    
    ceo = information[9]
    founded = information[10]
    employee = information[12]
    
    
    
    return ceo, founded, employee
    
    
    
    

# get stock price
def get_stock_price(stock_name):
    stock_urls = {
        "TCS": "https://www.google.com/finance/quote/TCS:NSE",
        "BlackRock": "https://www.google.com/finance/quote/BLK:NYSE",
        "Meta": "https://www.google.com/finance/quote/META:NASDAQ",
        "Google": "https://www.google.com/finance/quote/GOOG:NASDAQ",
        "Amazon": "https://www.google.com/finance/quote/AMZN:NASDAQ",
        "Nividia": "https://www.google.com/finance/quote/NVDA:NASDAQ",
        "Apple": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "SAP": "https://www.google.com/finance/quote/SAP:ETR",
        "Infosys": "https://www.google.com/finance/quote/INFY:NSE",
        "Tesla": "https://www.google.com/finance/quote/TSLA:NASDAQ",
        "HDFC bank": "https://www.google.com/finance/quote/HDFCBANK:NSE"
        
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
    
    if stock_name in ["TCS", "Infosys", "HDFC bank"]:
        return price, f"{changes_per}%"
    else:  
        return f"$ {price}", f"{changes_per}%" 


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
    elif stock_name == 'Apple':
        container3.caption('''Apple Inc. is a prominent global technology company headquartered in
                           Cupertino, California. Known for its innovative hardware, including the
                           iPhone, iPad, and Mac, Apple also offers a suite of software and services,
                           such as iOS, macOS, and iCloud. Established in 1976, Apple is renowned for
                           its design excellence, user-friendly products, and ecosystem integration,
                           making it a leader in consumer electronics and technology.''')
    
    elif stock_name == 'Infosys':
        container3.caption('''Infosys Limited is a global leader in IT services, consulting, and 
                           business solutions headquartered in Bengaluru, India. Established in 1981,
                           Infosys provides a broad spectrum of services including software development,
                           systems integration, and consulting. Renowned for its innovation in 
                           technology and digital transformation, Infosys serves clients worldwide 
                           and is a major player in the IT services sector.''')
    
    elif stock_name == 'HDFC bank':
        container3.caption('''HDFC Bank Limited is one of India’s leading private-sector banks, 
                           headquartered in Mumbai. Established in 1994, HDFC Bank offers a wide range 
                           of financial products and services including retail and wholesale banking,
                           insurance, and investment services. Known for its customer-centric approach
                           and robust financial services, HDFC Bank is a major player in the Indian 
                           banking sector.''')
    
    elif stock_name == 'Nividia':
        container3.caption('''Nvidia Corporation is a global leader in visual computing technology 
                           headquartered in Santa Clara, California. Founded in 1993, Nvidia is renowned
                           for its graphics processing units (GPUs) and AI hardware, serving markets 
                           from gaming to data centers. The company’s innovations in graphics and
                           artificial intelligence have solidified its position as a major technology
                           driver.''')
     
    elif stock_name == 'Meta':
        container3.caption('''Meta Platforms, Inc. (formerly Facebook) is a leading global technology
                           company headquartered in Menlo Park, California. Established in 2004, Meta 
                           focuses on building social media platforms, virtual reality, and augmented
                           reality technologies. Known for its flagship platforms like Facebook, 
                           Instagram, and WhatsApp, Meta drives innovation in digital communication and
                           connectivity.''')
    
    elif stock_name == 'Amazon':
        container3.caption('''Amazon.com, Inc. is a global e-commerce and technology giant headquartered
                           in Seattle, Washington. Founded in 1994, Amazon offers a vast array of
                           products and services, including online retail, cloud computing (AWS), and
                           digital streaming. Known for its innovation and customer-centric approach, 
                           Amazon is a major player in the global tech and retail industries.''')
    
    elif stock_name == 'Google':
        container3.caption('''Google LLC is a leading technology company headquartered in Mountain View,
                           California. Established in 1998, Google is renowned for its search engine and
                           a wide range of products and services, including advertising, cloud computing,
                           and digital services. Known for its innovation and influence in technology,
                           Google is a major player in the global tech landscape.''')
    
    elif stock_name == 'SAP':
        container3.caption('''SAP SE is a global enterprise software company headquartered in Walldorf,
                           Germany. Founded in 1972, SAP specializes in enterprise resource planning
                           (ERP) software, cloud solutions, and business technology platforms. Renowned
                           for its comprehensive suite of business solutions, SAP supports companies
                           in optimizing operations and driving digital transformation.''')
    
    elif stock_name == 'Tesla':
        container3.caption('''Tesla, Inc. is an American electric vehicle and clean energy company
                           headquartered in Palo Alto, California. Established in 2003, Tesla is known
                           for its innovative electric cars, battery energy storage solutions, and solar
                           energy products. The company’s focus on sustainable energy and cutting-edge
                           technology has made it a major player in the automotive and energy sectors.''')
    
    elif stock_name == 'BlackRock':
        container3.caption('''BlackRock, Inc. is a global investment management firm headquartered in
                           New York City. Founded in 1988, BlackRock provides a range of investment and
                           risk management services to institutional and individual investors. Known for
                           its expertise in asset management and financial technology, BlackRock is a 
                           leading player in the global investment industry.''')                                         
    

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
        

def refresh_app():
    st.rerun()


def main():
    page_title()
    # Initialize the session state for metrics and interval
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 0
    if 'stock_exchang' not in st.session_state:
        st.session_state.stock_exchang = 0
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    if 'interval' not in st.session_state:
        st.session_state.interval = 'Year'    
        
    stock_name = st.selectbox("Select a stock", ["TCS", "Apple", "Infosys", "HDFC bank", "Nividia", "Meta", "Amazon", "Google", "SAP", "Tesla", "BlackRock"], on_change=refresh_app)    
    interval = st.session_state.interval    
    
    if st.button("Refresh"):
        update_metrics(stock_name)
        st.session_state.last_refresh = time.time()
        st.rerun()
    
    st.caption("Please hit refresh button to get the latest data")    
    
    col1 , col2 = st.columns([1,4])
    with col1:
        container1 = st.container(border=True)    
        container1.metric(label=f"{stock_name}", value=st.session_state.stock_price, delta=st.session_state.stock_exchang)
    with col2:
        container2 = st.container(border=True)
        with container2:
            col8, col9 = st.columns([1,4.4])
            with col8:
                st.markdown(f"{stock_name}")
                download_data(stock_name)
            with col9:
                st.write(f''' Click the download button below to download the {stock_name} stock data in CSV format
                         for your analysis''')      
                st.caption("Note: Stock data last updated on 09/08/2024")            
                 
            
    
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
        st.rerun()    
 


main()        