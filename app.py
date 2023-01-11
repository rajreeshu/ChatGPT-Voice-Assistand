import tkinter as tk
import speech_recognition as sr
import openai
import os
from gtts import gTTS
import winsound
import pyttsx3
import threading



stop_speaking = False
previous_question=""


def listen_to_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5)
    return audio

def recognize_speech(audio):
    r = sr.Recognizer()

    # Update the label to show that the app is recognizing
    label.configure(text="Recognizing...")
    root.update_idletasks()

    text = r.recognize_google(audio)
    print(text);

    # Clear the label text
    label.configure(text="")
    root.update_idletasks()

    return text

def ask_question(question):
    try:
        question_label.configure(text="Searching for results...", font=("Verdana", 14, "bold"))
        question_label.pack()
        root.update_idletasks()
        
        openai.api_key = "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"
        model_engine = "text-davinci-002"
        prompt = (f"{question}\n")
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.5
        )
        message = completions.choices[0].text

        # Update the question label to display the question
        question_label.configure(text=question, font=("Verdana", 14, "bold"))
        question_label.pack()

        # Update the answer label to display the answer
        answer_label.configure(text=message, wraplength=600, justify=tk.LEFT)
        answer_label.pack()
        root.update_idletasks()

        

        return message
    except Exception as e:
        print(f"An error occurred while asking the question: {e}")
        return "Sorry, I am unable to answer your question at this time."



def speak_text(text):
    global stop_speaking
    if stop_speaking:
        return
    print(text)
    def run_in_thread():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"An error occurred while speaking the text: {e}")

    thread = threading.Thread(target=run_in_thread)
    thread.start()

def ask():
    global previous_question
    question=""

    # Update the label to show that the app is listening
    label.configure(text="Listening...")

    def run_in_thread():
        nonlocal question
        global previous_question
        try:
            # Try to listen to the microphone
            audio = listen_to_microphone()
        except Exception as e:
            print(f"An error occurred while listening: {e}")
            # Update the question label to display a default message
            question_label.configure(text="Sorry, I was unable to listen to your question.", font=("Verdana", 14, "bold"))
            question_label.pack()
            root.update_idletasks()
            return
        try:
            # Try to recognize the speech
            question = recognize_speech(audio)
            previous_question = question  # Update the global variable
            answer = ask_question(question)
            speak_text(answer)
            # Update the label to show that the app is done listening
            label.configure(text="")
        except Exception as e:
            print(f"An error occurred while recognizing speech: {e}")
            # Update the question label to display a default message
            question_label.configure(text=f"Sorry, I was unable to understand your question. \n{e}", font=("Verdana", 14, "bold"))
            question_label.pack()
            root.update_idletasks()
            return
    thread = threading.Thread(target=run_in_thread)
    thread.start()

def ask_again():
    global previous_question
    print(previous_question)
    if previous_question:
        answer = ask_question(previous_question)
        speak_text(answer)
    else:
        print("No previous question available")

def stop_speak():
    global stop_speaking
    stop_speaking = True

root = tk.Tk()
root.title("ChatGPT Voice Assistant")
root.geometry("600x400")


# Set the background color and font for the app
root.configure(bg="#808080")
font = ("Verdana", 14)

# Create the label for displaying listening/recognizing messages
label = tk.Label(root, text="", font=font, bg="#808080")
label.pack()

# Create the "Ask" button
ask_button = tk.Button(root, text="Ask", font=font, bg="#000080", fg="#FFFFFF", command=ask)
ask_button.pack(pady=10)

# Create the "Ask Again" button
ask_again_button = tk.Button(root, text="Ask Again", font=font, bg="#000080", fg="#FFFFFF", command=ask_again)
ask_again_button.pack(pady=10)



# Create the "Stop Speaking" button
stop_button = tk.Button(root, text="Stop Speaking", font=font, bg="#000080", fg="#FFFFFF", command=stop_speak)
stop_button.pack(pady=10)

# Create the label for displaying the question
question_label = tk.Label(root, text="", font=font, bg="#808080")

# Create the label for displaying the answer
answer_label = tk.Label(root, text="", font=font, bg="#808080")
answer_label.pack()

root.mainloop()