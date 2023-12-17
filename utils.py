from langchain.document_loaders import PyPDFLoader, YoutubeAudioLoader, WebBaseLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentLoader:
    def __init__(self):
        """
        Initializes the DocumentLoader.
        """
        pass

    def load_pdf(self, file_path):
        """
        Loads a PDF file using langchain's PyPDFLoader.

        Args:
        file_path (str): Path to the PDF file.

        Returns:
        list: A list of Documents from the PDF file.
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
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
        return self.text_splitter.split_text(document)