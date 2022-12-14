import streamlit as st
from utils.frontend import build_sidebar

st.set_page_config(page_title="Settings", page_icon="⚙️")
build_sidebar()
st.write("This is the settings page")