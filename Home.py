import speech_recognition as sr  # importing speech recognition module
import pyttsx3  # importing text to speech module
import SendMail as sm
import weather as wz 


def say_print(textstr):
    engine = pyttsx3.init()  # initializing text to speech module to start synthesizing texts
    engine.say(textstr)
    engine.runAndWait()
    print(textstr + "\n")


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
            print("I think I miss heard you a little bit.\n")  # handling the miss hearing of the user if he didn't talk
            # print("Exception " + str(e))

    return text.lower()


# Start
wake_up = "hey google"
print("Started")
while True:
    print("im listening.\n")
    wake_command = waitforaudio()
    if wake_command.count(wake_up) > 0:
        say_print("Welcome , you can start talking to your voice assistant now.")
        textcommand = waitforaudio()
        mail_str = ["send an email", "send email", "send mail", "send a mail"]
        weather_str = ["what about the weather", "how is the weather", "what is the forecast", "what is the weather", "how about the weather"]

        for phrase in mail_str:
            if phrase in textcommand:
                say_print("to whom you want me to sent this email ?,i prefer to write down the email you want\n")
                to = input()
                say_print("what do you want to be the subject of this email ?")
                subject = waitforaudio()
                say_print("what do you want me to write in this email ?")
                body = waitforaudio()
                auth = sm.send_mail_to(to, subject, body)
                say_print(auth)
        
        for phrase in weather_str:
            if phrase in textcommand:
                say_print("what city do you want to know its weather? note:Maximum 8 days ")
                city = waitforaudio()
                say_print("for how many days you wanna know its weather?")
                days_num= int(waitforaudio())
                temp_data = wz.get_waether_condition(city)
                for i in range(days_num):
                    say_print(temp_data[i])


