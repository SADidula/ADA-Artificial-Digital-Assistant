import random
import json
import pickle
import numpy as np
import sys
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import nltk
import winsound
import subprocess
import platform

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

engine=pyttsx3.init('sapi5')
engine.setProperty('rate', 180)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

searchQ_list = ['for', 'about', 'on']
w5_list = ['what','when','where','which','who','whom','whose','why','how']
alarm_hour_sq = ['in', 'for']
alarm_time_sq = ['at', 'till']

absolute_paths = json.loads(open('absolute_paths_softwares.json').read())
memory_read = json.loads(open('memory.json', 'r+').read())

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model("advance_ai.model")

ai_name = memory_read['memory'][2]['ai']

jarvis_invoked = False
web_browser_mode = False

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def speak(text):
    engine.say(text)
    engine.runAndWait()

def initiateSequence():

    with open('memory.json', 'r+') as f:
        data = json.load(f)

        if data['memory'][0]['initiate'] == False:
            speak("Initiating, Sequence!...")
            wishMe()
            speak("Allow me to introduce myself... I am " + ai_name + ". A virtual artificial intelligence. "
                  "and I'm here to assists you with variety of tasks as best as I can. 24 hours a day - 7 days a week!....... Importing all preferences from home interface!!.... Systems now fully operational!!.")

            data['memory'][0]['initiate'] = True
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        else:
            wishMe()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source, phrase_time_limit=5)

        try:
            statement=r.recognize_google(audio)

        except Exception as e:

            if jarvis_invoked:
                speak("Sorry sir could you repeat again?")

            return "None"
        return statement

def Statement_Splitter_Query_Search(statement, query_list):

    querywords = statement.split()
    resultwords = ''.join([word for word in querywords if word.lower() in query_list])

    return Query_Search(statement, resultwords)


def Query_Search(statement, q_word):

    if q_word:
        partitions = statement.partition(q_word)
        result = partitions[1] + partitions[2]
        result = result.replace(q_word, '')
        result = result.lstrip()

    else:
        result = ''

    return result

def alarm(set_alarm_timer):
    while True:
        time.sleep(1)
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")

        if now == set_alarm_timer:
            speak("Sir, time to wake up")
            break

def actual_time(set_time):
    speak(f"Sir, setting alarm for {set_time}")
    alarm(set_time)

def time_formatter_def_timer(hour, minute):
    current_time = datetime.datetime.now()
    hours_added = datetime.timedelta(hours=hour)
    minutes_added = datetime.timedelta(minutes=minute)
    future_alarm = current_time + hours_added + minutes_added
    actual_time(future_alarm.strftime("%H:%M:%S"))

def time_clarifier(desigTime):

    if ':' in desigTime:
        partition_time = desigTime.partition(':')
        hour = partition_time[0]
        minute = partition_time[2]
        time_formatter_def_timer(hour,minute)
    else:
        time_formatter_def_timer(desigTime,00)

initiateSequence()

