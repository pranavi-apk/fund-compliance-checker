"""
Main compliance checker module that orchestrates the entire checking process.
"""
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from colorama import Fore, Style, init

from .pdf_parser import PDFParser, DocumentChunk
from .vector_store import VectorStore
from .llm_analyzer import ComplianceLLM


init(autoreset=True)  # Initialize colorama


@dataclass
class ComplianceViolation:
    """Represents a compliance violation finding."""
    severity: str
    check_type: str
    issue: str
    location_page: int
    location_text: str
    regulation_citation: str
    explanation: str
    retrieved_context: List[str]


class ComplianceChecker:
    """Main compliance checker orchestrating all components."""
    
    def __init__(self, regulatory_pdfs: List[str], 
                 embedding_model: str = 'all-MiniLM-L6-v2',
                 llm_model: str = 'llama3.2'):
        """
        Initialize compliance checker.
        
        Args:
            regulatory_pdfs: List of paths to regulatory PDF documents
            embedding_model: Name of sentence-transformer model
            llm_model: Name of Ollama model
        """
        self.parser = PDFParser(chunk_size=1000, overlap=200)
        self.vector_store = VectorStore(model_name=embedding_model)
        self.llm = ComplianceLLM(model_name=llm_model)
        self.regulatory_pdfs = regulatory_pdfs
        
        # Define compliance checks to perform
        self.compliance_checks = [
            {
                'type': 'fee_disclosure',
                'query': 'management fees performance fees expenses charges fee structure calculation',
                'description': 'Fee Disclosure Completeness'
            },
            {
                'type': 'risk_disclosure',
                'query': 'risk factors market risk liquidity risk currency risk investment risks',
                'description': 'Risk Disclosure Requirements'
            },
            {
                'type': 'concentration_limits',
                'query': 'investment restrictions concentration limits single issuer exposure diversification',
                'description': 'Investment Concentration Limits'
            }
        ]
    
    def build_knowledge_base(self, cache_path: Optional[str] = None):
        """
        Build or load the regulatory knowledge base.
        
        Args:
            cache_path: Path to cached vector store (if exists)
        """
        if cache_path and os.path.exists(cache_path):
            print(f"{Fore.CYAN}Loading cached knowledge base from {cache_path}...")
            self.vector_store.load(cache_path)
            return
        
        print(f"{Fore.CYAN}Building regulatory knowledge base...")
        
        for pdf_path in self.regulatory_pdfs:
            print(f"{Fore.YELLOW}Processing: {os.path.basename(pdf_path)}")
            chunks = self.parser.parse_document(pdf_path)
            self.vector_store.add_documents(chunks)
        
        if cache_path:
            self.vector_store.save(cache_path)
    
    def check_prospectus(self, prospectus_path: str) -> List[ComplianceViolation]:
        """
        Check a prospectus for compliance violations.
        
        Args:
            prospectus_path: Path to prospectus PDF
            
        Returns:
            List of ComplianceViolation objects
        """
        print(f"\n{Fore.CYAN}Analyzing prospectus: {os.path.basename(prospectus_path)}")
        
        # Parse prospectus
        print(f"{Fore.YELLOW}Extracting text from prospectus...")
        prospectus_chunks = self.parser.parse_document(prospectus_path)
        
        violations = []
        
        # Perform each type of compliance check
        for check in self.compliance_checks:
            print(f"\n{Fore.MAGENTA}Running check: {check['description']}")
            
            # Search for relevant prospectus sections
            prospectus_results = self._search_in_chunks(
                prospectus_chunks, 
                check['query'], 
                top_k=3
            )
            
            for chunk, score in prospectus_results:
                # Retrieve relevant regulatory context
                regulatory_context = self.vector_store.search(
                    check['query'], 
                    top_k=3
                )
                
                context_texts = [c.text for c, s in regulatory_context]
                
                # Analyze with LLM
                result = self.llm.check_compliance(
                    prospectus_text=chunk.text,
                    regulatory_context=context_texts,
                    check_type=check['type']
                )
                
                # If violation found, add to results
                if result.get('violation_found', False):
                    violation = ComplianceViolation(
                        severity=result['severity'],
                        check_type=check['description'],
                        issue=result['issue'],
                        location_page=chunk.page_number,
                        location_text=chunk.text[:200] + '...',
                        regulation_citation=result['regulation_citation'],
                        explanation=result['explanation'],
                        retrieved_context=context_texts
                    )
                    violations.append(violation)
                    print(f"{Fore.RED}  ⚠ Violation found on page {chunk.page_number}")
        
        return violations
    
    def _search_in_chunks(self, chunks: List[DocumentChunk], 
                         query: str, top_k: int = 3) -> List[tuple]:
        """Search within a list of chunks using embedding similarity."""
        if not chunks:
            return []
        
        # Create temporary vector store for these chunks
        temp_store = VectorStore(model_name='all-MiniLM-L6-v2')
        temp_store.embedding_model = self.vector_store.embedding_model  # Reuse model
        temp_store.add_documents(chunks)
        
        return temp_store.search(query, top_k=top_k)
    
    def generate_report(self, prospectus_path: str, 
                       violations: List[ComplianceViolation]) -> str:
        """
        Generate a formatted compliance report.
        
        Args:
            prospectus_path: Path to the checked prospectus
            violations: List of violations found
            
        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("COMPLIANCE CHECK REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Document: {os.path.basename(prospectus_path)}")
        
        reg_names = [os.path.basename(p) for p in self.regulatory_pdfs]
        report_lines.append(f"Checked against: {', '.join(reg_names)}")
        report_lines.append("")
        report_lines.append(f"VIOLATIONS FOUND: {len(violations)}")
        report_lines.append("=" * 80)
        
        if not violations:
            report_lines.append("\n✓ No compliance violations detected.")
            report_lines.append("\nNote: This is an automated check and should be reviewed by compliance professionals.")
        else:
            for i, v in enumerate(violations, 1):
                report_lines.append(f"\n[{v.severity}] {v.check_type}")
                report_lines.append(f"Location: Page {v.location_page}")
                report_lines.append(f"Issue: {v.issue}")
                report_lines.append(f"Regulation: {v.regulation_citation}")
                report_lines.append(f"Explanation: {v.explanation}")
                report_lines.append(f"\nProspectus Context:")
                report_lines.append(f"  {v.location_text}")
                report_lines.append(f"\nRelevant Regulatory Text:")
                for j, context in enumerate(v.retrieved_context[:2], 1):
                    preview = context[:300].replace('\n', ' ')
                    report_lines.append(f"  [{j}] {preview}...")
                report_lines.append("\n" + "-" * 80)
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
