#!/bin/bash
# Code of Pride Installer Script

echo "Installing Code of Pride..."

# Create virtual environment
python3 -m venv code-of-pride-env
source code-of-pride-env/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Installation complete!"
echo "To run the game, execute: python core/main.py"
