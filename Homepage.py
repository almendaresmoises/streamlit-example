import streamlit as st

def app():
    st.title("Home page")
    st.write("Welcome to the Home page!")

st.header('Payments Management System')
st.text("Welcome to the payments management system.")

# hide streamlit menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)