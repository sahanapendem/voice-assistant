import speech_recognition as sr
import datetime
import requests
import os
import time
from gtts import gTTS
from pygame import mixer
from bs4 import BeautifulSoup

# Initialize the mixer for audio playback
try:
    mixer.init()
except Exception:
    pass  # Ignored if running on a headless cloud server

def speak(text):
    """Converts text to an MP3 file and plays it safely without driver lockups."""
    print(f"Assistant: {text}")
    
    # 1. Generate the audio file using Google TTS
    tts = gTTS(text=text, lang='en', slow=False)
    filename = "temp_voice.mp3"
    tts.save(filename)
    
    # 2. Play the audio file using pygame mixer
    mixer.music.load(filename)
    mixer.music.play()
    
    # 3. Wait until the assistant finishes speaking before moving on
    while mixer.music.get_busy():
        time.sleep(0.1)
        
    # 4. Unload the audio file so Windows/Mac releases the file lock
    mixer.music.unload()
    
    # 5. Clean up the temporary file
    try:
        os.remove(filename)
    except Exception:
        pass

def listen_command():
    """Listens to microphone, with a graceful fallback if no hardware mic is found."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        return query.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return "none"
    except Exception as e:
        # Catches environments without microphone hardware (like Streamlit Cloud servers)
        print(f"Microphone hardware not available: {e}")
        return "hardware_missing"

def get_weather():
    """Fetches a live weather summary via text-based web scraping."""
    try:
        response = requests.get("https://wttr.in/?format=%C+%t")
        if response.status_code == 200:
            return f"The current weather is {response.text.strip()}."
        else:
            return "I am having trouble accessing weather data right now."
    except Exception:
        return "I couldn't connect to the weather service."

def get_news():
    """Fetches top 3 headlines from Google News RSS feed."""
    try:
        url = "https://news.google.com/rss"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="xml")
        headlines = soup.findAll('title')
        
        news_list = []
        for i, headline in enumerate(headlines[1:4], 1): 
            news_list.append(f"Headline {i}: {headline.text}")
        return " Here are today's top headlines: " + " | ".join(news_list)
    except Exception:
        return "I am unable to fetch the news at the moment."

def set_reminder(query):
    """Saves a noted task directly into a text file workspace."""
    if "remind me to" in query:
        reminder = query.split("remind me to")[-1].strip()
        
        with open("reminders.txt", "a") as f:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f"[{current_time}] {reminder}\n")
        return f"Got it. I'll remind you to {reminder}."
    else:
        return "What exactly would you like me to remind you to do?"