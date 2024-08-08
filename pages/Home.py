import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_extras.colored_header import colored_header



def custom_css_box(text):    
    custom_css = f"""
    <style>
        .custom-box {{
            background-color:#262730;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
    """
    # Display the custom-styled box with content
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="custom-box">{text}</div>', unsafe_allow_html=True)    

    
    

def load_image(filepath : str):
    with open(filepath, 'r') as f:
        return json.load(f)
    

def page_title(text):
    colored_header(
        label=f"{text}",
        description=None,
        color_name="violet-70",
    )    
   


def main():
    st.title("Welcome to the Moneyview")
    custom_css_box('''Explore real-time financial markets with our comprehensive web app. Whether you're
                tracking stocks, futures, or market trends across India, the US, or Europe, we've got
                you covered. Stay informed with up-to-the-minute data on stock prices, futures contracts,
                and global market indices, all conveniently accessible in one place.''') 
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('</br>', unsafe_allow_html=True)




    col1, col2 ,col3 = st.columns([2,0.2,1])
    with col1:
        page_title("Stocks")
        st.markdown('</br>', unsafe_allow_html=True)
        st.write('''Monitor the latest movements in stock prices from leading exchanges around the globe. Gain detailed
                 insights into individual company stocks, helping you stay informed about 
                 market trends and performance.''')
    with col3:
        phone = load_image('images/Phone_image.json')
        st_lottie(
            phone,
            speed=1,
            loop=True,
            width=270,
            height=270,
        )
        

    col4, col5 ,col6 = st.columns([2,0.2,1])
    with col4:
        page_title("Cryptocurrency")
        st.markdown('</br>', unsafe_allow_html=True)
        st.write('''Stay up-to-date with the latest cryptocurrency prices. Track the value of Bitcoin,
                    Ethereum, and other major cryptocurrencies, enabling you to follow market trends and
                    identify potential investment opportunities in the growing digital asset space.''')
    with col6:
        crypto = load_image('images/crypto.json')
        st_lottie(
            crypto,
            speed=1,
            loop=True,
            width=270,
            height=300,
        )


    col7, col8 ,col9 = st.columns([2,0.2,1])
    with col7:
        page_title("Global Market Indices")
        st.markdown('</br>', unsafe_allow_html=True)
        st.write('''Keep tabs on key indices from major markets in India, the US, and Europe. 
                    Our platform allows you to track indices such as the Nifty 50, S&P 500, and FTSE 100,
                    providing a comprehensive overview of overall market sentiment and direction.''')
    with col9:
        globalM = load_image('images/global.json')
        st_lottie(
            globalM,
            speed=1,
            loop=True,
            width=270,
            height=300,
        ) 
      
main()  