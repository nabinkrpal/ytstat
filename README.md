# 🎯 YouTube Comment Analyzer Web App

A full-stack web application that analyzes YouTube video comments using Python-based NLP and displays insights via a Node.js-powered server and HTML frontend.

🔗 **Live Demo**: [Hosted Link](https://ytstat.onrender.com/)

---

## 📌 Features

- Fetches YouTube comments using YouTube Data API.
- Performs sentiment analysis (positive, neutral, negative) using Python (`TextBlob`).
- Extracts trending nouns and keywords using `spaCy`.
- Detects suggestion phrases like "make a video on..." or "talk about...".
- Filters spam-like comments for accurate insights.
- Displays results in a user-friendly interface.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS (in `/public/index.html`)
- **Backend**: Node.js (`server.js`)
- **NLP Processing**: Python (`sentiment_analysis.py`)
- **APIs**: YouTube Data API
- **Dependencies**:
  - Python: `TextBlob`, `spaCy`
  - Node.js: Express (or whatever is listed in `package.json`)

---

## 🧠 Project Overview

### 🔍 Problem Statement
YouTube creators often receive overwhelming comment volumes and lack tools to analyze them efficiently.

### 💡 Approach
- `server.js` acts as the backend server and communicates with the Python script.
- `sentiment_analysis.py` processes comments for sentiment and keyword extraction.
- The web interface (in `/public/index.html`) displays processed results to the user.
- Integrated communication between Node.js and Python using child processes or HTTP request/response model.

### 📊 Output / Result
- Real-time sentiment breakdown (positive, neutral, negative).
- List of suggested topics and frequently mentioned keywords.
- Clear insights into audience interests and engagement patterns.

---

## 🚀 Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-comment-analyzer.git
cd youtube-comment-analyzer
