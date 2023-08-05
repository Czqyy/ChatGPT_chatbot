# ChatGPT Elderly Bot
This bot connects to the ChatGPT API gpt-3.5-turbo model. The chat model role is to serve as a friendly elderly caretaker. 
## Instructions to run this program on a Raspberrypi
1. Create a `.env` file containing the OpenAI API key
2. Run `pip3 install -r requirements.txt` to install the required libraries
3. Run `sudo apt update && sudo apt install espeak ffmpeg libespeak1` to install espeak, ffmpeg and libespeak1 for the pyttsx3 library
4. Run `sudo apt install python3-pyaudio` followed by `pip3 install pyaudio` to install PyAudio for the Speech Recognition library
5. Run `sudo apt-get install flac` to install the FLAC encoder required to encode the audio data to send to the Speech Recognition API

