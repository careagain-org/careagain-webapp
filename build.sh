#!/bin/bash

# Install Python and dependencies
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Build your Python Reflex app
echo "Building the app..."
reflex run  
