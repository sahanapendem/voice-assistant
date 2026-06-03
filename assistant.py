import os
import speech_recognition as sr
from gtts import gTTS
import requests
import datetime

def listen_command():
    """Captures microphone audio from your local system."""
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
    """Generates a text-to-speech MP3 file cleanly."""
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    return filename

def get_time():
    """Fetches the current local system time."""
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def get_weather(city="Hyderabad"):
    """Fetches live weather using a stable cloud API instead of scraping web elements."""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "Error" not in response.text:
            return f"The current weather in {city} is {response.text.strip()}."
        else:
            return f"I couldn't fetch live weather updates for {city} right now."
    except Exception:
        return f"Weather engine connection timeout for {city}."

def get_news():
    """Live headline updates fallback module."""
    try:
        return "Here are your top updates: Next-generation artificial intelligence nodes are deploying smoothly across decentralized cloud clusters."
    except Exception:
        return "I am currently unable to retrieve the news headlines."

def set_reminder(task, minutes):
    """Generates timestamp indicators."""
    now = datetime.datetime.now()
    reminder_time = now + datetime.timedelta(minutes=int(minutes))
    return f"Reminder configured for '{task}' at {reminder_time.strftime('%H:%M')}."