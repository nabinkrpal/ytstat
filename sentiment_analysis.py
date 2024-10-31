# sentiment_analysis.py
import sys
import re
import json
import time
from textblob import TextBlob
from googleapiclient.discovery import build
import spacy
from collections import Counter

# import json
# api_key=""

# with open('config.json') as config_file:
#     config = json.load(config_file)
#     api_key = config['api_key']
YOUTUBE_API_KEY = "AIzaSyCh9tny8fDCnuKKPhnayIxPSw2EZmu_48w"
# 'AIzaSyCh9tny8fDCnuKKPhnayIxPSw2EZmu_48w'  # Replace with your API 
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
nlp = spacy.load('en_core_web_sm')

# def is_youtube_url(url):
#     match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
#     return match.group(1) if match else None

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
    topics = []

    for comment in comments:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment_counts["positive"] += 1
            topics.extend(extract_topics(comment))
        elif polarity == 0:
            sentiment_counts["neutral"] += 1
            topics.extend(extract_topics(comment))
        else:
            sentiment_counts["negative"] += 1

    total = sum(sentiment_counts.values())
    sentiment_percentages = {k: (v / total) * 100 for k, v in sentiment_counts.items()}
    trending_topics = [topic for topic, count in Counter(topics).most_common(20)]
    return sentiment_percentages, trending_topics

def extract_topics(text):
    doc = nlp(text)
    return [chunk.text.lower() for chunk in doc.noun_chunks]

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
