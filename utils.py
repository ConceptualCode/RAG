from langchain.document_loaders import PyPDFLoader, YoutubeAudioLoader, WebBaseLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import tempfile


class DocumentLoader:
    def __init__(self):
        """
        Initializes the DocumentLoader.
        """
        pass

    def load_pdf(self, uploaded_file):
        """
        Loads a PDF file using langchain's PyPDFLoader.

        Args:
        file_path (str): Path to the PDF file.

        Returns:
        list: A list of Documents from the PDF file.
        """
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name

        # Load the PDF using PyPDFLoader
        loaders = [PyPDFLoader(temp_file_path)]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        os.remove(temp_file_path)

        return docs



    
    def load_from_youtube(self, video_url, save_dir='youtube'):
        """
        Loads and processes audio from a YouTube video.

        Args:
        video_url (str): URL of the YouTube video.
        save_dir (str): Directory to save audio files.

        Returns:
        list: Transcribed text content from the YouTube video.
        """
        youtube_loader = YoutubeAudioLoader([video_url], save_dir)
        parser = OpenAIWhisperParser()
        loader = GenericLoader(youtube_loader, parser)
        docs = loader.load()
        return docs
    
    def load_from_web(self, url):
        """
        Loads and extracts text from a web page.

        Args:
        url (str): URL of the web page.

        Returns:
        str: Extracted text content from the web page.
        """
        web_loader = WebBaseLoader(web_path=url)
        text = web_loader.load()
        return text
    

    def index_documents(self, documents, persist_directory):
        """
        Indexes a list of documents into the Chroma vector store.

        Args:
        vectordb (Chroma): The Chroma vector store instance.
        documents (list): List of document texts to index.

        Returns:
        db
        """
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=persist_directory)
        return db


class DocumentSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", ". ", " ", ""]):
        """
        Initializes the DocumentSplitter with a RecursiveTextSplitter.

        Args:
        chunk_size (int): Maximum size of each text chunk.
        chunk_overlap (int): Number of characters of overlap between chunks.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                            chunk_overlap=chunk_overlap, 
                                                            separators=separators)

    def split_document(self, document):
        """
        Splits the document into chunks using RecursiveTextSplitter.

        Args:
        document (str): The document to be split.

        Returns:
        list: A list of text chunks.
        """
        return self.text_splitter.split_documents(document)