import sys
import re
import json
from textblob import TextBlob
from googleapiclient.discovery import build
import spacy
from collections import Counter

# Setup YouTube API and Spacy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv("API_KEY")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
nlp = spacy.load('en_core_web_sm')

# Keywords to detect suggested topics in comments
suggestion_keywords = ["want to see", "please make", "make a video on", "video on", "video about"]

def is_youtube_url(url):
    """
    Validates if the given URL is a YouTube video or Shorts URL.
    :param url: URL string
    :return: Video ID if valid, None otherwise
    """
    match = re.search(
        r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})",
        url,
    )
    return match.group(1) if match else None

def fetch_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText")
    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(comment['textDisplay'])
        request = youtube.commentThreads().list_next(request, response)
    return comments

def analyze_comments(comments):
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    suggested_topics = []

    for comment in comments:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment_counts["positive"] += 1
        elif polarity == 0:
            sentiment_counts["neutral"] += 1
        else:
            sentiment_counts["negative"] += 1

        # Check for topic suggestions in comments
        if any(keyword in comment.lower() for keyword in suggestion_keywords):
            suggested_topics.extend(extract_topics(comment))

    # Calculate sentiment percentages
    total = sum(sentiment_counts.values())
    sentiment_percentages = {k: (v / total) * 100 for k, v in sentiment_counts.items()}

    # Count and filter trending topics (appearing more than once)
    trending_topics = [topic for topic, count in Counter(suggested_topics).items() if count > 1]
    return sentiment_percentages, trending_topics

def extract_topics(text):
    """
    Extracts meaningful noun phrases from text using NLP without predefined non-topic words.
    :param text: String containing comment text.
    :return: List of meaningful topics.
    """
    doc = nlp(text)
    topics = []
    for chunk in doc.noun_chunks:
        # Only include chunks that are coherent noun phrases and not single pronouns
        if len(chunk) > 1 or chunk[0].pos_ == 'NOUN':
            topics.append(chunk.text.lower().strip())
    return topics

if __name__ == "__main__":
    url = sys.argv[1]
    video_id = is_youtube_url(url)

    if not video_id:
        print(json.dumps({"error": "Invalid YouTube URL"}))
        sys.exit(1)

    comments = fetch_comments(video_id)
    sentiment, topics = analyze_comments(comments)
    output = {"sentiment": sentiment, "topics": topics}
    print(json.dumps(output))
