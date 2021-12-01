import speech_recognition as sr
import os
import sys
import re
import webbrowser
import requests
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
recognition_language = "ru-RU"
engine.setProperty('voice', voices[0].id)  # 0-мужской , 1-женский

GREETINGS = ['sky', 'skyline', 'Sky', 'hey sky', 'skype', 'скай', 'time to work sky', 'время работать скай', 'you there sky', 'ты здесь скай', 'wake up sky', 'проснись скай', 'ты тут']
GREETINGS_RES = ["Всегда рядом с вами, Сэр", "Я готов, Сэр",
                 "Ваше желание - мой приказ", "Чем я могу вам помочь, Сэр?", "Я в сети и готов, Сэр"]
HOWAREYOU = ["Я в порядке, спасибо", "Все хорошо", "Лучше, чем когда-либо"]
def SkyResponse(audio):
    engine.say(audio)
    engine.runAndWait()

def myCommand():
    "listens for commands"
    global command
    command = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Скажите что-то...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print('Вы сказали: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command
def assistant(command):
    "if statements for executing commands"
    if 'открой git' in command:
        reg_ex = re.search('открой git (.*)', command)
        url = 'https://github.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        SkyResponse('Содержимое Reddit было открыто для вас, Сэр.')
    elif 'выключись' in command or 'на сегодня все' in command:
        SkyResponse('До свидания, Сэр. Хорошего дня')
        sys.exit()
    elif command in GREETINGS:
        SkyResponse(random.choice(GREETINGS_RES))
    elif 'перейди в дерикторию школа' in command:  #впиши сюда дерикторию которую хочеш чтоб открывала
        subprocess.Popen('explorer "E:\Школа"')    #впиши путь к этой папке
    elif 'перейди в музыку' in command:
        subprocess.Popen('explorer "E:\Загрузки\Музыка Основа"')
    elif "поменяй окно" in command or "смени окно" in command:
        SkyResponse("Хорошо, Сэр, переключаю окно")
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")
    elif "сверни все окна" in command or "разверни все окна" in command:
        SkyResponse("Хорошо, Сер")
        pyautogui.keyDown("Win")
        pyautogui.press("d")
        time.sleep(1)
        pyautogui.keyUp("Win")
    elif "поменяй язык" in command:
        SkyResponse("Хорошо, Сэр, сменила язык")
        pyautogui.hotkey('alt', 'shift')
    elif "закрой приложение" in command:
        SkyResponse("Хорошо, Сэр, закрыла приложение")
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        time.sleep(1)
        pyautogui.keyUp("alt")
    elif "система" in command:
        sistem_stats.system_stats()
    elif "мой ip" in command:
        ip = requests.get('https://api.ipify.org').text
        print(ip)
        SkyResponse(f"Ваш ip-адрес {ip}")
    elif 'открой' in command:
        reg_ex = re.search('открой (.+)' , command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://' + domain + '.ru'
            webbrowser.open(url)
            SkyResponse('Веб-сайт, который вы запросили, был открыт для вас, Сэр.')
        else:
            pass
    elif 'привет' in command or 'привет скай' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            SkyResponse('Здравствуйте, сэр. Доброе утро')
        elif 12 <= day_time < 18:
            SkyResponse('Здравствуйте, сэр. Добрый день')
        else:
            SkyResponse('Здравствуйте, сэр. Добрый вечер')
    # top stories from google news
    elif 'случайное число' in command:
        ot = command.find('от')
        do = command.find('до')
        f_num = int(command[ot+3:do-1])
        l_num = int(command[do + 3:])
        r = str(random.randint(f_num, l_num))
        print(r)
        SkyResponse(r)
    # current weather
    elif 'сколько время' in command:
        import datetime
        now = datetime.datetime.now()
        SkyResponse('Текущее время составляет %d часов %d минут' % (now.hour, now.minute))
    # play youtube song
    elif 'включи музыку' in command or "за работу sky" in command:
        SkyResponse("Приятно вас видеть за работой, Сер")
        music_dir = "E:\Muzic"   #вписи дерикторию с музыкой
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))
    # askme anything
    elif 'запусти steam' in command:
        codePath = "C:\Program Files (x86)\Steam\steam.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('Я запустила Steam')
    elif 'запусти blender' in command:
        codePath = "E:\SteamLibrary\steamapps\common\Blender\dblender.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('Я запустила Blender')
    elif 'запусти spotify' in command:
        codePath = "C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.164.561.0_x86__zpdnekdrzrea0\Spotify.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('Я запустила Spotify')
    elif 'запусти telegram' in command:
        codePath = "C:\Program Files\WindowsApps\TelegramMessengerLLP.TelegramDesktop_2.8.8.0_x64__t4vj0pshhgkwm\Telegram.exe"  # путь к приложению
        os.startfile(codePath)
        SkyResponse('Я запустила Telegram')
    elif 'как ты' in command:
        SkyResponse(random.choice(HOWAREYOU))
        SkyResponse("Как у вас дела, Сер?")

    elif 'отлично' in command or "хорошо" in command:
        SkyResponse("Приятно знать, что у тебя все в порядке")

    elif "как тебя зовут" in command:
        SkyResponse("Мои друзья зовут меня Скай")

    elif 'выйти' in command:
        SkyResponse("Спасибо, что уделили мне свое время")
        exit()
    elif "кто тебя создал" in command:
        SkyResponse("Я был создан 404")
    elif 'любовь это' in command:
        SkyResponse("Это 7-е чувство, которое уничтожает все остальные чувства")
    elif 'проиграй' in command:
        song = command.replace('проиграй', '')
        SkyResponse('проигрываю' + song)
        pywhatkit.playonyt(song)
    elif "ты кто" in command:
        SkyResponse("Я ваш виртуальный помощник, созданный 404")

    elif 'reason for you' in command:
        SkyResponse("Я был создан как голосовой помощник для помощи 404")
    elif 'спящий режим' in command:
        SkyResponse("Устройство заблокированно")
        ctypes.windll.user32.LockWorkStation()

# loop to continue executing multiple commands
def main_1():
    myCommand()
while True:
    assistant(myCommand())
