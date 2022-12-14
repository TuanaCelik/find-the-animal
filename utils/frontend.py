import streamlit as st

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def reset_results(*args):
    st.write("Called reset")
    st.session_state.answer = None
    st.session_state.results = None