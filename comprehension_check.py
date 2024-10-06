
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai

# TODO: implement accuracy check, generate score
# TODO: generate new worksheet based on score

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

    openai.api_key = 'your_openai_api_key_here'  # Replace with your OpenAI API key

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5
    )

    questions = response.choices[0].text.strip()
    return questions

def main(youtube_url):
    #Input test URl to command line 
    parser = argparse.ArgumentParser(description='Generate worksheet questions from a YouTube video transcript.')
    parser.add_argument('youtube_url', type=str, help='The URL of the YouTube video')
    args = parser.parse_args()

    youtube_url = args.youtube_url
    transcript = get_transcript(youtube_url)
    if "Error" in transcript:
        print(transcript)
        return

    questions = generate_questions(transcript)
    print("Generated Worksheet Questions:")
    print(questions)