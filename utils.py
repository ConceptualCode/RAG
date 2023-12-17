from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders import WebBaseLoader

class DocumentProcessor:
    def __init__(self, chunk_size=100, chunk_overlap=20):
        """
        Initializes the DocumentProcessor with a RecursiveTextSplitter.

        Args:
        chunk_size (int): Maximum size of each text chunk.
        chunk_overlap (int): Number of characters of overlap between chunks.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def load_and_split_pdf(self, file_path):
        """
        Loads a PDF file using langchain's PyPDFLoader and splits it into chunks using RecursiveTextSplitter.

        Args:
        file_path (str): Path to the PDF file.

        Returns:
        list: A list of text chunks from the PDF file.
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load() 

        # Split the document into chunks
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def load_from_youtube(self, video_url, save_dir='youtube'):
        """
        Loads and processes audio from a YouTube video.

        Args:
        video_url (str): URL of the YouTube video.
        save_dir (str): Directory to save audio files.

        Returns:
        str: Transcribed text content from the YouTube video.
        """
        youtube_loader = YoutubeAudioLoader([video_url], save_dir)
        parser = OpenAIWhisperParser() 
        loader = GenericLoader(youtube_loader, parser)
        docs = loader.load()
        return ' '.join([doc.page_content for doc in docs])
    
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