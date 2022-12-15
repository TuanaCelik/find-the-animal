import shutil
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes.retriever import EmbeddingRetriever, MultiModalRetriever
from haystack.nodes.reader import FARMReader
from haystack import Pipeline
from utils.config import (INDEX_DIR)
from typing import List
from haystack import BaseComponent, Answer
import streamlit as st



class AnswerToQuery(BaseComponent):

  outgoing_edges = 1

  def run(self, query: str, answers: List[Answer]):
    return {"query": answers[0].answer}, "output_1"

  def run_batch(self):
    raise NotImplementedError()

# cached to make index and models load only at start
@st.cache(
    hash_funcs={"builtins.SwigPyObject": lambda _: None}, allow_output_mutation=True
)
def start_haystack():
    """
    load document store, retrievers for images and text, reader and create pipeline
    """
    shutil.copy(f"{INDEX_DIR}/text.db", ".")
    shutil.copy(f"{INDEX_DIR}/images.db", ".")

    document_store_text = FAISSDocumentStore(
        faiss_index_path=f"{INDEX_DIR}/text.faiss",
        faiss_config_path=f"{INDEX_DIR}/text.json",
    )
    
    document_store_images = FAISSDocumentStore(
        faiss_index_path=f"{INDEX_DIR}/images.faiss",
        faiss_config_path=f"{INDEX_DIR}/images.json",
    )

    retriever_text = EmbeddingRetriever(
        document_store=document_store_text,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
    )

    reader = FARMReader(model_name_or_path="deepset/deberta-v3-base-squad2", use_gpu=True)
    

    retriever_images = MultiModalRetriever(
        document_store=document_store_images,
        query_embedding_model = "sentence-transformers/clip-ViT-B-32",
        query_type="text",
        document_embedding_models = {
            "image": "sentence-transformers/clip-ViT-B-32"
        }
    )
    
    answer_to_query = AnswerToQuery()

    pipe = Pipeline()

    pipe.add_node(retriever_text, name="text_retriever", inputs=["Query"])
    pipe.add_node(reader, name="text_reader", inputs=["text_retriever"])
    pipe.add_node(answer_to_query, name="answer2query", inputs=["text_reader"])
    pipe.add_node(retriever_images, name="image_retriever", inputs=["answer2query"])

    return pipe
    
pipe = start_haystack()

@st.cache(allow_output_mutation=True)
def query(statement: str, text_reader_top_k: int = 5):
    """Run query"""
    params = {"text_reader": {"top_k": text_reader_top_k},"image_retriever": {"top_k": 1},"text_retriever": {"top_k": 5} }
    results = pipe.run(statement, params=params)
    return results