from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

def initialize_vector_store(persist_directory='docs/chroma/'):
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb
