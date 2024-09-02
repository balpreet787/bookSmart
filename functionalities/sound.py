from textblob import TextBlob
import requests
import os
from dotenv import load_dotenv

load_dotenv()
FREESOUND_API_KEY = os.getenv('FREESOUND_API_KEY')


def analyze_page(page):
    """
    Analyze the sentiment of a page and determine the mood.

    :param page: a string containing the text of the page
    :precondition: page must be a non-empty string
    :postcondition: determines the mood based on the sentiment analysis of the text
    :return: a string representing the mood
    """
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

    return mood


def construct_query_url(query):
    """
    Construct a URL for querying the Freesound API.

    :param query: the search query string
    :precondition: query must be a non-empty string
    :postcondition: returns a properly formatted URL for the Freesound API
    :return: a string representing the URL for the Freesound API query
    """
    return f"https://freesound.org/apiv2/search/text/?query={query}&token={FREESOUND_API_KEY}"


def fetch_sound_details(sound_id):
    """
    Fetch the sound details from Freesound API using the sound ID.

    :param sound_id: the ID of the sound
    :precondition: sound_id must be a valid Freesound sound ID
    :postcondition: returns the URL of the sound preview if available
    :return: a string representing the URL of the sound preview, or None if not found
    """
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
    """
    Fetch the URL of the sound preview from Freesound API based on a search query.

    :param query: the search query string
    :precondition: query must be a non-empty string
    :postcondition: returns the URL of the first sound preview if available
    :return: a string representing the URL of the sound preview, or None if not found
    """
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
    """
    Fetch the mood sound URL based on the given mood.

    :param sounds: a string representing the mood
    :precondition: sounds must be a valid mood string
    :postcondition: returns the URL of the sound preview if available
    :return: a string representing the URL of the sound preview, or None if not found
    """
    mood_query = f"{sounds} piano sound"

    play_sound = None
    mood_sound_url = fetch_sound_url(mood_query)

    if mood_sound_url:
        play_sound = mood_sound_url
    return play_sound if play_sound else None
