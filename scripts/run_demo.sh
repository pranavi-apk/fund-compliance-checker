#!/bin/bash

# Demo script for Compliance Checker
# This script demonstrates the full workflow

echo "🎯 Investment Fund Compliance Checker Demo"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Check if Ollama is running
echo "Checking Ollama status..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install from https://ollama.ai/"
    exit 1
fi

if ! ollama list &> /dev/null; then
    echo "⚠️  Ollama service not running!"
    echo "Please start it with: ollama serve"
    echo "(Run in a separate terminal)"
    exit 1
fi

echo "✓ Ollama is running"
echo ""

# Check if model is available
echo "Checking for llama3.2 model..."
if ! ollama list | grep -q "llama3.2"; then
    echo "⚠️  Model llama3.2 not found"
    echo "Pulling model (this may take a few minutes)..."
    ollama pull llama3.2
fi
echo "✓ Model ready"
echo ""

# Build knowledge base if not exists
if [ ! -f "knowledge_base_cache.json" ]; then
    echo "📚 Building regulatory knowledge base (first time only)..."
    echo "This will take a few minutes..."
    python main.py --build-kb-only
    echo ""
fi

# Run demo checks
echo "🔍 Running compliance checks on test prospectuses..."
echo ""

# Check E Fund ETF
if [ -f "20230504163240_1872.pdf" ]; then
    echo "1️⃣  Checking E Fund ETF..."
    python main.py --prospectus "20230504163240_1872.pdf" --output efund_report.txt
    echo "   Report saved to: efund_report.txt"
    echo ""
fi

# Check ChinaAMC if available
if [ -f "E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf" ]; then
    echo "2️⃣  Checking ChinaAMC Global ETF..."
    python main.py --prospectus "E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf" --output chinaamc_report.txt
    echo "   Report saved to: chinaamc_report.txt"
    echo ""
fi

# Check BlackRock if available
if [ -f "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf" ]; then
    echo "3️⃣  Checking BlackRock Premier Funds..."
    python main.py --prospectus "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf" --output blackrock_report.txt
    echo "   Report saved to: blackrock_report.txt"
    echo ""
fi

echo "✅ Demo complete!"
echo ""
echo "📊 Generated reports:"
ls -lh *_report.txt 2>/dev/null || echo "   (check console output above)"
echo ""
echo "Next steps:"
echo "  - Review the generated reports"
echo "  - Try: python main.py --prospectus <your_file.pdf>"
echo "  - See README.md for more options"
