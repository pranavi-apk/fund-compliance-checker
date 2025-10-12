# Investment Fund Compliance Checker

A RAG-based system for scanning investment fund prospectuses against Hong Kong regulatory requirements (SFC Fund Manager Code of Conduct and MPF Code on Investment Funds).

**Built for**: Klares.io Application Demonstration  
**Author**: Pranavi Kuntrapakam

---

## 🎯 Project Overview

This prototype demonstrates an AI-powered compliance checking system that:
- Parses regulatory documents and fund prospectuses (PDFs)
- Creates semantic embeddings for intelligent retrieval
- Uses LLM analysis to identify compliance violations
- Generates detailed compliance reports with citations

### Compliance Checks Performed

1. **Fee Disclosure Completeness** - Validates that management fees, performance fees, and expenses are fully disclosed
2. **Risk Disclosure Requirements** - Ensures adequate disclosure of market, liquidity, and currency risks
3. **Investment Concentration Limits** - Checks for proper disclosure of single issuer exposure restrictions

---

## 📋 Prerequisites

### Required Software
- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running

### Required Documents
Place these PDFs in the project directory:

**Regulatory Documents** (Knowledge Base):
- `fund manager code of conduct.pdf` - [SFC Fund Manager Code](https://www.sfc.hk/-/media/EN/assets/components/codes/files-current/web/codes/fund-manager-code-of-conduct/fund-manager-code-of-conduct.pdf)
- `Code_on_MPF_Investment_Funds.pdf` - [MPF Investment Code](https://www.mpfa.org.hk/en/-/media/files/information-centre/legislation-and-regulations/codes/code_on_mpf_investment_funds.pdf)

**Test Prospectuses**:
- `20230504163240_1872.pdf` - E Fund ETF
- `E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf` - ChinaAMC Global ETF
- `blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf` - BlackRock Premier Funds

---

## 🚀 Quick Start

### Step 1: Install Ollama and Pull Model

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/

# Start Ollama service
ollama serve

# In a new terminal, pull the required model
ollama pull llama3.2
```

### Step 2: Set Up Python Environment

```bash
# Make setup script executable
chmod +x setup_venv.sh

# Run setup script
./setup_venv.sh

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Build Knowledge Base (First Time Only)

```bash
# Build regulatory knowledge base and cache it
python main.py --build-kb-only
```

This step takes a few minutes and creates `knowledge_base_cache.json` for faster subsequent runs.

### Step 4: Check a Prospectus

```bash
# Check E Fund ETF prospectus
python main.py --prospectus "20230504163240_1872.pdf"

# Save report to file
python main.py --prospectus "20230504163240_1872.pdf" --output efund_report.txt
```

---

## 📖 Usage Examples

### Basic Compliance Check
```bash
python main.py --prospectus "20230504163240_1872.pdf"
```

### Check with Different Model
```bash
python main.py --prospectus "20230504163240_1872.pdf" --model llama3.1
```

### Rebuild Knowledge Base from Scratch
```bash
python main.py --prospectus "20230504163240_1872.pdf" --no-cache
```

### Save Report to File
```bash
python main.py --prospectus "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf" --output blackrock_report.txt
```

---

## 🏗️ Architecture & Components

### Modular Design

```
compliance/
├── main.py                   # CLI entry point
├── compliance_checker.py     # Main orchestrator
├── pdf_parser.py            # PDF extraction and chunking
├── vector_store.py          # Embedding and semantic search
├── llm_analyzer.py          # LLM-based compliance analysis
├── requirements.txt         # Python dependencies
├── setup_venv.sh           # Environment setup script
└── README.md               # This file
```

### Component Description

1. **PDF Parser** (`pdf_parser.py`)
   - Extracts text from PDFs using pdfplumber
   - Chunks documents with overlap for context preservation
   - Maintains page number references

2. **Vector Store** (`vector_store.py`)
   - Uses sentence-transformers for embeddings
   - Implements cosine similarity search
   - Caches embeddings for performance

3. **LLM Analyzer** (`llm_analyzer.py`)
   - Integrates with Ollama for local LLM inference
   - Structured prompts for compliance analysis
   - Parses responses into violation reports

4. **Compliance Checker** (`compliance_checker.py`)
   - Orchestrates the entire workflow
   - Defines compliance check types
   - Generates formatted reports

---

## 📊 Sample Output

```
================================================================================
COMPLIANCE CHECK REPORT
================================================================================
Document: 20230504163240_1872.pdf
Checked against: fund manager code of conduct.pdf, Code_on_MPF_Investment_Funds.pdf

VIOLATIONS FOUND: 2
================================================================================

[CRITICAL] Fee Disclosure Completeness
Location: Page 15
Issue: Performance fee calculation methodology lacks specific examples
Regulation: SFC FMCC Section 5.1.2 - Fee Structure Disclosure
Explanation: The prospectus mentions performance fees but does not provide 
concrete examples of how they are calculated under different scenarios.

Prospectus Context:
  Performance fees may be charged based on fund performance exceeding benchmark...

Relevant Regulatory Text:
  [1] All fees and charges must be clearly disclosed including calculation 
  methods and worked examples to enable investors to understand...

--------------------------------------------------------------------------------

[WARNING] Risk Disclosure Requirements
Location: Page 23
Issue: Currency hedging risks not adequately disclosed for HKD share class
Regulation: MPF Code Section 4.3 - Currency Risk Disclosure
Explanation: The document mentions currency exposure but does not explain 
hedging strategies or residual risks for the HKD share class.

Prospectus Context:
  The fund may invest in securities denominated in foreign currencies...

Relevant Regulatory Text:
  [1] Funds offering multiple currency share classes must disclose currency 
  conversion risks, hedging strategies, and potential costs...

--------------------------------------------------------------------------------

================================================================================
END OF REPORT
================================================================================
```

---

## 🔧 Customization

### Add New Compliance Checks

Edit `compliance_checker.py` and add to `self.compliance_checks`:

```python
{
    'type': 'your_check_type',
    'query': 'keywords for semantic search',
    'description': 'Human-readable check name'
}
```

Then add corresponding logic in `llm_analyzer.py` → `_build_compliance_prompt()`.

### Adjust Chunk Size

Edit `compliance_checker.py` → `__init__()`:

```python
self.parser = PDFParser(chunk_size=1500, overlap=300)
```

### Use Different Embedding Model

Edit `compliance_checker.py` or pass to constructor:

```python
checker = ComplianceChecker(
    regulatory_pdfs=regulatory_docs,
    embedding_model='all-mpnet-base-v2'  # More accurate but slower
)
```

---

## 🧪 Testing Different Prospectuses

```bash
# E Fund ETF
python main.py --prospectus "20230504163240_1872.pdf"

# ChinaAMC Global ETF
python main.py --prospectus "E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf"

# BlackRock Premier Funds
python main.py --prospectus "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf"
```

---

## ⚠️ Limitations & Disclaimers

- **Prototype System**: This is a demonstration prototype, not production-ready
- **Manual Review Required**: All findings should be reviewed by compliance professionals
- **PDF Quality**: Results depend on PDF text extraction quality
- **LLM Variability**: LLM outputs may vary; use consistent models for reproducibility
- **Regulatory Updates**: Does not track regulatory changes automatically

---

## 🛠️ Troubleshooting

### Ollama Connection Error
```
Error: Could not connect to Ollama
```
**Solution**: Ensure Ollama is running with `ollama serve`

### Model Not Found
```
Error: Model 'llama3.2' not found
```
**Solution**: Pull the model with `ollama pull llama3.2`

### PDF Extraction Issues
```
Error extracting text from PDF
```
**Solution**: Ensure PDF is not scanned image-only. May need OCR preprocessing.

### Memory Issues
```
MemoryError during embedding generation
```
**Solution**: Reduce chunk_size or process documents one at a time

---

## 📚 Dependencies

- **pdfplumber** - PDF text extraction
- **sentence-transformers** - Text embeddings
- **ollama** - Local LLM inference
- **numpy** - Vector operations
- **torch** - Deep learning backend for embeddings
- **colorama** - Colored terminal output
- **tqdm** - Progress bars

---

## 🎓 Technical Highlights for Interview

This project demonstrates:

1. **RAG Architecture**: Semantic search + LLM generation
2. **Modular Design**: Separated concerns for maintainability
3. **Production Awareness**: Caching, error handling, CLI design
4. **Domain Knowledge**: Understanding of regulatory compliance
5. **Practical AI**: Local LLM deployment (Hong Kong context)

---

## 📞 Contact

**Pranavi Kuntrapakam**  
Built for Klares.io Application

---

## 📄 License

This is a demonstration project for application purposes.
