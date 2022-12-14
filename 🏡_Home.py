import streamlit as st
import time
import logging
from json import JSONDecodeError
from PIL import Image
from markdown import markdown
from annotated_text import annotation
from utils.haystack import query
from utils.frontend import reset_results, set_state_if_absent, build_sidebar

def create_answer_objects(predictions):
    results = []
    for answer in predictions:
        answer = answer.to_dict()
        if answer["answer"]:
            results.append(
                {
                    "context": "..." + answer["context"] + "...",
                    "answer": answer["answer"],
                    "relevance": round(answer["score"] * 100, 2),
                    "offset_start_in_doc": answer["offsets_in_document"][0]["start"],
                }
            )
        else:
            results.append(
                {
                    "context": None,
                    "answer": None,
                    "relevance": round(answer["score"] * 100, 2),
                }
            )
    return results


build_sidebar()

set_state_if_absent("statement", "What is the fastest animal?")
set_state_if_absent("results", None)

st.write("# Search for animals at Lisbon Zoo with MultiModalRetrieval π")
st.markdown(
    "**Disclaimer**: This demo will produce odd results if the Lisbon Zoo "
    "[does not have said animal](https://zooinstitutes.com/zooinstitutes/lisbon-zoo-518.html?id_type=2) π - "
    "Stay tuned for improvements"
)
st.markdown(
    """
##### Ask a question about animals in the Lisbon Zoo:
To learn more about this demo, check out the β­οΈ Info section
"""
)
# Search bar
statement = st.text_input(
    "", value=st.session_state.statement, max_chars=100, on_change=reset_results
)

run_pressed = st.button("Run")

run_query = (
    run_pressed or statement != st.session_state.statement
)

# Get results for query
if run_query and statement:
    time_start = time.time()
    reset_results()
    st.session_state.statement = statement
    with st.spinner("π πΌπ·π¦ &nbsp;&nbsp; Looking for the right animal"):
        try:
            docs = query(statement)
            for doc in docs["documents"]:
                image = Image.open(doc.content)
                st.image(image)
            st.session_state.results = create_answer_objects(docs["answers"])
            time_end = time.time()
        except JSONDecodeError as je:
            st.error(
                "π &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
            )
            
        except Exception as e:
            logging.exception(e)
            st.error("π &nbsp;&nbsp; An error occurred during the request.")
            

if st.session_state.results:
    st.write('## Why this image?')
    answers = st.session_state.results
    for count, answer in enumerate(answers):
        if answer["answer"]:
            text, context = answer["answer"], answer["context"]
            start_idx = context.find(text)
            end_idx = start_idx + len(text)
            st.write(
                markdown(context[:start_idx] + str(annotation(body=text, label="ANSWER", background="#964448", color='#ffffff')) + context[end_idx:]),
                unsafe_allow_html=True,
            )
            st.markdown(f"**Relevance:** {answer['relevance']}")
        else:
            st.info(
                "π€ &nbsp;&nbsp; Haystack is unsure whether any of the documents contain an answer to your question. Try to reformulate it!"
            )