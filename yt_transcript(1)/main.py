!pip install pytube
!pip install pydub
!apt-get install ffmpeg
!pip install youtube-transcript-api

import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(youtube_url):
    # Regular expression pattern for matching YouTube video ID
    pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/[^/]+/|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/watch\?v=)([^"&?/ ]{11})')

    # Search for the pattern in the URL
    match = pattern.search(youtube_url)

    if match:
        return match.group(1)
    else:
        return None

# Get video_id
youtube_url = "https://www.youtube.com/watch?v=PH-2FfFD2PU"
video_id = extract_video_id(youtube_url)

# Get the transcript for the video
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Function to format time in hh:mm:ss
def format_time(seconds):
    return "{:02d}:{:02d}:{:02d}".format(int(seconds / 3600), int((seconds % 3600) / 60), int(seconds % 60))

# Function to create formatted text
def create_formatted_text(transcript):
    formatted_text = ""
    start_time = 0

    for entry in transcript:
        end_time = entry['start'] + entry['duration']

        # Check if the entry duration is within the desired range (4-10 seconds)
        if 4 <= entry['duration'] <= 10:
            formatted_text += "{}-{}:  {}\n".format(format_time(start_time), format_time(end_time), entry['text'])
            start_time = end_time

    return formatted_text

# Create formatted text
formatted_text = create_formatted_text(transcript)

# Save formatted text to a file
with open('transcription.txt', 'w') as file:
    file.write(formatted_text)
