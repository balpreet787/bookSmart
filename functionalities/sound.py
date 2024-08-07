from textblob import TextBlob
import requests
import os
from dotenv import load_dotenv

load_dotenv()
FREESOUND_API_KEY = os.getenv('FREESOUND_API_KEY')


def analyze_page(page):
    blob = TextBlob(page)
    sentiment = blob.sentiment.polarity
    words = blob.words.singularize()

    mood = "neutral"
    if sentiment > 0.5:
        mood = "excited"
    elif sentiment > 0.2:
        mood = "happy"
    elif 0.1 < sentiment <= 0.2:
        mood = "calm"
    elif -0.1 <= sentiment <= 0.1:
        mood = "neutral"
    elif -0.2 <= sentiment < -0.1:
        mood = "sad"
    elif -0.5 <= sentiment < -0.2:
        mood = "fearful"
    elif sentiment < -0.5:
        mood = "angry"

    environments = [
        "rain", "forest", "beach", "city", "battle", "night",
        "morning", "desert", "mountains", "ocean", "crowd",
        "fireplace", "café", "snow", "garden"
    ]
    detected_environment = next((env for env in environments if env in words), "general")
    print(f"{mood} and {detected_environment}")
    return {"mood": mood, "environment": detected_environment}


def construct_query_url(query):
    return f"https://freesound.org/apiv2/search/text/?query={query}&token={FREESOUND_API_KEY}"


def fetch_sound_details(sound_id):
    url = f"https://freesound.org/apiv2/sounds/{sound_id}/?token={FREESOUND_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "previews" in data:
            if "preview-lq-mp3" in data["previews"]:
                return data["previews"]["preview-lq-mp3"]
            elif "preview-hq-mp3" in data["previews"]:
                return data["previews"]["preview-hq-mp3"]
    else:
        print(f"HTTP error {response.status_code}: {response.reason}")
    return None


def fetch_sound_url(query):
    url = construct_query_url(query)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            sound_id = data["results"][0]["id"]
            return fetch_sound_details(sound_id)
    else:
        print(f"HTTP error {response.status_code}: {response.reason}")
    return None


def fetch_sounds(sounds):
    mood_query = f"{sounds['mood']} lofi sound"
    environment_query = f"{sounds['environment']} sound"

    play_sounds = {}
    mood_sound_url = fetch_sound_url(mood_query)
    environment_sound_url = fetch_sound_url(environment_query)

    if mood_sound_url:
        play_sounds["mood"] = mood_sound_url
    if environment_sound_url:
        play_sounds["environment"] = environment_sound_url
    print(play_sounds)
    return play_sounds if play_sounds else None
