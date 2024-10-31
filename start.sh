#!/bin/bash
python -m venv venv
source .\venv\Scripts\Activate.ps1
# Install Python dependencies
pip install -r requirements.txt

# Optionally, download spaCy model
python -m textblob.download_corpora

python -m spacy download en_core_web_sm

# Start the Node.js server
node server.js
