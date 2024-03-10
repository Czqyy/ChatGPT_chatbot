import openai
import pyttsx3
import atexit
import speech_recognition as sr
import os
from .prompt import system_content, user_content
from .helpers import log_content


class TextChat(object):
    def __init__(self, output_limit, input_limit, clear_pairs, conversation_path) -> None:
        """
        Initialise text-prompted ChatGPT by setting the system content. 
        """
        self.output_limit = output_limit
        self.input_limit = input_limit
        self.clear_pairs = clear_pairs
        self.conversation_path = conversation_path

        # List to keep track of conversation history
        self.conversation = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

        log_content(self.conversation_path, "======== START ========\n")

        # Initialise text-to-speech engine
        self.ENGINE = pyttsx3.init()

        # Save remaining conversation history when program terminates
        atexit.register(log_content, self.conversation_path, self.conversation[2:] + ["======== END ========\n\n"])

        # # Add initial instructions to conversation to configure ChatGPT characteristics
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.conversation,
            output_limits = self.output_limit
        )
        output = completion["choices"][0]["message"]["content"]
        print(f"Initial response: {output}")
        print("ChatGPT initialised.")

    def get_prompt(self):
        """
        Gets user prompt through manual command line input. Returns the prompt as a string
        """
        prompt = input("Prompt: ")
        return prompt.lower()

    def get_response(self, prompt):
        """
        Connect to ChatGPT to generate a response to given prompt together with context from conversation history.
        Returns a string.
        """
        if prompt is None:
            print("No prompt given.")
            return

        self.conversation.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.conversation,
            output_limits = self.output_limit
        )
        output = completion["choices"][0]["message"]["content"]
        self.conversation.append({"role": "assistant", "content": output})
        print(f"Response: {output}")

        # Remove old conversations to avoid exceeding input token limit and save those conversations
        tokens = completion["usage"]["total_tokens"]
        print(f"Total tokens used: {tokens}")
        if tokens > self.input_limit:
            self.clear_history()
            print("Old conversations cleared.")
        return output
    
    def speak(self, text):
        """
        Takes a string as input and uses the text-to-speech engine to speak the text
        """
        if text is None:
            return
        
        self.ENGINE.say(text)
        self.ENGINE.runAndWait()

    def check_wellbeing(self):
        """
        Function to prompt ChatGPT to ask elderly question to check in on their well-being
        """
        output = self.get_response("Ask me the question: Are you okay?")
        self.speak(output)

    def clear_history(self):
        """
        Clears old conversations and saves in conversation log. Clears first 'prompts' number of user-assistant content pairs.
        """
        log_content(self.conversation_path, self.conversation[2:])

        # Account for user-assistant content pair
        end_index = (2 * self.clear_pairs) + 2
        for i in range(2, end_index):
            del self.conversation[i]


class VoiceChat(TextChat):
    def __init__(self, output_limit, input_limit, clear_pairs, conversation_path, mic_source) -> None:
        """
        Initialise voice-prompted ChatGPT. Source must be a sr.Microphone() object 
        """
        # Initialise voice recogniser
        assert isinstance(mic_source, sr.Microphone), "Audio input must be of class sr.Microphone."
        self.mic_source = mic_source
        self.recogniser = sr.Recognizer()

        # Configurations for the voice recogniser
        self.recogniser.energy_threshold = 4000
        
        # Adjusts the energy threshold dynamically using audio from mic_source to account for ambient noise
        # Duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning.       
        self.recogniser.adjust_for_ambient_noise(self.mic_source, duration=0.5)

        # Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
        # Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.
        self.recogniser.pause_threshold = 0.5

        super().__init__(output_limit, input_limit, clear_pairs, conversation_path)

    def get_prompt(self):
        """
        Gets user prompt through voice recognition. Returns the prompt as a string
        """
        try:
            # Listens for the user's input
            print("Listening...")
            audio = self.recogniser.listen(self.mic_source)
            
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