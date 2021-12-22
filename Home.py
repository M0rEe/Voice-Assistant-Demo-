import pygame as pygame
import speech_recognition as sr  # importing speech recognition module
import pyttsx3  # importing text to speech module
import SendMail as sm
import weather as wz
import calnderAPI as cal

import pywhatkit as kit
import datetime
import pyautogui as gui
import pyjokes

import re
import random as rr
from random import choice

#import playsound
import os
from googletrans import Translator
from gtts import gTTS

#you can solve the mutli time say hey google with flag to keep him hearing in a loop 
#its not the best solution but can do the thing

pygame.mixer.init()
Music_list=["sway.mp3","Love Me Like You Do.mp3","Perfect.mp3","No Promises.mp3","Its You.mp3","Easy On Me.mp3","Someone Like You.mp3","Hello.mp3"]


LANGUAGES = {
    'af': 'afrikaans',
    'ar': 'arabic',
    'hy': 'armenian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'hi': 'hindi',
    'hu': 'hungarian',
    'is': 'icelandic',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'km': 'khmer',
    'ko': 'korean',
    'la': 'latin',
    'lv': 'latvian',
    'mk': 'macedonian',
    'ml': 'malayalam',
    'mr': 'marathi',
    'no': 'norwegian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sr': 'serbian',
    'si': 'sinhala',
    'sk': 'slovak',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'vi': 'vietnamese',
    'cy': 'welsh'
}

mail_str = ["send an email", "send email",
            "send mail", "send a mail",
            "can you mail", "can you email"]
weather_str = ["what about the weather", "how is the weather",
               "what is the forecast", "what is the weather",
               "how about the weather", "what is the temprature",
               "should i take my umbrella", "what is the weather forecast",
               "is it cold", "is it warm",
               "is it hot", "is it raining"]

calendar = ["what do i have", "do i have plans", "am i busy on"]

Exit = ["exit", "bye", "see you later"]

rand_number = ["pick a random number", "choose a random number",
               "random number", "tell me any random number"]

translator = ["how do i say", "translate"]

shots = ["screenshot", "take a screen", "shot the screen"]

joke = ["tell me a joke", "tell me something funny", "make me laugh"]

search = ["search on youtube", "play a video from youtube",
          "i want to listen to", "can you search for me"]

random_music = ["turn some music","play songs","play a song","I want to listen to some songs"]
stopmusic_msg = ["stop now","stop it","it's okey","stop"]

time_ask = ["what time is it", "do you have the time",
            "have you got the time", "what is the time"]

definitions  = ["what are you", "who are you",
             "introduce yourself","who created you",
             "your name","may i have your name"]
settingslst = ["change setting" , "change settings",
                "edit settings","modify settings"]

comms = ["what can you do" , "what is your things",
         "i bet you can't do","what's your commands"]
             
program_name = "Dave"

def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        say_print("Good Morning !")

    elif hour >= 12 and hour < 18:
        say_print("Good Afternoon !")

    else:
        say_print("Good Evening !")


engine = pyttsx3.init()  # initializing text to speech module to start synthesizing texts
def say_print(textstr):
    engine.say(textstr)
    engine.runAndWait()
    print(textstr)


def translate_from_english(text, Lang):
    translater = Translator()
    out = translater.translate(text.strip(), dest=Lang)
    print(out)
    out_audio = gTTS(text=out.text, lang=Lang)
    out_audio.save("temp.mp3")
    os.system("temp.mp3")

def change_settings():
    voices = engine.getProperty('voices')
    if  engine.getProperty('voice') == voices[0].id :       #getting details of current voice
        engine.setProperty('voice', voices[1].id)   #changing index, changes voices. o for male
    else:
        engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female

def waitforaudio():
    r = sr.Recognizer()  # starting SR module to be able to recognize user "Human" voice
    with sr.Microphone() as source:  # using the default microphone as input device
        audio = r.listen(source)
        text = ""
        try:
            text = r.recognize_google(audio)
            print(text)
            # testing
        except Exception:
            # handling the miss hearing of the user if he didn't talk
            print("I think I miss heard you a little bit.")
            # print("Exception " + str(e))

    return text.lower()


# Start
wake_up = "hey google"
print("Started.")
# getting user google credentials file for the calnder commands
service = cal.authenticate_google()
counter = 00
flag_exit = False
time2 = str(datetime.datetime.now().hour) + ":" + \
    str(datetime.datetime.now().minute)
