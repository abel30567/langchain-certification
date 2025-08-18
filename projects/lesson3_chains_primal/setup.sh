#!/bin/bash

echo "Setting up Primal TCG Chains Project..."
echo "======================================="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=your_key_here" > .env
    echo ""
    echo "⚠️  Please edit .env and add your OpenAI API key"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Add your OpenAI API key to the .env file"
echo "3. Run the interactive demo: python3 demo_interactive.py"
echo "4. Or run the automatic demo: python3 demo_automatic.py"