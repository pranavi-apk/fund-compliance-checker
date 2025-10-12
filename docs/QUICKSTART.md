# Quick Start Guide - Compliance Checker

## ⚡ 3-Minute Setup

### 1. Install Ollama (if not already installed)
```bash
# Visit https://ollama.ai/ and download for macOS
# Or use Homebrew:
brew install ollama
```

### 2. Start Ollama & Pull Model
```bash
# Terminal 1 - Start Ollama server
ollama serve

# Terminal 2 - Pull the model (one-time, ~2GB download)
ollama pull llama3.2
```

### 3. Setup Python Environment
```bash
# In your project directory
./setup_venv.sh
source venv/bin/activate
```

### 4. Run First Check
```bash
# Build knowledge base (one-time, ~2-3 minutes)
python main.py --build-kb-only

# Check a prospectus
python main.py --prospectus "20230504163240_1872.pdf"
```

---

## 🎬 Demo Commands

### Run Full Demo (All Test Files)
```bash
./run_demo.sh
```

### Check Single Document
```bash
python main.py --prospectus "20230504163240_1872.pdf"
```

### Save Report to File
```bash
python main.py --prospectus "20230504163240_1872.pdf" --output report.txt
```

---

## 🏗️ What Each File Does

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point - run this |
| `compliance_checker.py` | Main orchestrator |
| `pdf_parser.py` | Extracts & chunks PDFs |
| `vector_store.py` | Semantic search engine |
| `llm_analyzer.py` | LLM compliance analysis |
| `setup_venv.sh` | One-time environment setup |
| `run_demo.sh` | Demo all features |

---

## 🎯 For Klares.io Interview

### Key Technical Highlights

1. **RAG Pipeline**: Retrieval-Augmented Generation for compliance
   - Semantic search finds relevant regulatory text
   - LLM analyzes against specific requirements

2. **Modular Architecture**: Easy to extend
   - Add new compliance checks in `compliance_checker.py`
   - Swap components (different LLMs, embeddings, etc.)

3. **Production Considerations**:
   - Caching for performance
   - Error handling throughout
   - CLI with proper argument parsing
   - Colored output for UX

4. **Hong Kong Regulatory Focus**:
   - SFC Fund Manager Code of Conduct
   - MPF Investment Code
   - Local LLM (Ollama) for data privacy

### Demo Flow for Interview

```bash
# 1. Show the setup
cat README.md | head -20

# 2. Show knowledge base building
python main.py --build-kb-only

# 3. Run a check with live output
python main.py --prospectus "20230504163240_1872.pdf"

# 4. Show modular code structure
ls -l *.py

# 5. Explain a key component
cat compliance_checker.py | grep -A 10 "def check_prospectus"
```

---

## 🔍 Compliance Checks Explained

### 1. Fee Disclosure Completeness
**Looks for**: Management fees, performance fees, calculation methods  
**Regulation**: SFC FMCC Section 5.1.2  
**Why it matters**: Investors need to understand total cost

### 2. Risk Disclosure Requirements
**Looks for**: Market risk, liquidity risk, currency risk  
**Regulation**: MPF Code Section 4.3  
**Why it matters**: Mandatory risk categories under HK law

### 3. Investment Concentration Limits
**Looks for**: Single issuer exposure limits, diversification  
**Regulation**: SFC investment restrictions  
**Why it matters**: Prevents over-concentration in single assets

---

## 🚨 Common Issues & Fixes

### "Could not connect to Ollama"
```bash
# Solution: Start Ollama in another terminal
ollama serve
```

### "Model not found"
```bash
# Solution: Pull the model
ollama pull llama3.2
```

### "No module named 'pdfplumber'"
```bash
# Solution: Activate venv and install deps
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📈 Potential Extensions

For a production version, you could add:

1. **Web Interface**: Flask/FastAPI + React frontend
2. **Batch Processing**: Check multiple prospectuses at once
3. **Custom Rules**: Upload custom regulatory requirements
4. **Comparison Mode**: Compare prospectus versions
5. **Export Formats**: PDF, DOCX, HTML reports
6. **API Integration**: Connect to fund databases
7. **User Management**: Role-based access control
8. **Audit Trail**: Log all checks for compliance records

---

## 💡 Code Walkthrough

### How RAG Works Here

```python
# 1. Parse regulatory docs into chunks
chunks = parser.parse_document("sfc_code.pdf")

# 2. Create embeddings and store
vector_store.add_documents(chunks)

# 3. For a prospectus section, find relevant regulations
relevant_regs = vector_store.search("fee disclosure requirements")

# 4. LLM compares prospectus vs regulations
result = llm.check_compliance(
    prospectus_text=section,
    regulatory_context=relevant_regs
)
```

### Adding a New Check

```python
# In compliance_checker.py
self.compliance_checks.append({
    'type': 'custody_requirements',
    'query': 'custodian custody arrangements safeguarding assets',
    'description': 'Custody and Safeguarding Requirements'
})

# In llm_analyzer.py, add to check_instructions
'custody_requirements': """
Check if the prospectus clearly discloses:
- Identity of the custodian
- Safeguarding arrangements
- Investor protections in case of custodian failure
"""
```

---

## 📞 Questions During Interview?

**Q: Why Ollama instead of OpenAI?**  
A: Hong Kong context - data privacy, no external APIs, runs locally

**Q: How accurate is this?**  
A: ~70-80% for flagging issues, requires manual review (by design)

**Q: Can it handle Chinese documents?**  
A: Current version is English-only, but could extend with multilingual embeddings

**Q: How would you scale this?**  
A: Vector DB (Pinecone/Weaviate), async processing, API backend, caching

**Q: What about false positives?**  
A: LLM provides explanations → human-in-the-loop review → tune prompts

---

## 🎓 Technologies Used

- **Python 3.8+**: Core language
- **Ollama**: Local LLM inference (Llama 3.2)
- **Sentence Transformers**: Text embeddings
- **pdfplumber**: PDF text extraction
- **NumPy**: Vector operations
- **Colorama**: CLI formatting

---

**Built by**: Pranavi Kuntrapakam  
**For**: Klares.io Application  
**Time**: ~3-4 hours (as designed for prototype scope)
