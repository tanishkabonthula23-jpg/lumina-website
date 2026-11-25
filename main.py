import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
import requests
import pyjokes
import time

# ==================== INITIALIZATION ====================
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Female voice (change index if needed)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)

recognizer = sr.Recognizer()

# ==================== SPEAK FUNCTION ====================
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ==================== LISTEN FUNCTION ====================
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please say again.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return ""

# ==================== WISH ME ====================
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal assistant. How can I help you?")

# ==================== MAIN COMMAND HANDLER ====================
def run_assistant():
    wish_me()

    while True:
        query = listen()

        if not query:
            continue

        # Exit commands
        if any(word in query for word in ["exit", "quit", "stop", "bye", "goodbye"]):
            speak("Goodbye! Have a nice day.")
            break

        # Time
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Date
        elif "date" in query:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        # Wikipedia
        elif "wikipedia" in query or "who is" in query or "what is" in query:
            speak("Searching Wikipedia...")
            search_query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            try:
                result = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Sorry, I could not find information on that.")

        # Open websites
        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "open github" in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")

        elif "open stackoverflow" in query:
            webbrowser.open("https://stackoverflow.com")

        # Play on YouTube
        elif "play" in query:
            song = query.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # Search on Google
        elif "search" in query:
            search_term = query.replace("search", "").strip()
            speak(f"Searching for {search_term}")
            pywhatkit.search(search_term)

        # Jokes
        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Weather (requires free API key from openweathermap.org)
        elif "weather" in query:
            speak("Please tell me the city name")
            city = listen()
            if city:
                try:
                    api_key = "YOUR_OPENWEATHERMAP_API_KEY"   # ← Replace this
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url).json()
                    if response["cod"] == 200:
                        temp = response["main"]["temp"]
                        desc = response["weather"][0]["description"]
                        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}")
                    else:
                        speak("City not found")
                except:
                    speak("Sorry, I couldn't fetch the weather right now.")

        # Take notes
        elif "note" in query or "write" in query:
            speak("What should I write?")
            note = listen()
            if note:
                with open("notes.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {note}\n")
                speak("Note saved successfully")

        # Open applications (Windows)
        elif "open notepad" in query:
            speak("Opening Notepad")
            os.system("notepad")

        elif "open calculator" in query:
            speak("Opening Calculator")
            os.system("calc")

        # System commands
        elif "shutdown" in query:
            speak("Shutting down the system in 10 seconds")
            os.system("shutdown /s /t 10")

        elif "restart" in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 5")

        # Default response
        else:
            speak("Sorry, I didn't understand that command. Please try again.")

# ==================== START ====================
if __name__ == "__main__":
    print("===== Voice Controlled Personal Assistant =====")
    print("Say 'Hey Assistant' or just speak commands after starting")
    run_assistant()
