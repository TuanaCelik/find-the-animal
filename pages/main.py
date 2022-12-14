import streamlit as st
from multipage import MultiPage
import time
import logging
from json import JSONDecodeError
from PIL import Image


from utils.haystack import query
from utils.frontend import reset_results, set_state_if_absent
from pages import info, settings

def app():

    set_state_if_absent("statement", "What is the fastest animal?")
    set_state_if_absent("results", None)

    st.write("# Look for images with MultiModalRetrieval 🐅")
    st.write()
    st.markdown(
        """
    ##### Enter a question about animals
    """
    )
    # Search bar
    statement = st.text_input(
        "", value=st.session_state.statement, max_chars=100, on_change=reset_results
    )
        
    col1, col2 = st.columns(2)
    col1.markdown(
        "<style>.stButton button {width:100%;}</style>", unsafe_allow_html=True
    )
   
    run_pressed = col1.button("Run")

    run_query = (
        run_pressed or statement != st.session_state.statement
    )

    # Get results for query
    if run_query and statement:
        time_start = time.time()
        reset_results()
        st.session_state.statement = statement
        with st.spinner("🔎 🐼🐷🦊 &nbsp;&nbsp; Looking for the right animal"):
            try:
                docs = query(statement)
                st.write(docs["documents"])
                for doc in docs["documents"]:
                    image = Image.open(doc.content)
                    st.image(image)
                for answer in docs["answers"]:
                    st.write(answer)
                print(f"S: {statement}")
                time_end = time.time()
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                print(f"elapsed time: {time_end - time_start}")
            except JSONDecodeError as je:
                st.error(
                    "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
                )
                return
            except Exception as e:
                logging.exception(e)
                st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
            return
    
    # if st.session_state.results:
    #     st.write("Got some results")
    #     print("GOT RESTULTS")
        # st.write("Received Results")
        # results = st.session_state.results
        # print(results)
        # docs = results["documents"]
        # st.write(results)
        # # show different messages depending on entailment results
        # for doc in docs:
        #     image = Image(filename=doc.content)
        #     st.image(image)