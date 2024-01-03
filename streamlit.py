import streamlit as st
import requests
import json

st.title('RAG AI')

# Backend service URLs
CHAT_URL = 'http://localhost:5000/chat'
UPLOAD_PDF_URL = 'http://localhost:5000/upload_pdf'
INDEX_YOUTUBE_URL = 'http://localhost:5000/index_youtube'
INDEX_WEBPAGE_URL = 'http://localhost:5000/index_webpage'
UPDATE_DOCUMENT_URL = 'http://localhost:5000/update_document'
LIST_DOCUMENTS = 'http://localhost:5000/list_documents'
DELETE_DOCUMENT_URL = 'http://localhost:5000/delete_document'

menu = st.sidebar.radio("Choose a feature", 
    ("Chat your Data", "Upload PDF", "Index YouTube Video", "Index Web Content", "Update Document", "List Documents", "Delete Document"))

if menu == "Chat your Data":
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Type your message here:")

    if user_input:
        # Update chat history with the user's message
        st.session_state.chat_history.append({'author': 'user', 'message': user_input})

        with st.spinner('Generating a response...'):
            # Send the message to Flask backend and get the response
            response = requests.post(CHAT_URL, json={"message": user_input})
            if response.status_code == 200:
                answer = response.json().get('response', 'No response')
                st.session_state.chat_history.append({'author': 'assistant', 'message': answer})
            else:
                st.session_state.chat_history.append({'author': 'assistant', 'message': 'Error in processing request'})

    for chat in st.session_state.chat_history:
        with st.chat_message(chat['author']):
            st.write(chat['message'])

elif menu == "Upload PDF":
    uploaded_pdf = st.file_uploader("Choose a PDF file:", type="pdf")
    if st.button('Upload and Process PDF'):
        if uploaded_pdf is not None:
            files = {'file': uploaded_pdf.getvalue()}
            response = requests.post(UPLOAD_PDF_URL, files=files)
            if response.status_code == 200:
                st.success('PDF processed successfully')
            else:
                st.error('Error in processing PDF')

elif menu == "Index YouTube Video":
    youtube_url = st.text_input("Enter a YouTube Video URL:")
    if st.button('Process Audio'):
        if youtube_url:
            response = requests.post(INDEX_YOUTUBE_URL, json={'url': youtube_url})
            if response.status_code == 200:
                st.success('YouTube video indexed successfully')
            else:
                st.error('Error in processing YouTube video')

elif menu == "Index Web Content":
    webpage_url = st.text_input("Enter a Web Page URL:")
    if st.button('Extract Content'):
        if webpage_url:
            response = requests.post(INDEX_WEBPAGE_URL, json={'url': webpage_url})
            if response.status_code == 200:
                st.success('Web content extracted successfully')
            else:
                st.error('Error in extracting web content')

# Update Document
if menu == "Update Document":
    doc_id = st.text_input('Document ID to Update:')
    new_content = st.text_area('New Content for Document:')
    if st.button('Update Document'):
        response = requests.post(UPDATE_DOCUMENT_URL, json={"id": doc_id, "content": new_content})
        if response.status_code == 200:
            st.success('Document updated successfully.')
        else:
            st.error('Error updating document.')

if menu == "List Documents":
    response = requests.get(LIST_DOCUMENTS)
    if response.status_code == 200:
        document_ids = response.json().get('document_ids', [])
        st.write("Document IDs:")
        for doc_id in document_ids:
            st.write(doc_id)
    else:
        st.error('Error retrieving document list.')

# Delete Document
elif menu == "Delete Document":
    doc_id = st.text_input('Document ID to Delete:')
    if st.button('Delete Document'):
        response = requests.post(DELETE_DOCUMENT_URL, json={"id": doc_id})
        if response.status_code == 200:
            st.success('Document deleted successfully.')
        else:
            st.error('Error deleting document.')