loop_handler = 0

while True:
    if loop_handler == 0:
        print("im listening.")
        wake_command = waitforaudio()

    if flag_exit:
        break

    if wake_command.count(wake_up) > 0 or loop_handler == 1:
        if loop_handler == 0:
            loop_handler = 1
            greetings()
        else:
            print("awating commands")

        textcommand = waitforaudio()
        for phrase in Exit:
            if phrase in textcommand :
                print("Stopped")
                flag_exit = True
                break

        for phrase in calendar:
            if phrase in textcommand:
                date = cal.get_date(textcommand)
                events = cal.get_events(date, service)
                if not events[0] == 'No upcoming events found.':
                    say_print(f'you have {len(events)} events on {date}')
                for event in events:
                    say_print(event)

        for phrase in mail_str:
            if phrase in textcommand:
                say_print(
                    "to whom you want me to sent this email ?,i prefer to write down the email you want")
                to = input()
                if to != "":
                    say_print(
                        "what do you want to be the subject of this email ?")
                    subject = waitforaudio()
                    say_print("what do you want me to write in this email ?")
                    body = waitforaudio()
                    auth = sm.send_mail_to(to, subject, body)
                    say_print(auth)

        for phrase in weather_str:
            if phrase in textcommand:
                say_print("what city do you want to know its weather?")
                city = waitforaudio()
                city = city.split(' ')
                say_print(
                    "for how many days you wanna know its weather ? note : Maximum 8 days.")
                days_num = waitforaudio()
                days_num = days_num.split(" ")
                for z in days_num:
                    if z.isdigit():
                        daynum = z
                        break

                temp_data = wz.get_waether_condition(city[0])
                for i in range(int(daynum)):
                    say_print(temp_data[i])

        for phrase in search:
            if phrase in textcommand:
                say_print("what video you want me to search for on youtube ?")
                title = waitforaudio()
                kit.playonyt(title)

        for phrase in random_music:
            if phrase in textcommand:
                say_print("Here you go with music")
                Song = choice(Music_list)
                pygame.mixer.music.load(Song)
                pygame.mixer.music.play()

        for phrase in stopmusic_msg:
            if phrase in textcommand:
               pygame.mixer.music.stop()

        for phrase in time_ask:
            if phrase in textcommand:
                say_print(f'time now is {time2}')

        for phrase in shots:
            if phrase in textcommand:
                screenshot = gui.screenshot()
                screenshot.save(f'./screenshot{counter}.png')
                counter += 1
                say_print(
                    f"i took a screenshot as you said and saved it to the project folder with the name screenshot{counter}.png")

        for phrase in rand_number:
            if phrase in textcommand:
                if re.search("\d+\s\D+\s\d+", textcommand) != None:
                    temp = re.search(
                        "\d+\s\D+\s\d+", textcommand).group().split()
                    say_print(rr.randint(int(temp[0]), int(temp[2])))
                    break
                say_print(rr.randint(0, 1000))
                break

        for phrase in translator:
            if phrase in textcommand:
                for j in LANGUAGES:
                    if LANGUAGES[j] in textcommand:
                        textcommand.replace(phrase, '')
                        textcommand = textcommand[0:len(
                            textcommand)-len(LANGUAGES[j])-4]
                        translate_from_english(str(textcommand), str(j))
                        break
                break

        for phrase in joke:
            if phrase in textcommand:
                say_print(pyjokes.get_joke())

        for phrase in definitions:
            if phrase in textcommand:
                say_print(f"my name is {program_name} and iam an voice assistant made for dsp project in 2021 with some simple commands ")
        

        for phrase in comms:
            if phrase in textcommand:
                say_print(' 1 i can send an email for you. \n\
                            2 i can tell you how is the weather forecast for some days. \n\
                            3 i can play music on youtube. \n\
                            4 i can read your events on google calender. \n\
                            5 i can tell you a joke. \n\
                            6 i can translate. \n\
                            7 i can role a random number. \n\
                            8 i can take a screenshot of your screen when you say u want **\n\
                            9 you can edit some settings in my code.')

        for phrase in settingslst:
            if phrase in textcommand:
                say_print("what settings do you want me to change for you ? ")
                changes = waitforaudio()
                if "your name" in changes:
                    say_print("What do you want to call me?")
                    program_name = waitforaudio()
                elif "your gender" in changes:
                    change_settings()
                    say_print("is this tone better for now ?")
