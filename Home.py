import speech_recognition as sr  # importing speech recognition module
import pyttsx3  # importing text to speech module
import SendMail as sm
import weather as wz
import calnderAPI as cal
import pywhatkit as kit


mail_str    = ["send an email", "send email",
            "send mail", "send a mail",
            "can you mail","can you email"]

weather_str = ["what about the weather", "how is the weather",
            "what is the forecast", "what is the weather", 
            "how about the weather", "what is the temprature",
            "should i take my umbrella", "what is the weather forecast",
            "is it cold","is it warm",
            "is it hot","is it raining"]

calendar    = ["what do i have","do i have plans"
            "am i busy on"]

Exit        = ["exit","bye","see you later"]

search          = ["search on youtube","play a video from youtube",
                "i want to listen to","can you search for me"]



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
print("Started.")
#getting user google credentials file for the calnder commands
service = cal.authenticate_google()

flag_exit = False

while True:
    print("im listening.")
    wake_command = waitforaudio()
    for ext in Exit:
        if ext in wake_command :
            print("Stopped")
            flag_exit = True
            break 
    if flag_exit:
        break

    if wake_command.count(wake_up) > 0:
        say_print("Welcome ,")
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
                    say_print("what do you want to be the subject of this email ?")
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
                say_print("for how many days you wanna know its weather ? note : Maximum 8 days.")
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

