#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create a virtual environment
python -m venv .venv
echo '.venv' >> .gitignore
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create the .env file
echo "Enter your UPSTAGE_API_KEY: "
read UPSTAGE_API_KEY
cat > .env <<EOL
UPSTAGE_API_KEY='$UPSTAGE_API_KEY'
EOL

# Navigate to the app directory and run the app
cd app
python main.py

# Print out the URLs for accessing the app
echo "App is running. You can access it at the following URLs:"
echo "http://0.0.0.0:8000/ : same with http://0.0.0.0:8000/main/playground"
echo "http://0.0.0.0:8000/chat/playground"
echo "http://0.0.0.0:8000/main/playground"