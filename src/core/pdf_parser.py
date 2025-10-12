"""
PDF parsing module for extracting text from regulatory and prospectus documents.
"""
import pdfplumber
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a chunk of text from a PDF document."""
    text: str
    page_number: int
    chunk_id: int
    source_file: str
    
    def __repr__(self):
        preview = self.text[:50].replace('\n', ' ')
        return f"Chunk({self.source_file}, p{self.page_number}, '{preview}...')"


class PDFParser:
    """Parser for extracting and chunking text from PDF documents."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize PDF parser.
        
        Args:
            chunk_size: Target size of each text chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def extract_text_with_pages(self, pdf_path: str) -> List[Tuple[int, str]]:
        """
        Extract text from PDF with page numbers.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of tuples (page_number, page_text)
        """
        pages_text = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        pages_text.append((i + 1, text))
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            
        return pages_text
    
    def chunk_text(self, text: str, page_number: int, source_file: str, 
                   start_chunk_id: int = 0) -> List[DocumentChunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            page_number: Page number this text comes from
            source_file: Source PDF filename
            start_chunk_id: Starting ID for chunks
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0
        chunk_id = start_chunk_id
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence or word boundary
            if end < len(text):
                # Look for period followed by space
                last_period = chunk_text.rfind('. ')
                if last_period > self.chunk_size * 0.5:  # At least 50% through
                    end = start + last_period + 1
                    chunk_text = text[start:end]
                else:
                    # Look for space
                    last_space = chunk_text.rfind(' ')
                    if last_space > 0:
                        end = start + last_space
                        chunk_text = text[start:end]
            
            if chunk_text.strip():
                chunks.append(DocumentChunk(
                    text=chunk_text.strip(),
                    page_number=page_number,
                    chunk_id=chunk_id,
                    source_file=source_file
                ))
                chunk_id += 1
            
            start = end - self.overlap
            if start <= 0:
                start = end
                
        return chunks
    
    def parse_document(self, pdf_path: str) -> List[DocumentChunk]:
        """
        Parse entire PDF document into chunks.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of DocumentChunk objects
        """
        pages_text = self.extract_text_with_pages(pdf_path)
        all_chunks = []
        chunk_id = 0
        
        for page_num, page_text in pages_text:
            chunks = self.chunk_text(
                page_text, 
                page_num, 
                pdf_path.split('/')[-1],
                start_chunk_id=chunk_id
            )
            all_chunks.extend(chunks)
            chunk_id += len(chunks)
        
        return all_chunks
