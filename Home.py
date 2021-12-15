import speech_recognition as sr  # importing speech recognition module
import pyttsx3  # importing text to speech module
import SendMail as sm
import weather as wz
import calnderAPI as cal
import re
import random as rr
#import playsound
import os
from googletrans import Translator
from gtts import gTTS


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
mail_str    = ["send an email", "send email",
            "send mail", "send a mail",
            "can you mail","can you email"]
weather_str = ["what about the weather", "how is the weather",
            "what is the forecast", "what is the weather", 
            "how about the weather", "what is the temprature",
            "should i take my umbrella", "what is the weather forecast",
            "is it cold","is it warm",
            "is it hot","is it raining"]

calendar = ["what do i have","do i have plans","am i busy on"]

Exit = ["exit","bye","see you later"]

rand_number=["pick a random number","choose a random number","random number","tell me any random number"]

translator =["how do i say","translate"]



def say_print(textstr):
    engine = pyttsx3.init()  # initializing text to speech module to start synthesizing texts
    engine.say(textstr)
    engine.runAndWait()
    print(textstr)

def translate_from_english(text,Lang):
    translater=Translator()
    out=translater.translate(text.strip(),dest=Lang)
    print(out)
    out_audio = gTTS(text=out.text,lang=Lang)
    out_audio.save("temp.mp3")
    os.system("temp.mp3")

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
            print("I think I miss heard you a little bit.\n")
            # print("Exception " + str(e))

    return text.lower()


# Start
wake_up = "hey google"
print("Started.")
service = cal.authenticate_google()

while True:
    print("im listening.")
    wake_command = waitforaudio()
    if wake_command == 'exit':
        print("Stopped")
        break 
    if wake_command.count(wake_up) > 0:
        say_print("Welcome , you can start talking to your voice assistant now.")
        textcommand = waitforaudio()
        if textcommand == 'exit':
            print("Stopped")
            break 
        for phrase in calendar :
            if phrase in textcommand:
                date = cal.get_date(textcommand)
                events = cal.get_events(date,service)
                if not events[0] == 'No upcoming events found.':
                    say_print(f'you have {len(events)} events on {date}')

                for event in events: 
                    say_print(event)

        for phrase in mail_str:
            if phrase in textcommand:
                say_print("to whom you want me to sent this email ?,i prefer to write down the email you want")
                to = input()
                if to !="":
                    say_print("what do you want to be the subject of this email ?\n")
                    subject = waitforaudio()
                    say_print("what do you want me to write in this email ?\n")
                    body = waitforaudio()
                    auth = sm.send_mail_to(to, subject, body)
                    say_print(auth)

        for phrase in weather_str:
            if phrase in textcommand:
                say_print("what city do you want to know its weather?\n")
                city = waitforaudio()
                city = city.split(' ')
                say_print("for how many days you wanna know its weather ? note : Maximum 8 days\n")
                days_num = waitforaudio()
                days_num = days_num.split(" ")
                for z in days_num:
                    if z.isdigit():
                        daynum = z
                        break

                temp_data = wz.get_waether_condition(city[0])
                for i in range(int(daynum)):
                    say_print(temp_data[i])

        for phrase in rand_number:
            if phrase in textcommand:
                if re.search("\d+\s\D+\s\d+",textcommand) !=None :
                    temp=re.search("\d+\s\D+\s\d+",textcommand).group().split()
                    say_print(rr.randint(int(temp[0]),int(temp[2])))
                    break
                say_print(rr.randint(0,1000))
                break

        for phrase in translator:
            if phrase in textcommand:
                for j in LANGUAGES:
                    if LANGUAGES[j] in textcommand:
                        textcommand.replace(phrase, '')
                        textcommand= textcommand[0:len(textcommand)-len(LANGUAGES[j])-4]
                        translate_from_english(str(textcommand),str(j))
                        break
                break






