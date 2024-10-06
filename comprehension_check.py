#! /usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
import re, requests
import anthropic 
import argparse
from flask import Flask
from pdb import set_trace as bp
from dotenv import load_dotenv 
import os
SECRET_KEY=mysecretkey

# TODO: implement accuracy check, generate score
# TODO: generate new worksheet based on score

app = Flask(__name__)
load_dotenv()  # get variables from .env file
secret_key = os.getenv("SECRET_KEY")

def get_video_id(youtube_url):
    # Extract the video ID from the YouTube URL
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, youtube_url)
    return match.group(1) if match else None

def get_transcript(youtube_url):
    video_id = get_video_id(youtube_url)
    if not video_id:
        return "Invalid YouTube URL"

    try:
        # Get transcript using video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript into single string
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text

    except Exception as e:
        return f"Error fetching transcript: {e}"


def generate_questions(transcript):
    # Generate worksheet questions

    prompt = "Create 4 comprehension questions based on the following transcript:\n" + transcript

    # Replace with actual API endpoint and authentication
    url = "https://api.anthropic.com/v1/completions"
    headers = {
        "Authorization": "Bearer " + SECRET_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "claude-3-sonnet-20240229",
        "max_tokens_to_sample": 1000
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["completion"]
    else:
        print(f"Error: {response.status_code}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #youtube_url = request.form.get('youtube_url')
        youtube_url = 'https://www.youtube.com/watch?v=m65RS5NFlf4'
        transcript = get_transcript(youtube_url)
        
        # Compare essay
        essay = "test input"  # You might want to get this from the user input as well
        score = compute_score(essay, transcript)

        print("Student comprehension score: " + str(score))
        
        #return render_template('result.html', score=score, transcript=transcript)
    
    #return render_template('index.html')

def compute_score(essay, transcript):
    # Tokenize the strings into sets of words
    set1 = set(essay.split())
    set2 = set(transcript.split())
    
    # Calculate the intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    # Calculate Jaccard similarity
    if not union:  # To avoid division by zero
        return 0.0
    
    similarity = len(intersection) / len(union)
    return similarity

if __name__=="__main__":
    app.run(debug=True)
