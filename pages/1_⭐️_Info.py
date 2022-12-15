import streamlit as st
from utils.frontend import build_sidebar

build_sidebar()

st.markdown("""
# Better Image Retrieval With Retrieval-Augmented CLIP 🧠


[CLIP](https://openai.com/blog/clip/) is a neural network that can predict how semantically close images and text pairs are. 
In simpler terms, it can tell that the string "Cat" is closer to images of cats rather than images of dogs.

What makes CLIP so powerful is that is a zero-shot model: that means that it can generalize concepts,
understand text and images it has never seen before. For example, it can tell that the string "an animal with yellow eyes"
is closer to images of cats rather than dogs, even though such pair was not in its training data.

Why does this matter? Because zero shot capabilities allow models to understand descriptions. And in fact
CLIP understands that "an animal with pink feathers" matches a flamingo better than a pig.

However, these descriptions need to be related to what the image shows. CLIP knows nothing about the animal features, 
history and cultural references: It doesn't know which animals live longer than others, that jaguars were often depicted 
in Aztec wall paintings, or that wolves and bears are typical animals that show up in European fairy tales. It doesn't even 
know that cheetas are fast, because it cannot tell it from the image.

However, Wikipedia contains all this information, and more. Can we make CLIP "look up" the answer to
our questions on Wikipedia before looking for matches?

In this demo application, we see how can we combine traditional Extractive QA on Wikipedia and CLIP with Haystack.""")

st.image("diagram.png")

st.markdown("""
In the image above you can see how the process looks like.

First, we download a slice of Wikipedia with information about all the animals in the Lisbon zoo and preprocess,
index, embed and store them.

At this point they are ready to be queried by the text Retriever, which compares the user's question ("The fastest animal")
to all the documents indexed earlier and returns the documents which are more likely to contain an answer to the question.
In this case, it will probably return snippets from the Cheetah Wikipedia entry.

Once the documents are found, they are handed over to the Reader, a model that is able to locate precisely the answer to a
question into a document. These answers are strings that should be now very easy for CLIP to understand, such as the name of an animal.
In this case, the Reader will return answers such as "Cheetah", "the cheetah", etc.

These strings are then ranked and the most likely one is sent over to CLIP, which will use its own document store of images
to find all the pictures that match the string. Cheetah are present in the Lisbon zoo, so it will find pictures of them and
return them.
""")