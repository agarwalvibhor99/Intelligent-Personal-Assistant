import pyttsx3
import speech_recognition as sr #pip3 install speechrecognition
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#brew cask install chromedriver


engine = pyttsx3.init()

def updateRate():
    '''RATE'''
    newRate = input("New Rate: ")
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print ("Current Rate:", rate)                        #printing current voice rate
    engine.setProperty('rate', newRate)     # setting up new voice rate
    print ("New Rate:", engine.getProperty('rate'))

def updateVolume():
    """VOLUME"""
    newVolume = int(input("New Volume: "))
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print ("Current Volume:", volume)                          #printing current volume level
    engine.setProperty('volume',newVolume)    # setting up volume level  between 0 and 1
    print ("New Volume:", engine.getProperty('volume'))

def updateVoice():
    """VOICE"""
    newVoice = int(input("Select 0 for male and 1 for female: "))
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[newVoice].id)   #changing index, changes voices. 1 for female

def searchGoogle(query):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    search = driver.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)

def speechRecog():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        transcript = r.recognize_google(audio, language = 'en-in')
        print(transcript)
        return transcript
    except Exception as e: 
        print("I didn't understand that. Error " + str(e))

    # recognize speech using Sphinx
    # try:
    #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))


def speak(command):
    engine.say(command)
    engine.runAndWait()
    
def stopEngine():
    engine.stop()

def main():
    print("Hi! I'm your Virtual Assistant")
    speak("Hi! I'm your Virtual Assistant. What can I do for you today?")
    print("1. Update Rate\n2. Update Volume\n3. Update Voice\n4. I can repeat what you say\n5. Talk to Me\n6. Quit")

    while(True):
        option = int(input("Please make a selection: "))
        if(option == 1):
            updateRate()
        elif(option == 2):
            updateVolume()
        elif(option == 3):
            updateVoice()
        elif(option == 4):
            command = input("What do you want me to repeat: ")
            speak(command)
        elif(option == 5):
            transcript = speechRecog()
            if('open' in transcript.lower()):
                d = '/Applications'
                apps = list(map(lambda x: x.split('.app')[0], os.listdir(d)))
                print(apps)
                print(transcript) 

                app = transcript.split()[1]
                os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))

            elif("google search" in transcript.lower()):
                print("Transcript: " + transcript)
                transcript = transcript.lower()
                query = transcript.split("google search")[1]
                print("Query: " + query)
                searchGoogle(query)
            
            elif(("quit" or "bye bye" or "bye" or "exit") in transcript.lower()):
                stopEngine()
                exit(0)
            speak(transcript)
        elif(option == 6):
            stopEngine()
            print("See you again!")
            speak("Bye-Bye! See you again!")
            exit(0)
        else:
            print("Invalid Option Try Again")

main()
