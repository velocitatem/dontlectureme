RECORDING_TIME = 15 # seconds
import base64
import whisper
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import uuid


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["|", "/", "-", "\\"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

def transcribe(audio_file):
    # suppress any warnings
    import warnings
    warnings.filterwarnings("ignore")
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# this projects helps students in lectures
# it runs in the background on their computer and for every minute it runs, it records and audio file
# it then transcribes the audio file
# it then checks if the transcription contains any of the keywords that the student has set
# if it does, it sends a notification to the student


import sounddevice as sd
import soundfile as sf
import time
def record():

    fs = 44100  # Sample rate
    seconds = RECORDING_TIME  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    fileName = str(uuid.uuid4()) + ".wav"
    sf.write(fileName, myrecording, fs)  # Save as WAV file
    return fileName


# read keywords from a file keywords.txt
keywords = []
with open('keywords.txt', 'r') as f:
    keywords = [line.strip() for line in f.readlines()]

def check_keywords(transcription):
    # return the keyword that was matched
    for keyword in keywords:
        if keyword in transcription:
            return keyword
    return None


def notify(context):
    import notify2
    notify2.init('DontLectureMe')
    n = notify2.Notification('Keyword match', context)
    n.show()

import openai
def contextualize(transcript, keyword_match):
    prompt = f"The transcript from the class at the moment is: {transcript}.\nYou requested to be notified when the keyword {keyword_match} is mentioned.\nIn what context has it been metioned in the transcript?\nContext:\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"]


def main():
    import sqlite3
    dateString = time.strftime("%Y-%m-%d")
    conn = sqlite3.connect(f"donotlectureme-{dateString}.db")
    c = conn.cursor()
    # crate a table if it doesn't exist
    # table with columns: timestamp, audio, transcription, keyword_match, context
    command = "CREATE TABLE IF NOT EXISTS lectures (timestamp TEXT, audio TEXT, transcription TEXT, keyword_match TEXT, context TEXT)"
    # execute the command
    c.execute(command)
    # commit the changes
    conn.commit()

    while True:
        loader = Loader("Recording audio").start()
        audio_file = record() # you can run the demo by changing this to "feynman-cut.mp3"
        loader.stop()
        # create an animation of transcribing the audio file here

        loader = Loader("Transcribing audio").start()
        transcription = transcribe(audio_file)
        print(transcription)
        loader.stop()
        match = check_keywords(transcription)
        context = None
        if match:
            context = contextualize(transcription, match)
            notify(context)
        # save the raw audio file, the transcription, the keyword match, and the context to the database
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        transcription = base64.b64encode(transcription.encode()).decode()
        command = f"INSERT INTO lectures VALUES ('{timestamp}', '{audio_file}', '{transcription}', '{match}', '{context}')"
        print(command)
        c.execute(command)
        conn.commit()
    c.close()



if __name__ == '__main__':
    main()
