import openai
import os
import sys
from dotenv import load_dotenv
import speech_recognition as sr
import argparse
from chats import VoiceChat, TextChat


# Set api_key for ChatGPT
load_dotenv()
openai.api_key = os.environ['API_KEY']

def run_chat(chat):
    """
    Function to be called continuously to run the chatbot. Takes in a TextChat object.
    """
    prompt = chat.get_prompt()
    response = chat.get_response(prompt)
    chat.speak(response)


def main():
    parser = argparse.ArgumentParser(description="Run 'python3 main.py t' for TextChat, 'python3 main.py v' for VoiceChat.")
    parser.add_argument("input_type")
    args = parser.parse_args()
  
    if args.input_type == "t":
        # Using manual command line input
        chat = TextChat()
        while(1):
            run_chat(chat)
    elif args.input_type == "v":
        # Using voice recognition
        with sr.Microphone() as source:
            chat = VoiceChat(source)
            while(1):
                run_chat(chat)
    else:
        print("Invalid command line argument. Run 'python3 main.py t' for TextChat, 'python3 main.py v' for VoiceChat.")
        return


if __name__ == "__main__":
    main()  
