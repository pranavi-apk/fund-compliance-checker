#!/bin/bash

echo "🔧 Setting up Compliance Checker Virtual Environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To check if Ollama is running:"
echo "  ollama list"
echo ""
echo "To pull the required model (if not already available):"
echo "  ollama pull llama3.2"
