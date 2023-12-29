import streamlit as st
from utils import DocumentLoader, DocumentSplitter
from vector_store import initialize_vector_store
from conversational_retrieval import create_conversational_chain
from chat_model import initialize_chat_model
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

vectordb = initialize_vector_store()
llm = initialize_chat_model()
conversational_qa_chain = create_conversational_chain(llm, vectordb)
document_loader = DocumentLoader()
document_splitter = DocumentSplitter()

st.title('ChatFlex AI')

menu = st.sidebar.radio("Choose a feature", 
    ("Chat your Data", "Upload PDF", "Index YouTube Video", "Index Web Content"))

if menu == "Chat your Data":
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Type your message here:")

    if user_input:
        st.session_state.chat_history.append({'author': 'user', 'message': user_input})

        response_obj = conversational_qa_chain({"question": user_input})
        response = response_obj.get("answer", "No answer found.")
        st.session_state.chat_history.append({'author': 'assistant', 'message': response})
    
    for chat in st.session_state.chat_history:
        with st.chat_message(chat['author']):
            st.write(chat['message'])

# PDF Upload
elif menu == "Upload PDF":
    uploaded_pdf = st.file_uploader("Choose a PDF file:", type="pdf", key="pdf_uploader")
    if uploaded_pdf is not None:
        pdf_docs = document_loader.load_pdf(uploaded_pdf)
        pdf_chunks = document_splitter.split_document(pdf_docs)
    if st.button('Index Documents'):
        document_loader.index_documents(pdf_chunks, 'docs/chroma')
        st.success('Documents indexed successfully!')

# YouTube Audio Processing
elif menu == "Index YouTube Video":
    youtube_url = st.text_input("Enter a YouTube Video URL:", key="youtube_input")
    if st.button('Process Audio', key="process_youtube"):
        if youtube_url:
            audio_content = document_loader.load_from_youtube(youtube_url)
            audio_chunks = document_splitter.split_document(audio_content)
            document_loader.index_documents(audio_chunks, 'docs/chroma')
            st.success('Documents indexed successfully!')
            st.text_area('Processed Audio Content:', audio_chunks, height=150)
        else:
            st.warning("Please enter a YouTube video URL.")

# Webpage Content Extraction
elif menu == "Index Web Content":
    webpage_url = st.text_input("Enter a Web Page URL:", key="webpage_input")
    if st.button('Extract Content', key="extract_webpage"):
        if webpage_url:
            web_content = document_loader.load_from_web(webpage_url)
            web_chunks = document_splitter.split_document(web_content)
            document_loader.index_documents(web_chunks, 'docs/chroma')
            st.success('Documents indexed successfully!')
            st.text_area('Extracted Web Content:', web_content, height=150)
        else:
            st.warning("Please enter a web page URL.")