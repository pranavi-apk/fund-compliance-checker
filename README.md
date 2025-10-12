# Investment Fund Compliance Checker

**Organized Project Structure** - Clean, modular, production-ready

A RAG-based system for scanning investment fund prospectuses against Hong Kong regulatory requirements (SFC Fund Manager Code of Conduct and MPF Code on Investment Funds).

**Built for**: Klares.io Application Demonstration  
**Author**: Pranavi Kuntrapakam

---

## 📁 Project Structure

```
compliance/
├── 📂 src/                          # Source code
│   ├── 📂 core/                     # Core business logic
│   │   ├── __init__.py              # Package initialization
│   │   ├── pdf_parser.py            # PDF extraction & chunking
│   │   ├── vector_store.py          # Semantic search engine
│   │   ├── llm_analyzer.py          # LLM compliance analysis
│   │   └── compliance_checker.py    # Main orchestrator
│   │
│   └── 📂 ui/                       # User interfaces
│       ├── __init__.py              
│       └── app.py                   # Streamlit web app
│
├── 📂 config/                       # Configuration files
│   └── config.py                    # System settings
│
├── 📂 data/                         # Data files
│   └── 📂 pdfs/                     # PDF documents
│       ├── fund manager code of conduct.pdf
│       ├── Code_on_MPF_Investment_Funds.pdf
│       ├── 20230504163240_1872.pdf  # E Fund ETF
│       ├── E-[Clean]ChinaAMC...pdf  # ChinaAMC Global
│       └── blackrock-premier...pdf  # BlackRock Premier
│
├── 📂 docs/                         # Documentation
│   ├── README.md                    # This file
│   ├── QUICKSTART.md               # Quick setup guide
│   ├── STREAMLIT_GUIDE.md          # Streamlit app guide
│   └── PROJECT_SUMMARY.md          # Technical summary
│
├── 📂 scripts/                      # Utility scripts
│   ├── setup_venv.sh               # Environment setup
│   ├── run_app.sh                  # Run Streamlit app
│   ├── run_demo.sh                 # Full demo
│   ├── quick_demo.sh               # Interview demo
│   └── check_setup.py              # Pre-flight checks
│
├── 📂 tests/                        # Test files
│   ├── test_components.py          # Unit tests
│   └── test_checker.py             # Integration tests
│
├── main.py                          # CLI entry point
├── run_app.sh                       # Main app launcher
├── requirements.txt                 # Dependencies
└── knowledge_base_cache.json        # Cached embeddings
```

---

## 🚀 Quick Start

### **Option 1: Web Interface (Recommended)**

```bash
# Setup (first time only)
./scripts/setup_venv.sh
source venv/bin/activate

# Start Ollama (separate terminal)
ollama serve
ollama pull llama3.1:8b

# Launch web app
./run_app.sh
```

Visit: **http://localhost:8501**

### **Option 2: Command Line Interface**

```bash
# Build knowledge base (first time)
python main.py --build-kb-only

# Analyze a prospectus
python main.py --prospectus "data/pdfs/20230504163240_1872.pdf"
```

---

## 🎨 Benefits of New Structure

### **🧩 Modular Architecture**
- **`src/core/`** - Business logic, reusable across interfaces
- **`src/ui/`** - Interface code, easily swappable
- **`config/`** - Centralized configuration management
- **`tests/`** - Comprehensive test coverage

### **📦 Clean Imports**
```python
# Old (messy)
from compliance_checker import ComplianceChecker
from pdf_parser import PDFParser

# New (clean)
from src.core import ComplianceChecker, PDFParser
```

### **🔧 Easy Maintenance**
- **Separation of concerns** - Each module has single responsibility
- **Easy testing** - Mock individual components
- **Scalable** - Add new features without breaking existing code
- **Professional** - Industry-standard Python project structure

### **🎯 Production Ready**
- **Package structure** - Can be built into Python package
- **Import paths** - Proper relative imports
- **Configuration** - External config files
- **Documentation** - Organized in `docs/` folder

---

## 📊 Component Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| **PDFParser** | Extract & chunk PDF text | `src/core/pdf_parser.py` |
| **VectorStore** | Semantic search engine | `src/core/vector_store.py` |
| **ComplianceLLM** | LLM analysis engine | `src/core/llm_analyzer.py` |
| **ComplianceChecker** | Main orchestrator | `src/core/compliance_checker.py` |
| **Streamlit App** | Web interface | `src/ui/app.py` |
| **CLI Interface** | Command line tool | `main.py` |

---

## 🔧 Development Workflow

### **Adding New Features**

1. **Core Logic** → Add to `src/core/`
2. **UI Updates** → Modify `src/ui/app.py`
3. **Configuration** → Update `config/config.py`
4. **Tests** → Add to `tests/`
5. **Documentation** → Update `docs/`

### **Running Tests**

```bash
# Unit tests
python tests/test_components.py

# Integration tests  
python tests/test_checker.py

# Pre-flight check
python scripts/check_setup.py
```

### **Different Interfaces**

```bash
# Web app (Streamlit)
./run_app.sh

# Command line
python main.py --prospectus "data/pdfs/file.pdf"

# Programmatic usage
python -c "from src.core import ComplianceChecker; ..."
```

---

## 🎯 Key Features

### **3 Compliance Checks**
1. **Fee Disclosure** - Management fees, performance fees, calculations
2. **Risk Disclosure** - Market, liquidity, currency risks  
3. **Concentration Limits** - Single issuer exposure restrictions

### **Professional UI**
- **Black theme** - Clean, modern aesthetic
- **Loading animations** - Real-time progress feedback
- **Interactive charts** - Violation visualization
- **Reset functionality** - Start fresh with new files

### **Robust Architecture** 
- **RAG Pipeline** - Semantic search + LLM analysis
- **Local LLM** - Ollama for data privacy
- **Caching** - Fast subsequent runs
- **Error handling** - Graceful failure recovery

---

## 🚨 Migration Notes

### **Path Updates**
All file references have been updated:

```bash
# PDFs moved to
data/pdfs/

# Scripts moved to  
scripts/

# Core modules moved to
src/core/

# Tests moved to
tests/
```

### **Import Changes**
```python
# Old imports
from compliance_checker import ComplianceChecker

# New imports  
from src.core import ComplianceChecker
```

### **Running the App**
```bash
# Old
streamlit run app.py

# New
./run_app.sh
# or
streamlit run src/ui/app.py
```

---

## 📈 Performance Benefits

- **Faster imports** - Organized module structure
- **Better caching** - Dedicated data directory
- **Easier debugging** - Clear component boundaries  
- **Scalable testing** - Isolated test environment

---

## 🎓 Technical Highlights

This reorganized structure demonstrates:

✅ **Software Engineering Best Practices**  
✅ **Clean Architecture Principles**  
✅ **Python Package Structure**  
✅ **Separation of Concerns**  
✅ **Maintainable Codebase**  
✅ **Production Readiness**  

Perfect for demonstrating professional development skills in job applications!

---

**Built for Klares.io Application**  
**Clean, Organized, Production-Ready Architecture** 🏗️