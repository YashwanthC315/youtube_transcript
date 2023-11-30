from pytube import YouTube
from pydub import AudioSegment
import os
import assemblyai as aai
from datetime import timedelta

# Set up AssemblyAI API key
aai.settings.api_key = "cf797eab606743f2bd90c9c74a7568a6"

# Function to download YouTube video, convert to MP3 and WAV, and transcribe
def process_youtube_video(video_url):
    save_path = "/content/"

    # Step 1: Download YouTube Video
    youtube = YouTube(video_url)
    video_stream = youtube.streams.filter(only_audio=True).first()
    video_stream.download(save_path)

    # Step 2: Convert MP4 to MP3
    video_path = os.path.join(save_path, video_stream.title + ".mp4")
    mp3_path = os.path.join(save_path, video_stream.title + ".mp3")

    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export(mp3_path, format="mp3")

    # Step 3: Convert MP3 to WAV
    wav_path = os.path.join(save_path, video_stream.title + ".wav")

    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio.export(wav_path, format="wav")

    # Step 4: Transcribe to Text using AssemblyAI
    transcribed_text = transcribe_audio(wav_path)

    # Step 5: Save Transcription to Text File
    text_file_path = os.path.join(save_path, video_stream.title + ".txt")
    with open(text_file_path, 'w') as text_file:
        text_file.write(transcribed_text)

    # Step 6: Split Transcription into 10-second intervals with time stamps
    split_text = split_into_intervals(transcribed_text, interval_length=10)
    intervals_file_path = os.path.join(save_path, video_stream.title + "_intervals.txt")
    with open(intervals_file_path, 'w') as intervals_file:
        intervals_file.write('\n'.join(split_text))

    # Clean up: Delete the downloaded video, MP3, and WAV files
    os.remove(video_path)
    os.remove(mp3_path)
    os.remove(wav_path)

# Function to transcribe audio using AssemblyAI
def transcribe_audio(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    return transcript.text

# Function to split text into intervals with time stamps
def split_into_intervals(transcribed_text, interval_length=10):
    words = transcribed_text.split()
    current_interval = ''
    intervals = []
    current_time = 0

    for word in words:
        current_interval += word + ' '
        if current_time >= interval_length:
            start_time = format_time(current_time - interval_length)
            end_time = format_time(current_time)
            intervals.append(f'{start_time}-{end_time} {current_interval.strip()}')
            current_interval = ''
            current_time = 0
        else:
            current_time += 1

    return intervals

# Function to format time in seconds to hh:mm:ss
def format_time(seconds):
    return str(timedelta(seconds=seconds))

# Enter youtube video url
video_url = "https://www.youtube.com/watch?v=PH-2FfFD2PU"
process_youtube_video(video_url)
