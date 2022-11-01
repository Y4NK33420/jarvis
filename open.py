import os
import openai
import pyttsx3


# Load your API key from an environment variable or secret management service
key = ''#enter your key here

query = 'The following is a conversation with a virtual assistant whose name is friday. The assistant is sarcastic, yet helpful.\nHuman: Hi what is your name?\nFriday:'

engine = pyttsx3.init("sapi5") 
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

#defining the speak function and recognize function that are to be used throughout our program
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def clever(query):
    response = openai.Completion.create(model="text-davinci-002", prompt=query, temperature=0.9, max_tokens=130)

    response = response['choices'][0]['text']

    speak(response)

