import openai
import os
import sys
from dotenv import load_dotenv
import speech_recognition as sr
import argparse
from chatbot.chats import VoiceChat, TextChat


# Set api_key for ChatGPT
load_dotenv()
openai.api_key = os.environ['API_KEY']

CONVERSATION_PATH = os.path.join("data", "conversation_log", "conversation.txt")

# Token limit for output response
OUTPUT_TOKEN_LIMIT = 100

# Token limit for chat input
INPUT_TOKEN_LIMIT = 500

# Number of user-assistant conversation pairs to clear once INPUT_TOKEN_LIMIT has been reached.
CLEAR_PAIRS = 5


def run_conversation(chat: TextChat):
    """
    Function to be called continuously to run the chatbot.
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
        chat = TextChat(OUTPUT_TOKEN_LIMIT, INPUT_TOKEN_LIMIT, CLEAR_PAIRS, CONVERSATION_PATH)
        while True:
            run_conversation(chat)
    elif args.input_type == "v":
        # Using voice recognition
        with sr.Microphone() as source:
            chat = VoiceChat(OUTPUT_TOKEN_LIMIT, INPUT_TOKEN_LIMIT, CLEAR_PAIRS, CONVERSATION_PATH, source)
            while True:
                run_conversation(chat)
    else:
        print("Invalid command line argument. Run 'python3 main.py t' for TextChat, 'python3 main.py v' for VoiceChat.")
        return


if __name__ == "__main__":
    main()  
