import os
import speech_recognition as sr
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import datetime

def listen_command():
    """Captures microphone audio from local machine. 
    Note: On cloud hosting like Streamlit, standard microphone access requires HTTPS."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio)
            return command.lower()
        except Exception:
            return ""

def speak(text):
    """Generates an MP3 file using gTTS and returns the filename."""
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    return filename

def get_weather(city="Hyderabad"):
    """Fetches simple live weather descriptions via scraping."""
    try:
        url = f"https://www.google.com/search?q=weather+in+{city}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        weather = soup.find("div", class_="BNeawe").text
        return f"The current weather in {city} is {weather}."
    except Exception:
        return "I couldn't fetch the weather updates right now."

def get_news():
    """Fetches trending headlines."""
    try:
        url = "https://news.google.com/rss"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")
        titles = [item.title.text for item in soup.find_all("item")[:3]]
        return "Here are the top headlines: " + ". ".join(titles)
    except Exception:
        return "I am currently unable to retrieve the news."

def set_reminder(task, minutes):
    """Calculates a future timestamp for user tasks."""
    now = datetime.datetime.now()
    reminder_time = now + datetime.timedelta(minutes=int(minutes))
    return f"Reminder set for '{task}' at {reminder_time.strftime('%H:%M')}."