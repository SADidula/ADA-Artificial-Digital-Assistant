from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import  speech_recognition as sr
import time
import pyttsx3

driver = webdriver.Chrome("broweser-assistant/chromedriver.exe")
driver.maximize_window()

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(invoke):
    engine.say(invoke)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=3)
    response = ""
    speak("identifying speech...")
    try:
        response = recognizer.recognize_google(audio)
    except:
        response = "Error"
    return response
time.sleep(3)
speak("Hey!, you can ask me anything")

while True:
    voice = recognize_speech().lower()
    print(voice)
    if 'open google' in voice:
        speak('opening google')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://google.com')
    elif 'search google' in voice:
        while True:
            speak('web mode activated')
            query = recognize_speech()
            if query != "error":
                break
        element = driver.find_element(by=By.NAME, value='q')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'open youtube' in voice:
        speak('opening google')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://google.com')
    elif 'search youtube' in voice:
        while True:
            speak('web mode activated')
            query = recognize_speech()
            if query != "error":
                break
        element = driver.find_element(by=By.NAME, value='search_query')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)

    elif 'switch tab' in voice:
        num_tabs = len(driver.window_handles)
        cur_tab = 0
        for i in range(num_tabs):
            if driver.window_handles[i] == driver.current_window_handle:
                if i != num_tabs - 1:
                    cur_tab = i + 1
                    break
        driver.switch_to.window(driver.window_handles[cur_tab])
    elif 'close tab' in voice:
        speak("closing tab")
        driver.close()
    elif 'go back' in voice:
        driver.back()
    elif 'go forward' in voice:
        driver.forward()
    elif 'exit' in voice:
        speak('closing window')
        driver.quit()
        break
    else:
        speak('not a valid command')
    time.sleep(2)
