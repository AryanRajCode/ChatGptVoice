import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import webbrowser
from openai import OpenAI
import wikipedia

client = OpenAI(api_key="Open Ai chat gpt api here")
class Kape:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.stop_listening = False  # Flag to control when to stop taking commands

    def talk(self, text):
        """Speak the given text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print('Listening...')
                    voice = self.listener.listen(source)
                    command = self.listener.recognize_google(voice).lower()
                    if any(phrase in command for phrase in ['kape', 'hey kape', 'cape', 'kapee', 'kap', 'keep']):
                        print(command)
                        command = command.replace('kape', '').replace('hey', '').replace('cape', '').replace("keep","").strip()
                        return command
                    elif 'stop' in command:
                        self.stop_listening = True
                        return None
                    else:
                        print("Sorry, I didn't catch that. Please try again.")
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Please try again.")
            except sr.RequestError:
                print("Could not request results. Check your internet connection.")

    def run(self):
        """Main loop to process voice commands."""
        while not self.stop_listening:
            command = self.take_command()
            if command:
                print(command)
                if 'stop' in command:
                    self.stop_listening = True
                elif 'play' in command:
                    song = command.replace('play', '').strip()
                    self.talk(f'Playing {song}')
                    pywhatkit.playonyt(song)
                elif 'time' in command:
                    self.talk(f'Current time is {self.get_current_time_in_india()}')
                elif 'date' in command:
                    self.talk(f"Current date in {self.get_current_date_in_india()}")
                elif 'joke' in command:
                    self.talk(pyjokes.get_joke())
                elif "who made you" in command:
                    self.talk("Aryan Made Me")
                elif "what's your name" in command:
                    self.talk("My Name Is Kape")
                elif "wikipedia" in command:
                    summary = wikipedia.summary("Python", sentences=2)
                    self.talk(summary)
                elif "open" in command:
                    try: 
                        command = command.replace("open", '').strip()
                        if not (command.endswith("in") or command.endswith("com")):
                                command = f'{command}.com'
                        else:
                            pass        
                        webbrowser.open(command)
                    except Exception as e:
                        self.talk("I can't do that at this time. Error: " + str(e))


                else:
                    
                    messages = [{"role": "system", "content": "You are a Kape"}]
                    messages.append({"role": "user", "content": command})
                    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
                    reply = chat.choices[0].message.content
                    print(f"Kape: {reply}")
                    self.talk(reply)
                    messages.append({"role": "assistant", "content": reply})

    def get_current_time_in_india(self):
        india_time_zone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        current_time = datetime.datetime.now(tz=india_time_zone)
        formatted_time = current_time.strftime("%H:%M")
        return formatted_time

    def get_current_date_in_india(self):
        india_date_zone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        current_date = datetime.datetime.now(tz=india_date_zone)
        formatted_date = current_date.strftime("%D")
        return formatted_date

if __name__ == "__main__":
    kape = Kape()
    kape.run()
