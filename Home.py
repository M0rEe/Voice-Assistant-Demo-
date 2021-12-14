import speech_recognition as sr  # importing speech recognition module
import pyttsx3  # importing text to speech module
import SendMail as sm
import weather as wz
import calnderAPI as cal


mail_str = ["send an email", "send email",
            "send mail", "send a mail",
            "can you mail","can you email"]

weather_str = ["what about the weather", "how is the weather",
            "what is the forecast", "what is the weather", 
            "how about the weather", "what is the temprature",
            "should i take my umbrella", "what is the weather forecast",
            "is it cold","is it warm",
            "is it hot","is it raining"]

calendar = ["what do i have",
            "am i busy on"]



def say_print(textstr):
    engine = pyttsx3.init()  # initializing text to speech module to start synthesizing texts
    engine.say(textstr)
    engine.runAndWait()
    print(textstr)


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
print("Started\n")
service = cal.authenticate_google()

while True:
    print("im listening.\n")
    wake_command = waitforaudio()
    if wake_command.count(wake_up) > 0:
        say_print("Welcome , you can start talking to your voice assistant now.\n")
        textcommand = waitforaudio()
        for phrase in calendar :
            if phrase in textcommand:
                date = cal.get_date(textcommand)
                say_print("you have on")
                say_print(date)
                events = cal.get_events(date,service)
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
