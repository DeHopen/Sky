import speech_recognition as sr
import os
import sys
import re
import webbrowser
import requests
import wikipedia
import random
from time import strftime
import pyttsx3
import ctypes
import pywhatkit
import pyautogui
import time
from sky_2 import sistem_stats
import subprocess
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') #даёт подробности о текущем установленном голосе
engine.setProperty('voice', voices[0].id)  # 0-мужской , 1-женский

GREETINGS = ['sky', 'skyline', 'Sky', 'hey sky', 'skype', 'ski', 'time to work sky', 'time to work skype', 'you there sky', 'you there skype', 'wake up sky', 'wake up skype', 'are you there']
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]
HOWAREYOU = ["I am fine, Thank you", "Everything is fine", "Better than ever"]
def SkyResponse(audio):
    engine.say(audio)
    engine.runAndWait()

def myCommand():
    "listens for commands"
    global command
    command = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command
def assistant(command):
    "if statements for executing commands"
    if 'open git' in command:
        reg_ex = re.search('open git (.*)', command)
        url = 'https://github.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        SkyResponse('The Reddit content has been opened for you Sir.')
    elif 'off' in command:
        SkyResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    elif command in GREETINGS:
        SkyResponse(random.choice(GREETINGS_RES))
    elif 'get file' in command:
        subprocess.Popen('explorer "E:\Школа"')
    elif 'get music' in command:
        subprocess.Popen('explorer "E:\Загрузки\Музыка Основа"')
    elif "switch the window" in command or "switch window" in command:
        SkyResponse("Okay sir, Switching the window")
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")
    elif "change language" in command:
        SkyResponse("Okay sir, Change language")
        pyautogui.keyDown("alt")
        pyautogui.press("shift")
        time.sleep(1)
        pyautogui.keyUp("alt")
    elif "unfold window" in command or "unfold old window" in command:
        SkyResponse("Okay sir, Unfolded all windows")
        pyautogui.keyDown("Win")
        pyautogui.press("d")
        time.sleep(1)
        pyautogui.keyUp("Win")
    elif "close app" in command:
        SkyResponse("Okay sir, close app")
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        time.sleep(1)
        pyautogui.keyUp("alt")
    elif "system" in command:
        sistem_stats.system_stats()
    elif "ip address" in command:
        ip = requests.get('https://api.ipify.org').text
        print(ip)
        SkyResponse(f"Your ip address is {ip}")
    elif 'open' in command or 'открой' in command:
        reg_ex = re.search('open (.+)' , command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://' + domain + '.ru'
            webbrowser.open(url)
            SkyResponse('The website you have requested has been opened for you Sir.')
        else:
            pass
    elif 'hello' in command or 'hey sky' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            SkyResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            SkyResponse('Hello Sir. Good afternoon')
        else:
            SkyResponse('Hello Sir. Good evening')
    # joke
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            SkyResponse(str(res.json()['joke']))
        else:
            SkyResponse('oops!I ran out of jokes')
    # top stories from google news
    elif 'random' in command:
        ot = command.find('from')
        do = command.find('before')
        f_num = int(command[ot+3:do-1])
        l_num = int(command[do + 3:])
        r = str(random.randint(f_num, l_num))
        print(r)
        SkyResponse(r)
    # current weather
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        SkyResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    # play youtube song
    elif 'play music' in command or "play song" in command or "go work" in command:
        SkyResponse("Here you go with music")
        music_dir = "E:\Muzic"
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))
    # askme anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                SkyResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            print(e)
            SkyResponse(e)
    elif 'lunch steam' in command or 'launch steam' in command:
        codePath = "C:\Program Files (x86)\Steam\steam.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('I launched Steam')
    elif 'lunch blender' in command or 'launch blender' in command:
        codePath = "E:\SteamLibrary\steamapps\common\Blender\dblender.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('I launched Blender')
    elif 'lunch spotify' in command or 'launch spotify' in command:
        codePath = "C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.164.561.0_x86__zpdnekdrzrea0\Spotify.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('I launched Spotify')
    elif 'lunch telegram' in command or 'launch telegram' in command:
        codePath = "C:\Program Files\WindowsApps\TelegramMessengerLLP.TelegramDesktop_2.8.8.0_x64__t4vj0pshhgkwm\Telegram.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('I launched Telegram')
    elif 'how are you' in command:
        SkyResponse(random.choice(HOWAREYOU))
        SkyResponse("How are you, Sir")

    elif 'fine' in command or "good" in command:
        SkyResponse("It's good to know that your fine")

    elif "what's your name" in command or "What is your name" in command:
        SkyResponse("My friends call me Sky")

    elif 'exit' in command:
        SkyResponse("Thanks for giving me your time")
        exit()
    elif "who made you" in command or "who created you" in command:
        SkyResponse("I have been created by 404")
    elif "why you came to world" in command:
        SkyResponse("Thanks to 404. further It's a secret")
    elif 'is love' in command:
        SkyResponse("It is 7th sense that destroy all other senses")
    elif 'play' in command:
        song = command.replace('play', '')
        SkyResponse('playing' + song)
        pywhatkit.playonyt(song)
    elif "who are you" in command:
        SkyResponse("I am your virtual assistant created by 404")

    elif 'reason for you' in command:
        SkyResponse("I was created as a Minor project by Mister 404")
    elif 'sleep' in command:
        SkyResponse("locking the device")
        ctypes.windll.user32.LockWorkStation()
    elif "write a note" in command:
        SkyResponse("What should i write, sir")
        note = myCommand()
        file = open('jarvis.txt', 'w')
        SkyResponse("Sir, Should i include date and time")
        snfm = myCommand()
        if 'yes' in snfm or 'sure' in snfm:
            file.write(" :- ")
            file.write(note)
        else:
            file.write(note)

    elif "show note" in command:
        SkyResponse("Showing Notes")
        file = open("jarvis.txt", "r")
        print(file.read())
        SkyResponse(file.read(6))


#SkyResponse("Initializing Sky")
#SkyResponse("Starting all systems applications")
#SkyResponse("Installing and checking all drivers")
#SkyResponse("Caliberating and examining all the core processors")
#SkyResponse("Checking the internet connection")
#SkyResponse("Wait a moment sir")
#SkyResponse("All drivers are up and running")
#SkyResponse("All systems have been activated")
#SkyResponse("Now I am online")
#SkyResponse("Please tell me how may I help you")


# loop to continue executing multiple commands
def main_1():
    myCommand()
while True:
    assistant(myCommand())
