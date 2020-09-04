# -*- coding: utf-8 -*-
import pyttsx3
import playsound
import speech_recognition as sr

def speak(text):
    eng = pyttsx3.init()
    eng.setProperty("rate",140)
    eng.setProperty("volume",1.0)
    listVoices = eng.getProperty("voices")
    eng.setProperty("voice", listVoices[2].id)
    eng.say(text)
    eng.runAndWait()

def listen():
    r = sr.Recognizer()
    palabra = ""
    with sr.Microphone(device_index = 0) as source:
        audio = r.listen(source)
        try:
            palabra = r.recognize_google(audio,language="es")
            print(palabra)
        except Exception as e:
            print("Exception: " + str(e))
    return palabra