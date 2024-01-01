from flask import Flask, request, jsonify
from utils import DocumentLoader, DocumentSplitter
from vector_store import initialize_vector_store
from conversational_retrieval import create_conversational_chain
from chat_model import initialize_chat_model
import os
from logger import setup_logging
import openai

setup_logging()
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

vectordb = initialize_vector_store()
llm = initialize_chat_model()
conversational_chain = create_conversational_chain(llm, vectordb)
document_loader = DocumentLoader()
document_splitter = DocumentSplitter()

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response_obj = conversational_chain({"question": user_input})
    response = response_obj.get("answer", "No answer found.")
    return jsonify({'response': response})

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    pdf_docs = document_loader.load_pdf(file)
    pdf_chunks = document_splitter.split_document(pdf_docs)
    index_result = document_loader.index_documents(pdf_chunks, 'docs/chroma')
    return jsonify({'message': 'PDF processed and indexed', 'result': index_result})

@app.route('/index_youtube', methods=['POST'])
def index_youtube():
    youtube_url = request.json.get('url', '')
    audio_content = document_loader.load_from_youtube(youtube_url)
    audio_chunks = document_splitter.split_document(audio_content)
    index_result = document_loader.index_documents(audio_chunks, 'docs/chroma')
    return jsonify({'message': 'YouTube audio processed and indexed', 'result': index_result})

@app.route('/index_webpage', methods=['POST'])
def index_webpage():
    webpage_url = request.json.get('url', '')
    web_content = document_loader.load_from_web(webpage_url)
    web_chunks = document_splitter.split_document(web_content)
    index_result = document_loader.index_documents(web_chunks, 'docs/chroma')
    return jsonify({'message': 'Webpage content extracted and indexed', 'result': index_result})

if __name__ == '__main__':
    app.run(debug=True)
