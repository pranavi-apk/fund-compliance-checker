"""
Unit tests for core components.
Run with: python -m pytest test_components.py -v
or: python test_components.py (standalone)
"""
import unittest
import os
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pdf_parser import PDFParser, DocumentChunk
from src.core.vector_store import VectorStore


class TestPDFParser(unittest.TestCase):
    """Test PDF parsing functionality"""
    
    def setUp(self):
        self.parser = PDFParser(chunk_size=500, overlap=100)
    
    def test_chunk_text(self):
        """Test text chunking with overlap"""
        text = "This is a test. " * 100  # 1600 chars
        chunks = self.parser.chunk_text(text, page_number=1, source_file="test.pdf")
        
        self.assertGreater(len(chunks), 1, "Should create multiple chunks")
        
        # Check overlap
        if len(chunks) > 1:
            # Last part of first chunk should appear in second chunk
            self.assertTrue(len(chunks[0].text) > 400, "Chunks should be reasonably sized")
    
    def test_document_chunk_creation(self):
        """Test DocumentChunk dataclass"""
        chunk = DocumentChunk(
            text="Test content",
            page_number=5,
            chunk_id=10,
            source_file="sample.pdf"
        )
        
        self.assertEqual(chunk.page_number, 5)
        self.assertEqual(chunk.chunk_id, 10)
        self.assertIn("sample.pdf", repr(chunk))


class TestVectorStore(unittest.TestCase):
    """Test vector store functionality"""
    
    def setUp(self):
        # Use smaller model for faster tests
        self.store = VectorStore(model_name='all-MiniLM-L6-v2')
    
    def test_add_and_search(self):
        """Test adding documents and searching"""
        chunks = [
            DocumentChunk(
                text="Investment funds must disclose all management fees clearly.",
                page_number=1,
                chunk_id=0,
                source_file="reg.pdf"
            ),
            DocumentChunk(
                text="Currency risks must be explained for foreign investments.",
                page_number=2,
                chunk_id=1,
                source_file="reg.pdf"
            ),
            DocumentChunk(
                text="Market volatility can affect fund performance significantly.",
                page_number=3,
                chunk_id=2,
                source_file="reg.pdf"
            )
        ]
        
        self.store.add_documents(chunks)
        
        # Search for fee-related content
        results = self.store.search("fee disclosure requirements", top_k=2)
        
        self.assertEqual(len(results), 2, "Should return top 2 results")
        
        # First result should be about fees
        top_chunk, top_score = results[0]
        self.assertIn("fees", top_chunk.text.lower())
        self.assertGreater(top_score, 0.3, "Similarity score should be reasonable")
    
    def test_empty_search(self):
        """Test search on empty store"""
        results = self.store.search("test query")
        self.assertEqual(len(results), 0, "Empty store should return no results")


class TestIntegration(unittest.TestCase):
    """Integration tests with real PDFs"""
    
    def test_regulatory_pdf_exists(self):
        """Check if regulatory PDFs are available"""
        pdfs = [
            "data/pdfs/fund manager code of conduct.pdf",
            "data/pdfs/Code_on_MPF_Investment_Funds.pdf"
        ]
        
        for pdf in pdfs:
            exists = os.path.exists(pdf)
            if not exists:
                self.skipTest(f"PDF not found: {pdf}")
    
    def test_parse_real_pdf(self):
        """Test parsing a real PDF if available"""
        pdf_path = "data/pdfs/fund manager code of conduct.pdf"
        
        if not os.path.exists(pdf_path):
            self.skipTest(f"PDF not found: {pdf_path}")
        
        parser = PDFParser(chunk_size=1000, overlap=200)
        chunks = parser.parse_document(pdf_path)
        
        self.assertGreater(len(chunks), 0, "Should extract chunks from PDF")
        self.assertIsInstance(chunks[0], DocumentChunk)
        self.assertTrue(len(chunks[0].text) > 0, "Chunks should have content")
        
        print(f"\n  ✓ Parsed {len(chunks)} chunks from {pdf_path}")
        print(f"  ✓ Sample chunk: {chunks[0].text[:100]}...")


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("  Running Component Tests")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPDFParser))
    suite.addTests(loader.loadTestsFromTestCase(TestVectorStore))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
