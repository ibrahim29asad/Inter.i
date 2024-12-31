# https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/


# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3 

print("Hello World")

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
    
# Loop infinitely for user to
# speak


# Loop infinitely for user to speak
while True:
    try:
        # Use the microphone as source for input
        with sr.Microphone() as source2:
            # Adjust the recognizer sensitivity to ambient noise
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            # Listen for the user's input
            audio2 = r.listen(source2)
            
            # Using Google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Did you say:", MyText)
            SpeakText(MyText)
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("Unknown error occurred")