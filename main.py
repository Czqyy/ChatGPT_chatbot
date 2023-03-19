import openai
import key
import pyttsx3
import speech_recognition as sr


# Obtain audio from microphone
r = sr.Recognizer()

# Set api_key for ChatGPT
openai.api_key = key.API_KEY

# Initialise text-to-speech engine
ENGINE = pyttsx3.init()


def get_response(prompt):
    """
    Connect to ChatGPT to generate a string as a response to given prompt
    """
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an elderly caretaker"}, 
            {"role": "system", "content": "Treat me as an elderly and give me short and simple responses"},
            {"role": "user", "content": "{}".format(prompt)}
        ],
        max_tokens = 50
    )

    output = completion["choices"][0]["message"]["content"]
    print(output)
    return output


def check_wellbeing():
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
    with sr.Microphone() as source:   
        # Adjusts the energy threshold dynamically using audio from source to account for ambient noise
        # Duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning.       
        r.adjust_for_ambient_noise(source, duration=0.5)

        # Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
        # Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.
        r.pause_threshold = 0.5

        # Loop indefinitely for user to speak
        while(1):
            try:
                # Listens for the user's input
                audio = r.listen(source)
                
                # Use Google Speech Recognition to recognize audio
                prompt = r.recognize_google(audio)
                prompt = prompt.lower()
                print(f"Speech input: {prompt}")

                # Get speech response
                response = get_response(prompt)
                speak(response)

                print("Response complete")

            except sr.RequestError as e:
                print("Could not request results: {}".format(e))
            
            except sr.UnknownValueError:
                print("No speech detected.")


if __name__ == "__main__":
    main()  
