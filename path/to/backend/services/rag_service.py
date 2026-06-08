import os
import logging
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    Docx2txtLoader,
    CSVLoader,
    ExcelLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.chain = None
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = ChatOllama(model="llama3", temperature=0.0)
        
        # Initialize the vector store if it exists
        self._init_vectorstore()
    
    def _init_vectorstore(self):
        """Initialize vector store from existing data"""
        try:
            if os.path.exists("vectorstore"):
                self.vectorstore = FAISS.load_local(
                    "vectorstore", 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
                self.retriever = self.vectorstore.as_retriever()
                logger.info("Vector store loaded successfully")
            else:
                logger.info("No existing vector store found")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
    
    def _load_document(self, file_path: str):
        """Load document based on file extension"""
        try:
            if file_path.endswith('.txt'):
                loader = TextLoader(file_path)
            elif file_path.endswith('.pdf'):
                loader = PDFMinerLoader(file_path)
            elif file_path.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            elif file_path.endswith('.csv'):
                loader = CSVLoader(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                loader = ExcelLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    def _split_documents(self, documents):
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        return text_splitter.split_documents(documents)
    
    def process_documents(self, file_paths: List[str]):
        """Process multiple documents and build vector store"""
        try:
            all_documents = []
            
            for file_path in file_paths:
                logger.info(f"Processing {file_path}")
                documents = self._load_document(file_path)
                all_documents.extend(documents)
            
            # Split documents
            chunks = self._split_documents(all_documents)
            
            # Create vector store
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            else:
                self.vectorstore.add_documents(chunks)
            
            # Save vector store
            self.vectorstore.save_local("vectorstore")
            
            # Create retriever
            self.retriever = self.vectorstore.as_retriever()
            
            # Create RAG chain with strict prompt
            self._create_rag_chain()
            
            logger.info(f"Successfully processed {len(file_paths)} documents")
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise
    
    def _create_rag_chain(self):
        """Create a strict RAG chain that avoids hallucinations"""
        # Strict prompt to avoid hallucinations
        prompt_template = """
        You are an expert assistant with access to specific document information.
        Only answer questions based on the provided context. If the answer is not 
        explicitly stated in the context, respond with: "I don't have enough information 
        to answer this question based on the provided documents."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate.from_template(prompt_template)
        
        # Create chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def query(self, question: str) -> str:
        """Query the RAG system"""
        try:
            if not self.chain:
                return "No documents processed yet. Please upload documents first."
            
            # Get answer from chain
            answer = self.chain.invoke(question)
            
            # Add a safety check to ensure we don't hallucinate
            if "I don't have enough information" in answer.lower():
                return "I don't have enough information to answer this question based on the provided documents."
            
            return answer
            
        except Exception as e:
            logger.error(f"Error during query: {str(e)}")
            return f"An error occurred while processing your query: {str(e)}"
