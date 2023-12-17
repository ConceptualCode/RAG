from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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