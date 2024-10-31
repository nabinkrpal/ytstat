#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Optionally, download spaCy model
python -m textblob.download_corpora

python -m spacy download en_core_web_sm

# Start the Node.js server
node server.js
