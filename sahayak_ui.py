# sahayak_ui.py

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import streamlit as st
import threading

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# --- Core assistant logic functions ---

def speak(text):
    st.session_state["assistant_reply"] = text
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Sahayak, your personal assistant. Please tell me how may I help you.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state["status"] = "🎙 Listening..."
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        st.session_state["status"] = "🧠 Recognizing..."
        query = r.recognize_google(audio, language='en-in')
        st.session_state["query"] = query
        return query.lower()
    except Exception:
        st.session_state["status"] = "😶 Could not recognize. Please try again."
        return "None"

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')  # Use secure method!
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

# --- Task Dispatcher ---

def process_query(query):
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia: " + results)

    elif 'open youtube' in query:
        speak("Opening YouTube.")
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        speak("Opening Google.")
        webbrowser.open("google.com")

    elif 'open stackoverflow' in query:
        speak("Opening StackOverflow.")
        webbrowser.open("stackoverflow.com")

    elif 'play music' in query:
        music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        speak("Playing your favorite music.")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        codePath = "C:\\Users\\Mahul\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)
        speak("Opening Visual Studio Code.")

    elif 'email to mahul' in query:
        speak("What should I say?")
        content = takeCommand()
        to = "mahulyourEmail@gmail.com"
        try:
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception:
            speak("Sorry, I couldn't send the email.")

    elif 'exit' in query or 'quit' in query:
        speak("Goodbye Sir. Sahayak signing off.")
        st.stop()

    else:
        speak("Sorry, I didn’t understand that command.")


# --- Streamlit UI setup ---

st.set_page_config(page_title="Sahayak - Voice Assistant", layout="centered")
st.title("🤖 SAHAYAK - Your Personal AI Assistant")
st.markdown("##### Speak a command and let Sahayak do the work!")

if "status" not in st.session_state:
    st.session_state["status"] = "Idle"
    st.session_state["query"] = ""
    st.session_state["assistant_reply"] = ""

st.info(st.session_state["status"])
st.text_input("🗣 Last Command", value=st.session_state["query"], key="display_query")
st.text_area("🤖 Assistant Says", value=st.session_state["assistant_reply"], height=100)

# --- Button Handlers ---

def run_assistant():
    wishMe()
    query = takeCommand()
    if query != "None":
        process_query(query)

if st.button("🎤 Start Listening"):
    threading.Thread(target=run_assistant).start()
