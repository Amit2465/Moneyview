import streamlit as st



# setting the configuration
st.set_page_config(
    page_title='MoneyView',
    page_icon='💰',
    layout='wide',
    initial_sidebar_state='auto')


# set logo
st.logo("Logo.svg")


# hiding the hamburger menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# removing extra padding
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)




# set pages
p1 = st.Page("pages/Home.py", title="Home", icon=":material/home:")
p2 = st.Page("pages/India.py", title="India", icon=":material/language:")
p3 = st.Page("pages/US.py", title="USA", icon=":material/badge:")
p4 = st.Page("pages/Europe.py", title="Europe", icon=":material/code:")
p5 = st.Page("pages/Stocks.py", title="Stocks", icon=":material/stacked_line_chart:")
p6 = st.Page("pages/Currencies.py", title="Currencies", icon=":material/currency_exchange:")
p7 = st.Page("pages/Crypto.py", title="Crypto", icon=":material/currency_bitcoin:")
p8 = st.Page("pages/Futures.py", title="Futures", icon=":material/online_prediction:")
pg = st.navigation([p1,p2, p3, p4, p5, p6, p7, p8])
pg.run() 



# footer    
st.markdown('</br>', unsafe_allow_html = True)  
st.markdown("""
<style>
    .badge-container {
        display: flex;
        justify-content: center;
    }
    .badge-container a {
        margin: 0 3px;  
    }
</style>
<hr>
<div class="badge-container">
    <a href="https://www.linkedin.com/in/amit-yadav-674a9722b">
        <img src="https://img.shields.io/badge/-LinkedIn-306EA8?style=flat&logo=Linkedin&logoColor=white" alt="LinkedIn">
    </a>
    <a href="https://github.com/Amit2465">
        <img src="https://img.shields.io/badge/-GitHub-2F2F2F?style=flat&logo=github&logoColor=white" alt="GitHub">
    </a>
    <a href="mailto:your.amityadav23461@gmail.com.com">
        <img src="https://img.shields.io/badge/-Email-D14836?style=flat&logo=gmail&logoColor=white" alt="Email">
    </a>
</div>
</br>
<div style="text-align: center;">© 2024 Amit Yadav</div>
""", unsafe_allow_html=True)