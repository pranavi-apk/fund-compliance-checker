#!/bin/bash

# Launcher script for Streamlit Compliance Checker

echo "🚀 Starting Investment Fund Compliance Checker..."
echo ""

# Activate virtual environment
source venv/bin/activate

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

# Run Streamlit
streamlit run src/ui/app.py
