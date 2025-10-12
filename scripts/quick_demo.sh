#!/bin/bash

# Quick demo script - shows one complete check from start to finish
# Perfect for demonstrating during an interview

clear

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║      Investment Fund Compliance Checker - Quick Demo          ║"
echo "║      Built for Klares.io Application                          ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print with color
print_step() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check environment
print_step "STEP 1: Checking Environment"

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated"
    echo ""
    echo "Please run:"
    echo "  source venv/bin/activate"
    echo ""
    echo "Or if not yet setup:"
    echo "  ./setup_venv.sh"
    echo "  source venv/bin/activate"
    exit 1
fi

echo "✓ Virtual environment active: $VIRTUAL_ENV"

# Check Ollama
if ! ollama list &> /dev/null; then
    echo "❌ Ollama not running"
    echo ""
    echo "Please start Ollama in another terminal:"
    echo "  ollama serve"
    exit 1
fi

echo "✓ Ollama is running"

# Check model
if ! ollama list | grep -q "llama3.2"; then
    echo "⚠️  llama3.2 not found, pulling now..."
    ollama pull llama3.2
fi

echo "✓ Model llama3.2 ready"

# Show project structure
print_step "STEP 2: Project Structure"

echo "Core Components:"
ls -lh *.py | awk '{printf "  %-40s %6s\n", $9, $5}'

echo ""
echo "Documentation:"
ls -lh *.md | awk '{printf "  %-40s %6s\n", $9, $5}'

echo ""
echo "Regulatory Documents:"
ls -lh "fund manager code of conduct.pdf" "Code_on_MPF_Investment_Funds.pdf" 2>/dev/null | awk '{printf "  %-40s %6s\n", $9, $5}' || echo "  (PDFs not found)"

# Show a code snippet
print_step "STEP 3: Code Sample - Main Orchestrator"

echo "Here's how the compliance checker works:"
echo ""
head -50 compliance_checker.py | tail -30

read -p "Press ENTER to continue to live demo..." dummy

# Build knowledge base
print_step "STEP 4: Building Regulatory Knowledge Base"

if [ -f "knowledge_base_cache.json" ]; then
    echo "✓ Using cached knowledge base"
    ls -lh knowledge_base_cache.json
else
    echo "Building knowledge base from regulatory PDFs..."
    echo "(This takes ~2-3 minutes on first run)"
    echo ""
    python main.py --build-kb-only
fi

read -p "Press ENTER to run compliance check..." dummy

# Run compliance check
print_step "STEP 5: Running Live Compliance Check"

# Use first available prospectus
PROSPECTUS=""
if [ -f "20230504163240_1872.pdf" ]; then
    PROSPECTUS="20230504163240_1872.pdf"
elif [ -f "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf" ]; then
    PROSPECTUS="blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf"
fi

if [ -z "$PROSPECTUS" ]; then
    echo "❌ No test prospectus found"
    exit 1
fi

echo "Analyzing: $PROSPECTUS"
echo ""
echo "This will:"
echo "  1. Parse the prospectus PDF"
echo "  2. Search for fee, risk, and concentration sections"
echo "  3. Retrieve relevant regulatory requirements"
echo "  4. Use LLM to analyze compliance"
echo "  5. Generate a detailed report"
echo ""

python main.py --prospectus "$PROSPECTUS" --output demo_report.txt

# Show summary
print_step "STEP 6: Results Summary"

if [ -f "demo_report.txt" ]; then
    echo "Report generated: demo_report.txt"
    echo ""
    echo "━━━ Report Preview ━━━"
    head -40 demo_report.txt
    echo ""
    echo "... (see demo_report.txt for full report) ..."
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "⚠️  Report not generated (check for errors above)"
fi

# Final summary
print_step "Demo Complete!"

echo "What this demonstrates:"
echo ""
echo "  ✓ RAG Pipeline - Retrieval-Augmented Generation for compliance"
echo "  ✓ PDF Processing - Intelligent chunking with context preservation"
echo "  ✓ Semantic Search - Finding relevant regulations by meaning"
echo "  ✓ LLM Analysis - GPT-class reasoning with local inference"
echo "  ✓ Structured Output - Actionable reports with citations"
echo ""
echo "Technical Highlights:"
echo ""
echo "  • Modular architecture (5 core components)"
echo "  • Production-aware (caching, error handling, testing)"
echo "  • Hong Kong regulatory focus (SFC, MPF)"
echo "  • Local LLM for data privacy (Ollama)"
echo "  • Professional CLI with colored output"
echo ""
echo "Files Generated:"
echo "  • demo_report.txt - Compliance report"
echo "  • knowledge_base_cache.json - Embedded regulations"
echo ""
echo "Next Steps:"
echo "  • Read full report: cat demo_report.txt"
echo "  • Check other prospectuses: python main.py --prospectus <file.pdf>"
echo "  • Review documentation: cat README.md"
echo "  • Explore code: cat compliance_checker.py"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Built by: Pranavi Kuntrapakam                                 ║"
echo "║  For: Klares.io Application                                    ║"
echo "║  Tech: Python + Ollama + RAG + PDF Processing                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
