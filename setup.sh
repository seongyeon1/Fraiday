#!/bin/bash

# Create and activate virtual environment
python -m venv .venv
echo '.venv' >> .gitignore
source .venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Prompt user for UPSTAGE_API_KEY
read -p "Enter your UPSTAGE_API_KEY: " UPSTAGE_API_KEY

# Create .env file
cat > .env <<EOL
UPSTAGE_API_KEY=$UPSTAGE_API_KEY
EOL

# Run OCR processing for both PDFs
make ocr

# Run chunking process for both OCR results
make chunk

# Run the app
make rerun

# Print out the URLs for accessing the app
echo "App is running. You can access it at the following URLs:"
echo "http://0.0.0.0:8000/ : same with http://0.0.0.0:8000/main/playground"
echo "http://0.0.0.0:8000/chat/playground"
echo "http://0.0.0.0:8000/main/playground"