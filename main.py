import openai
import pyttsx3
import os
from dotenv import load_dotenv
import speech_recognition as sr


# Set api_key for ChatGPT
load_dotenv()
openai.api_key = os.environ['API_KEY']


class Chat(object):
    def __init__(self, max_token=100, source=False) -> None:
        """
        Initialise ChatGPT by setting the system content. 
        """
        self.max_token = max_token
        self.source = source

        # Initialise text-to-speech engine
        self.ENGINE = pyttsx3.init()

        # Initialise and configure voice recognition if set to True
        if self.source:  
            # Obtain voice recogniser from microphone
            self.recogniser = sr.Recognizer()
            
            # Adjusts the energy threshold dynamically using audio from source to account for ambient noise
            # Duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning.       
            self.recogniser.adjust_for_ambient_noise(self.source, duration=0.5)

            # Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
            # Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.
            self.recogniser.pause_threshold = 0.5


        # List keeping track of conversation history
        self.conversation = []
    
        # Add initial instructions to conversation to configure ChatGPT characteristics
        self.conversation.append(
            {"role": "user", "content": "You are a friendly elderly caretaker."}
        )
        self.conversation.append(
            {"role": "user", "content": "I am an elderly. All your responses to me should be short and simple."}
        )

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.conversation,
            max_tokens = self.max_token
        )

        output = completion["choices"][0]["message"]["content"]

        print(f"Initial response: {output}")
        print("ChatGPT initialised.")


    def get_prompt(self):
        """
        Gets user prompt either through voice recognition or manual cli input. Returns the prompt as a string
        """
        if self.source:
            try:
                # Listens for the user's input
                print("Listening...")
                audio = self.recogniser.listen(self.source)
                
                # Use Google Speech Recognition to recognize audio
                prompt = self.recogniser.recognize_google(audio)
                prompt = prompt.lower()
                print(f"Speech input: {prompt}")
                return prompt

            except sr.RequestError as e:
                print(f"Could not request results: {e}")
            
            except sr.UnknownValueError:
                print("No speech detected.")
                return 

        else:
            prompt = input("Prompt: ")
            prompt = prompt.lower()
            return prompt


    def get_response(self, prompt):
        """
        Connect to ChatGPT to generate a string as a response to given prompt together with context from conversation history
        """
        if prompt is None:
            print("No prompt given.")
            return

        # Add prompt to conversation as user message
        self.conversation.append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.conversation,
            max_tokens = self.max_token
        )

        output = completion["choices"][0]["message"]["content"]
        print(f"Response: {output}")

        tokens = completion["usage"]["total_tokens"]
        print(f"Total tokens used: {tokens}")

        # Remove some conversation history to avoid exceeding maximum token limit of model 
        if tokens > 3000:
            self.clear_conversation(self.conversation)

        # Log user message into conversation history 
        self.conversation.append({"role": "assistant", "content": output})

        return output


    def clear_conversation(self, prompts=10):
        """
        Function to clear conversation history with ChatGPT. Clears 'prompts' number of user messages 
        Default number set to 10 user-assistant content pairs.
        """
        # Account for user-assistant content pair
        end_index = (2 * prompts) + 2
        for i in range(2, end_index):
            del self.conversation[i]


    def check_wellbeing(self):
        """
        Function to prompt ChatGPT to ask elderly question to check in on their well-being
        """
        output = self.get_response("Ask me the question: Are you okay?")
        self.speak(output)


    def speak(self, text):
        """
        Takes a string as input and uses the text-to-speech engine to speak the text
        """
        if text is None:
            return
        
        self.ENGINE.say(text)
        self.ENGINE.runAndWait()



def main():
    # Using manual command line input
    chat = Chat()

    while(1):
        prompt = chat.get_prompt()
        response = chat.get_response(prompt)
        chat.speak(response)

    
    # Using voice recognition
    # with sr.Microphone() as source:
    #     chat = Chat(source=source)

    #     while(1):
    #         prompt = chat.get_prompt()
    #         response = chat.get_response(prompt)
    #         chat.speak(response)



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
