import streamlit as st

def build_sidebar():
    sidebar = """
    <div style='text-align: center'>
    <p><br/><a href='https://github.com/TuanaCelik/find-the-animal'>Github project</a> - Based on <a href='https://github.com/deepset-ai/haystack'>Haystack</a></p>
    <p>Project by <a href='https://github.com/ZanSara'>Sara Zanzottera</a> and <a href='https://github.com/TuanaCelik'>Tuana Celik</a></p>
    </div>
    """
    st.sidebar.markdown(sidebar, unsafe_allow_html=True)

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def reset_results(*args):
    st.session_state.results = None