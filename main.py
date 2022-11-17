'''
Made by Y4NK33420


Virtual assistant with multitude of functions for personal use and can even utilise open ai 's gpt-3 model to answer
questions which would require thinking.
'''


#these our the initial imports required for our assistant
import pyttsx3
import speech_recognition as sr
import datetime
from googlesearch import search
import os, webbrowser
import pyjokes
import time
import pyautogui
import clipboard
import pytube
import wikipedia
from time import sleep
from threading import Thread
import openai
from open import key,clever #import from file open.py 
import playsound
import requests
import json
import urllib
import re

#here we are initializing the text-to-speech engines and defining its voice
engine = pyttsx3.init("sapi5") 
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
openai.api_key = key


#defining the speak function and recognize function that are to be used throughout our program
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()



def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.RequestError:
        # API was unreachable or unresponsive
            print('cannot reach api at the moment')
        except sr.UnknownValueError:
            # speech was unintelligible
            speak('cannot understand what you said please try again')
            #trying again one more time
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                said = ""

                try:
                    said = r.recognize_google(audio)
                    print(said)
                except Exception as e:
                    print(e)

    return said.lower() # returning the recognised text to the variable assigned

# function for accessing gpt3 model for qna capabilities
#def clever(query):
#
#    response = openai.Completion.create(model="text-davinci-002", prompt=query, temperature=0.9, max_tokens=130)
#
#    response = response['choices'][0]['text']
#
#    speak(response)    


#this is the main function that initiates the required task according to the voice command 
def main_func():
    speak('what would you like to do sir')
    query = recognize()
    # to understand which function is to be used it tries to find certain keywords in speech which correspond to the required functions
    if 'mode' in query:
        speak('clever mode activated')
        query = recognize()
        clever(query)

    elif 'wish' in query:
            wish()

    elif 'google' in query:
        google_search()

    elif 'search' in query:
        wiki()

    elif 'app' in query:
        open_app(query)

    elif 'open' in query and 'youtube' in query:
            open_youtube()

    elif 'open' in query and 'site' in query:
            open_site()
    
    elif 'music' in query:
            play_music()

    elif 'pause' in query:
        pause()

    elif 'jokes' in query or "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
    
    elif 'type' in query:
        type()
    
    elif 'location' in query:
        location()

    elif 'time' in query:
        speak(f'The time is {datetime.datetime.now().hour} {datetime.datetime.now().minute} ')

    elif 'download' in query and 'video' in query:
        download_vid()

    elif 'anime' in query or 'boruto' in query:
        webbrowser.open('https://zoro.to/watch/boruto-naruto-next-generations-8143')

    #the timer function is defined inside main function itself so that user doesn't have to speak the time again
    #it extracts the time from the first prompt itself instead of telling user to say it again
    elif 'timer' in query:
        minutes,seconds = 0,0
        if 'for' in query:
            time_slot = list(query.split())
            for word in time_slot:
                if word == 'minutes':
                    minutes = int(time_slot[time_slot.index('minutes') - 1])
                elif word == 'minute':
                    minutes = int(time_slot[time_slot.index('minute') - 1])
                
                if word == 'seconds':
                    seconds = int(time_slot[time_slot.index('seconds') - 1])
                elif word == 'second':
                    seconds = int(time_slot[time_slot.index('second') - 1])
            
            tm = minutes*60 + seconds + 1
            speak(f'Timer set for {minutes} minutes and {seconds} seconds')
            #activating the timer in a seperate thread so that our program can keep runnning while the timer is on
            thread = Thread(target=timer,args=(tm,'time up'))
            thread.start()  
        else:
            #if user doesn't speak the time in the first prompt we can ask him again
            speak('For how much time sir?')
            tme = recognize()
            time_slot = list(tme.split())
            for word in time_slot:
                if word == 'minutes':
                    minutes = int(time_slot[time_slot.index('minutes') - 1])
                elif word == 'minute':
                    minutes = int(time_slot[time_slot.index('minute') - 1])
                if word == 'seconds':
                    seconds = int(time_slot[time_slot.index('seconds') - 1])
                elif word == 'second':
                    seconds = int(time_slot[time_slot.index('second') - 1])            
            tm = minutes*60 + seconds + 1
            speak(f'Timer set for {minutes} minutes and {seconds} seconds')
            thread = Thread(target=timer,args=(tm,'time up'))
            thread.start()

    elif 'time' in query:
        if datetime.datetime.now().hour > 12:
            speak(f'The time is {int(datetime.datetime.now().hour) - 12} {datetime.datetime.now().minute} ')
        else:
            speak(f'The time is {datetime.datetime.now().hour} {datetime.datetime.now().minute} ')

    else:
        #if the user said a function which is not yet present we can close the loop after asking if there is anything else we can do
            speak('your request cannot be executed right now our developers will add the functionality soon')
            speak('is there anything else you would like to do')
            response = recognize()
            if 'yes' in response:
                main_func()
            else:
                speak('thank you for using me')
                #after this the assistant goes back into listening mode until the wake word is announced  
                  

