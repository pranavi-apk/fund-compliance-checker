#!/bin/bash

# Launcher script for Streamlit Compliance Checker
# Updated for new organized file structure

echo "🚀 Starting Investment Fund Compliance Checker..."
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found!"
    echo "Please create it with: python3 -m venv venv"
    exit 1
fi

# Check if Ollama is running
if ! ollama list &> /dev/null; then
    echo "⚠️  Ollama not running!"
    echo "Please start Ollama in another terminal: ollama serve"
    exit 1
fi

echo "✓ Ollama detected"
echo "✓ Launching Streamlit app..."
echo ""
echo "📱 The app will open in your browser automatically"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit with the new path
streamlit run src/ui/app.py