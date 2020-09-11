import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files
import subprocess
import bs4 as bs
import urllib.request
import requests

class person:
    name = ''
    def setName(self, name):
        self.name = name

class asis:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio(ask=""):
    with sr.Microphone() as source: # microphone as source
        if ask:
            engine_speak(ask)
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print("Terminé de escucharte fuerte y claro")
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio,language="es-PE")  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            engine_speak('No te escuché bien')
            return record_audio("Repítelo, porfavor")
        except sr.RequestError:
            engine_speak('Disculpa, el servidor se cayó') # error: recognizer is not connected
        print(">>", voice_data.lower()) # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def engine_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='es') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(asis_obj.name + ":", audio_string) # print what app said
    os.remove(audio_file) # remove audio file

def respond(voice_data):
    # 1: greeting
    for term in ['hey','hola','aló']:
        if term in voice_data:
            greetings = ["hola, ¿cuál es tu nombre?" +"hola, ¿cómo estás?" + person_obj.name, "hola, ¿qué tal?" + person_obj.name, "hola" + person_obj.name]
            greet = greetings[random.randint(0,len(greetings)-1)]
            engine_speak(greet)

    # 2: name
    for term in ["cuál es tu nombre","cómo te llamas","dime tu nombre"]:
        if term in voice_data:
            if person_obj.name:
                engine_speak(f"Mi nombre es {asis_obj.name}, gusto en conocerte, {person_obj.name}") #gets users name from voice input
            else:
                engine_speak(f"Me llamo {asis_obj.name}. y tú como te llamas?") #incase you haven't provided your name.

    if "mi nombre es" in voice_data:
        person_name = voice_data.split("es")[-1].strip()
        engine_speak("está bien, voy a recordar eso " + person_name)
        person_obj.setName(person_name) # remember name in person object
    
    for term in ["cuál es mi nombre","cómo me llamo"]:
        if term in voice_data:
            engine_speak("Esa es facil. Tu eres " + person_obj.name)
    
    if "ahora te llamas" in voice_data:
        asis_name = voice_data.split("llamas")[-1].strip()
        engine_speak("está bien, recordaré que mi nombre ahora es " + asis_name)
        asis_obj.setName(asis_name) # remember name in asis object

    # 3: greeting
    for term in ["cómo estas","qué tal la estas pasando"]:
        if term in voice_data:
            engine_speak("estoy muy bien, gracias por preguntar " + person_obj.name)

    # 4: search google
    for term in ["busca en google","buscar en google"]:
        if 'youtube' not in voice_data:
            if term in voice_data:
                search_term = voice_data.split("google")[-1]
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
                engine_speak("Esto es lo que encontre acerca de " + search_term + "en google")
    
    if ("quiero saber que es " in voice_data) and ('youtube' not in voice_data):
        search_term = voice_data.replace("es","")
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Esto es lo que encontre sobre " + search_term + "en google")

    # 5: search youtube
    if "youtube" in voice_data:
        search_term = voice_data.split("busca")[-1]
        search_term = search_term.replace("en youtube","").replace("busca","")
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        engine_speak("Esto es lo que encontre sobre " + search_term + "en youtube")

     #6: get stock price
    if "precio del " in voice_data:
        search_term = voice_data.split("del")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Esto es lo que encontre para " + search_term + " en google")
    
    
     #7 weather
    if "clima" in voice_data:
        search_term = voice_data.split("clima")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        engine_speak("Este es el clima hoy")
     

     #8 stone paper scisorrs
    if "jugar" in voice_data:
        voice_data = record_audio("escoge entre piedra, papel o tijeras")
        moves=["piedra", "papel", "tijeras"]
    
        cmove=random.choice(moves)
        pmove=voice_data
        

        engine_speak("elegí " + cmove)
        engine_speak("Tu elegiste " + pmove)

        if pmove==cmove:
            engine_speak("hemos empatado")
        elif pmove== "piedra" and cmove== "tijeras":
            engine_speak("Tu ganaste")
        elif pmove== "piedra" and cmove== "papel":
            engine_speak("Yo gané")
        elif pmove== "papel" and cmove== "piedra":
            engine_speak("Tu ganaste")
        elif pmove== "papel" and cmove== "tijeras":
            engine_speak("Yo gané")
        elif pmove== "tijeras" and cmove== "papel":
            engine_speak("Tu ganaste")
        elif pmove== "tijeras" and cmove== "piedra":
            engine_speak("Yo gané")

     #9 toss a coin
    for term in ["tira","gira","moneda"]:
        if term in voice_data:
            moves=["cara", "sello"]   
            cmove=random.choice(moves)
            engine_speak("Salió " + cmove)

     #10 calc
    for term in ["multiplica","+","menos","por","entre","al"]:
        if term in voice_data:
            opr = voice_data.split()[1]

            if opr == '+':
                engine_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
            elif opr == 'menos':
                engine_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
            elif (opr == 'multiplica') or (opr=='por'):
                engine_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
            elif opr == 'entre':
                engine_speak(int(voice_data.split()[0])/int(voice_data.split()[2]))
            elif opr == 'al':
                engine_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
            else:
                engine_speak("Operador Incorrecto")

    for term in ["salir", "apagar", "adiós","hasta pronto", "chau","hasta luego"]:
        if term in voice_data:
            engine_speak("nos vemos")
            exit()



time.sleep(1)

person_obj = person()
asis_obj = asis()
asis_obj.name = 'jarvis'
person_obj.name = ""
respond("dónde estoy")