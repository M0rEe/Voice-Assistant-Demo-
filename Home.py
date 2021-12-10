from posixpath import split, splitext
import speech_recognition as sr  #importing speech recognition module 
import pyttsx3    #importing text to speech module    

engine = pyttsx3.init()     #intiallizing text to speech module to start synthesizing texts
r = sr.Recognizer()            #starting SR module to be able to recognize user "Human" voice 

with sr.Microphone() as source:          #using the default microphone as input device 
    engine.say("Welcome , you can start talking to your voice assistant now ")
    engine.runAndWait()
    print("Welcome , you can start talking to your voice assistant now .\n")
    audio = r.listen(source)

    try:
        text= r.recognize_google(audio)       
        #testing 
        comm = format(text)
        comm = comm.split(" ")      #splitting the user voice to string ,thus making his command 

        print('i heard that : {} is it correct ?'.format(text))
        engine.say('i heard that : {} is it correct ?'.format(text))
        engine.runAndWait()
        """
        if comm[0] == 'joke':
            print('What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.')
            engine.say('What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.')
            engine.runAndWait()///
        """


    except:           #handling the miss hearing of the user if he didnt talk 
        print("I think I miss heard you a little bit")
        engine.say('i think i miss heard you a little bit')
        engine.runAndWait()