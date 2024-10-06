#! /usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
import argparse
from pdb import set_trace as bp

# TODO: implement accuracy check, generate score
# TODO: generate new worksheet based on score

openai.api_key = '' 

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
    prompt = (
        "Create 4 comprehension questions based on the following transcript:\n\n"
        f"{transcript}\n\n"
        "Questions:\n"
    )

    
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",  # Specify the model to use
        messages=[
            {"role": "user", "content": prompt}  # Replace 'prompt' with your input
        ],
        max_tokens=150,
        temperature=0.5
    )

    questions = response.choices[0].text.strip()
    return questions

def main():

    youtube_url = 'https://www.youtube.com/watch?v=m65RS5NFlf4'
    
    """   
    # Prompt the user for the YouTube URL  
    try:
        youtube_url = input("Input YouTube URL: ")
        # Ensure the URL is valid (you can add further validation here)
        if not youtube_url.startswith("https://www.youtube.com/watch?v="):
            print("Invalid YouTube URL format.")
            return
    except Exception as e:  # Catch any exception
        print(f"Error: {e}. Please try again.")
        return 
    """

    transcript = get_transcript(youtube_url)  # Fetch the transcript
    print(transcript)  

    questions = generate_questions(transcript)  # Generate questions from the transcript
    print("Generated Worksheet Questions:")
    for question in questions:
        print(question)

if __name__=="__main__":
    main()