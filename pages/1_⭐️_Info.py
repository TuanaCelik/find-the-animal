import streamlit as st
from utils.frontend import build_sidebar

build_sidebar()

st.markdown("""
# Better Image Retrieval With Retrieval-Augmented CLIP 🧠


CLIP is a neural network trained on image-text pairs that can predict how semantically close images are with some text
But, although CLIP understands what it sees, it doesn't know its properties. While other models can understand text that contains such information, like Wikipedia.

In this demo application, we see if we can 'help' CLIP with another model.""")

st.image("diagram.png")