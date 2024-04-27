import os
import requests
import moviepy.editor as mp
from elevenlabs.client import ElevenLabs

# ElevenLabs API 설정
VOICE_ID = "oWAxZDx7w5VEj9dCyTzz"
API_KEY = "{API_KEY}"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
HEADERS = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

# 자막 파일 읽기
def read_subtitles(subtitle_file):
    subtitles = []
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            start_time_str = lines[i].strip()
            text = lines[i+1].strip()
            parts = start_time_str.split(':')
            start_time = '{}-{}'.format(parts[0], parts[1])
            subtitles.append((start_time, text))
    return subtitles

# 오디오 생성
def generate_audio(text, filename):
    url = BASE_URL + VOICE_ID
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=HEADERS)
    with open(filename, 'wb') as f:
        f.write(response.content)

# 비디오 생성
def generate_video(input_video, output_video, subtitles):
    video = mp.VideoFileClip(input_video)
    audio_clips = []

    for start_time, text in subtitles:
        audio_file = start_time + ".mp3"
        if not os.path.exists(audio_file):
            generate_audio(text, audio_file)
        audio_clip = mp.AudioFileClip(audio_file)
        audio_clips.append(audio_clip.set_start(start_time.replace('-', ':')))

    final_audio = mp.CompositeAudioClip(audio_clips)
    video = video.set_audio(final_audio)
    video.write_videofile(output_video)

# 실행
input_video = "original_video.mp4"
subtitle_file = "subtitles.txt"
output_video = "dubbed_video.mp4"

subtitles = read_subtitles(subtitle_file)
generate_video(input_video, output_video, subtitles)
