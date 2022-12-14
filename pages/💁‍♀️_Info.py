import streamlit as st

st.markdown("""
# Better Image Retrieval With Reinforced CLIP 🧠


CLIP is a neural network trained on image-text pairs that can predict how semantically close images are with some text
But, although CLIP understands what it sees, it doesn't know its properties. While other models can understand text that contains such information, like Wikipedia.

In this demo application, we see if we can 'help' CLIP by reinforcing it with another model.""")

st.image("diagram.png")