#defining various functions for our assistant

# timer(890, 'wake up')
def timer(time,msg):
    '''
    This is the timer function to be used in a seperate thread
    
    Parameters: 
    time(int): time for which the timer will run in seconds
    msg(str): msg which needs to be printed after the time is up

    Returns:
    None
    '''
    sleep(time)
    print(msg)
    playsound.playsound('alarm.wav')

def wish():
    """wishes the user on the basis of the current time of the day
    """    
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 0 and hour < 12 :
        speak('good morning')
    elif hour >= 12 and hour < 15:
        speak('good afternoon')
    else:
        speak('good evening')    

def find_link(name):
    query = name.split(' ')
    srch = ''
    for i in query:
        srch = srch+'+'+i
    srch = srch[1:]
    print(srch)
    url = str(f'https://www.youtube.com/results?search_query={srch}')
    url = url.encode('ascii', 'ignore').decode('ascii')

    html = urllib.request.urlopen(url)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    return ('https://www.youtube.com/watch?v='+video_ids[0])

def yt_full():
    pass

def wiki():
    """searches for anything on wikipedia after getting voice input from the user
    """    
    speak('what do you want to search sir')
    query = recognize()
    result = wikipedia.summary(query, sentences = 3)   
    speak(result)

def location():
        speak("Wait, let me check")
        try:
            send_url = "http://api.ipstack.com/check?access_key=8e00f15add44e5b7834c7c76bc2dd6b3"
            geo_req = requests.get(send_url)
            geo_json = json.loads(geo_req.text)
            city = geo_json['city']
            country = geo_json['country_name']
            state = geo_json['region_name']
            speak(f'We are in {country},{state},{city}')
        except Exception as e:
            speak("Sorry due to network issue i am not able to find where we are.")

def play_music():
    """plays music from spotify by opening spotify from your computer and pressing the play button to play the most
    recently played song
    """    
    os.startfile(r"D:\Spotify\Spotify.exe")
    speak('Which song')
    query = recognize()
    time.sleep(5)
    pyautogui.hotkey('ctrl','l')
    time.sleep(1)
    pyautogui.write(query)
    time.sleep(1)
    pyautogui.moveTo(786,380)
    pyautogui.click()
    time.sleep(1)
    img = pyautogui.screenshot()
    pt = pyautogui.find_img(img,"D:\python projects\projects\content\playbutton.png")
    try:
        pyautogui.click(pt)
    except Exception as e:
        pass
    pyautogui.hotkey('alt','tab')

def pause():
    """pauses the currently playing media
    """    
    pyautogui.press('playpause')

def download_vid():
    """downloads the current video by getting link from browser's query box and downloading it using pytube
    """    
    pyautogui.moveTo(489,61)
    pyautogui.click()
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    url = clipboard.paste()
    yt = pytube.YouTube(url)
    speak('fetching data...')
    my_stream = yt.streams.get_highest_resolution()
    speak('downloading...')
    my_stream.download(output_path="D:\Downloads")
    speak('done')


def search_func():
    """Fully voice automated search. Searches for a query on google and gets the first ten queries out of which user can choose which one to visit 
     it then opens up the required webpage in your default browser
    """    
    speak('what do you want to search sir')
    query = recognize()

    results = search(query,tld ='com',num = 10,stop = 10, pause = 2)
    
    results1 = []

    for i in results:
        print(i)
        results1.append(str(i))

    speak('whcih result would you like to visit?')
   
    web_index = recognize()
    dict1 = {'first':0,'second':1,'third':2,'fourth':3,'fifth':4,'sixth':5,'seventh':6,'eight':7,'ninth':8,'tenth':9}
    try:
        index_req = dict1[web_index]
    except KeyError as k:
        index_req = 1
    
    webbrowser.open(results1[index_req])

