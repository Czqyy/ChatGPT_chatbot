import openai
import pyttsx3
import os
from dotenv import load_dotenv
# import speech_recognition as sr


# Obtain audio from microphone
# r = sr.Recognizer()

# Set api_key for ChatGPT
load_dotenv()
openai.api_key = os.environ['API_KEY']

# Token restriction on ChatGPT response
MAX_TOKEN = 100

# Initialise text-to-speech engine
ENGINE = pyttsx3.init()

def init_chat(conversation):
    """
    Initialise ChatGPT by setting the system content. Updates and returns the conversation list
    """
    # Initial instructions to set chatgpt characteristics
    conversation.append(
        {"role": "system", "content": "You are a friendly elderly caretaker."}
    )
    conversation.append(
        {"role": "user", "content": "I am an elderly. All your responses to me should be short and simple."}
    )

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = conversation,
        max_tokens = MAX_TOKEN
    )

    output = completion["choices"][0]["message"]["content"]
    print(output)


def get_response(prompt, conversation):
    """
    Connect to ChatGPT to generate a string as a response to given prompt together with context from conversation history
    """
    # Add prompt to conversation as user message
    conversation.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = conversation,
        max_tokens = MAX_TOKEN
    )

    output = completion["choices"][0]["message"]["content"]
    print(output)

    # Log user message into conversation history 
    conversation.append({"role": "assistant", "content": output})

    return output


# def check_wellbeing():
    """
    Function to prompt ChatGPT to ask elderly question to check in on their well-being
    """
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an elderly caretaker"}, 
            {"role": "system", "content": "Treat me as an elderly and give me short and simple responses"},
            {"role": "user", "content": "Ask me the question: Are you okay?"}
        ],
        max_tokens = 50
    )

    output = completion["choices"][0]["message"]["content"]
    speak(output)


def speak(text):
    """
    Takes a string as input and uses the text-to-speech engine to speak the text
    """
    ENGINE.say(text)
    ENGINE.runAndWait()


def main():
    # Log of conversation history
    conversation = []

    # Configure characteristics of ChatGPT
    init_chat(conversation)

    # Manual typing of prompt without the use of microphone
    while(1):
        prompt = input("Prompt: ")
        prompt = prompt.lower()

        response = get_response(prompt, conversation)
        speak(response)

        print('Response complete')

    # Uncomment when microphone is available
    # with sr.Microphone() as source:   
    #     # Adjusts the energy threshold dynamically using audio from source to account for ambient noise
    #     # Duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning.       
    #     r.adjust_for_ambient_noise(source, duration=0.5)

    #     # Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
    #     # Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.
    #     r.pause_threshold = 0.5

    #     # Loop indefinitely for user to speak
    #     while(1):
    #         try:
    #             # Listens for the user's input
    #             audio = r.listen(source)
                
    #             # Use Google Speech Recognition to recognize audio
    #             prompt = r.recognize_google(audio)
    #             prompt = prompt.lower()
    #             print(f"Speech input: {prompt}")

    #             # Get speech response
    #             response = get_response(prompt)
    #             speak(response)

    #             print("Response complete")

    #         except sr.RequestError as e:
    #             print("Could not request results: {}".format(e))
            
    #         except sr.UnknownValueError:
    #             print("No speech detected.")


if __name__ == "__main__":
    main()  
