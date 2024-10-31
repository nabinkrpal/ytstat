#!/bin/bash
# python -m venv env
# source .\env\Scripts\Activate.ps1
# # Install Python dependencies
# pip install -r requirements.txt

# # Optionally, download spaCy model
# python -m textblob.download_corpora

# python -m spacy download en_core_web_sm

# # Start the Node.js server
# node server.js


# Install Python dependencies
echo "Installing Python dependencies....."
pip install -r requirements.txt

# Download necessary TextBlob corpora if required
python -m textblob.download_corpora || echo "TextBlob corpora download failed"

# Download spaCy model if required
python -m spacy download en_core_web_sm || echo "spaCy model download failed"

# Start the Node.js server
echo "Starting Node.js server guys..."
node server.js