def google_search():
    """searches google for a particular query and opens up google search in your browser
    """    
    speak('what would you like to search sir')
    query = recognize()
    webbrowser.open(f'https://google.com/search?q={query}')
    speak('This is what i found sir')

def type():
    speak('start speaking sir')
    txtprev = ''
    while 1:
        txt = get_audio()
        if 'terminate' in txt:
            speak('should i save it?')
            wtd = recognize()
            if 'yes' in wtd:
                speak('What should be the filename?')
                file_name = recognize()
                pyautogui.hotkey('ctrl','s')
                pyautogui.write(file_name)
                pyautogui.press('enter')
                pyautogui.hotkey('alt','f4')
                break
            else:
                pyautogui.hotkey('ctrl','w')
                pyautogui.press('right')
                pyautogui.press('enter')
                break
        elif 'done' in txt:
            break
        elif 'delete that' in txt:
            pyautogui.press('backspace',presses = int(len(txtprev) + 1))
        elif 'next line' in txt:
            pyautogui.press('enter')
        else:
            pyautogui.write(f'{txt} ')
        txtprev = txt

def open_app(query):
    """opens up your required app through cmd.
    Does not work for apps that cmd doesn't recognize
    """    
    try:
        app = str(query.split(' ')[2])
        print(app)
        pyautogui.hotkey('win','s')
        time.sleep(0.2)
        pyautogui.write(app)
        time.sleep(0.2)
        pyautogui.press('enter')
    except IndexError as e:
        speak('which app')
        app = recognize()
        pyautogui.hotkey('win','s')
        time.sleep(0.2)
        pyautogui.write(app)
        time.sleep(0.2)
        pyautogui.press('enter')
    
    else:
        os.system(query)


def open_youtube():
    """opens youtube in your browser
    """    
    webbrowser.open('www.youtube.com')

def open_site():
    """opens up any site in browser using its url
    """    
    speak('which website would you like to open')
    query = recognize()
    webbrowser.open(query)


def move_mouse(direction):
    """moves mouse in the specified direction by 100 pixels

    Args:
        direction (str): direction in which you want to nmove your cursor
    """
    if direction == 'up':
        pyautogui.moveRel(0,-100)
    elif direction == 'down':
        pyautogui.moveRel(0,100)
    elif direction == 'right':
        pyautogui.moveRel(100,0)
    elif direction == 'left':
        pyautogui.moveRel(-100,0)
    
def get_audio():
    """recognising function for the main loop which keeps running infinitely

    seperate from the recognize function which tells if it has understood what you said and retries once more.
    it is built for running at short intervals without giving any error whatsoever

    Returns:
        str: returns the recognised text if any
    """    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            pass

    return said.lower()


#this is the mainloop which allows our assistant to run 24/7 in the background
WAKE = "friday"#wake word for the assistant after listening which it will activate
def mainloop():
    #initially wishes the user
    speak('welcome yankee')
    wish()
    speak('how has your day been going')
    while True:
        #main loop which runs infintely in the background until program is closed manually or using the exit voice command
        ctext = get_audio()
        #checking for wake word
        if ctext.count(WAKE) > 0:
            main_func()
        #checking for mouse commands
        elif 'move' in ctext:
            if 'up' in ctext:
                move_mouse('up')
            elif 'left' in ctext:
                move_mouse('left')
            elif 'right' in ctext:
                move_mouse('right')
            elif 'down' in ctext:
                move_mouse('down')
            else:
                speak('please specify the direction')

        elif 'play' in ctext or 'pause' in ctext:
            pause()
        elif 'click' in ctext:
            pyautogui.click()
        #checking for exit or quit in query which if present will break the while loop and close the program
        elif 'exit' in ctext or 'quit' in ctext:
            break

                
# traditional name check to ensure that mainloop doesn't work if functions of this program are imported elsewhere            
if __name__ == '__main__':
    mainloop()