if __name__=='__main__':

    while True:
        statement = takeCommand().lower()
        print(statement)

        if statement==0:
            continue

        if ai_name.lower() in statement:
            speak("Yes Sir!")
            jarvis_invoked = True

        if jarvis_invoked:
            if "goodbye" in statement or "bye" in statement or "stop" in statement or "to go" in statement:
                speak("Have a nice day Sir!.")
                jarvis_invoked = False

            if "shut down the sequence" in statement or "shutdown the sequence" in statement or "shutdown sequence" in statement or "shut down sequence" in statement:
                speak("Terminating Sequence!")
                sys.exit(0)

            if 'wikipedia' in statement:
                try:
                    webbrowser.open_new_tab("https://en.wikipedia.org/wiki/" + Statement_Splitter_Query_Search(statement, searchQ_list))
                    speak("Sir, According to Wikipedia")

                except Exception as e:
                    speak("Sorry sir I couldn't find any results")
                    continue

            elif 'youtube' in statement:
                webbrowser.open_new_tab(
                    "https://www.youtube.com/results?search_query=" + Statement_Splitter_Query_Search(statement, searchQ_list))
                speak("Opening Youtube")

            elif 'who are you' in statement or 'what are you' in statement or 'what is your purpose' in statement:
                speak("Allow me to introduce myself... I am " + ai_name + ", a virtual artificial intelligence, "
                      "and I'm here to assists you with variety of tasks as best as I can, 24 hours a day - 7 days a week")

            elif any(word in statement for word in w5_list) or 'google' in statement:
                if 'open' in statement:
                    webbrowser.open_new_tab("https://google.com/search?q=" + Statement_Splitter_Query_Search(statement, searchQ_list))
                    speak("Opening Google")
                else:
                    webbrowser.open_new_tab("https://google.com/search?q=" + statement)
                    speak("Sir, according to google")

            elif 'gmail' in statement:
                webbrowser.open_new_tab("gmail.com")
                speak("Opening Gmail")

            elif 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

            elif "open" in statement:

                operatingSys = platform.system().lower()
                prefixadder = ''

                if operatingSys == "windows":
                    prefixadder = ''
                elif operatingSys == "darwin":
                    prefixadder = 'open /Applications/'
                elif operatingSys == "linux":
                    prefixadder = ''

                sftware = Query_Search(statement,'open')
                appstatus = True

                for sftwares in absolute_paths['softwares']:
                    if sftware.lower() == sftwares['sft_name']:
                        speak(f"Opening {sftware}")
                        subprocess.Popen(sftwares['path'])
                        appstatus = True
                        break
                    else:
                        appstatus = False

                if not appstatus:
                    output_sftware = os.system(prefixadder+sftware)
                    if output_sftware > 0:
                        speak(f"Sir, I couldn't detect any software called {sftware} in your operating system")
                    else:
                        speak(f"Opening {sftware}")

            elif 'activate web mode' in statement:
                speak('Web mode activated')
                web_browser_mode = True
                driver = webdriver.Chrome("broweser-assistant/chromedriver.exe")
                driver.maximize_window()

                while web_browser_mode:
                    statement = takeCommand().lower()
                    if 'open' in statement:
                        speak('opening new tab')
                        driver.execute_script("window.open('');")
                        window_list = driver.window_handles
                        driver.switch_to.window(window_list[-1])
                        driver.get('https://google.com')
                    elif 'search' in statement:
                        element = driver.find_element(by=By.NAME, value='q')
                        element.clear()
                        element.send_keys(Statement_Splitter_Query_Search(statement, searchQ_list))
                        element.send_keys(Keys.RETURN)
                    elif 'switch' in statement:
                        num_tabs = len(driver.window_handles)
                        cur_tab = 0
                        for i in range(num_tabs):
                            if driver.window_handles[i] == driver.current_window_handle:
                                if i != num_tabs - 1:
                                    cur_tab = i + 1
                                    break
                        driver.switch_to.window(driver.window_handles[cur_tab])
                    elif 'close' in statement:
                        speak("closing tab")
                        driver.close()
                    elif 'go back' in statement:
                        driver.back()
                    elif 'go forward' in statement:
                        driver.forward()
                    elif 'deactivate web mode' in statement:
                        speak('Web mode de-activated')
                        web_browser_mode = False
                    elif 'exit' in statement:
                        speak('closing window, Sir')
                        speak('Web mode de-activated')
                        driver.quit()
                        web_browser_mode = False
                        break
                    time.sleep(2)


            # elif 'wake' in statement or 'alarm' in statement:
            #     if any(word in statement for word in alarm_time_sq):
            #         desigTime = Statement_Splitter_Query_Search(statement, alarm_time_sq)
            #         if "clock" in desigTime:
            #             num = [int(i) for i in desigTime if i.isdigit()]
            #             time_clarifier(str(num[0]))
            #         else:
            #             time_clarifier(desigTime)
            #     else:
            #         desigTime = Statement_Splitter_Query_Search(statement, alarm_hour_sq)
            #         if 'hour' in desigTime or 'hours' in desigTime:
            #             num = [int(i) for i in desigTime if i.isdigit()]
            #             time_formatter_def_timer(num[0],0)
            #         elif 'minute' in desigTime or 'minutes' in desigTime:
            #             num = [int(i) for i in desigTime if i.isdigit()]
            #             time_formatter_def_timer(0,num[0])

            # else:
            #     try:
            #         ints = predict_class(statement)
            #         res = get_response(ints, intents)
            #         speak(res)
            #
            #     except Exception as e:
            #         continue

time.sleep(3)
