import whisper
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


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
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
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
    seconds = 60  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    sf.write('output.wav', myrecording, fs)  # Save as WAV file
    return 'output.wav'


# read keywords from a file keywords.txt
keywords = []
with open('keywords.txt', 'r') as f:
    keywords = [line.strip() for line in f.readlines()]

def check_keywords(transcription):
    for keyword in keywords:
        if keyword in transcription:
            return True
    return False

def notify():
    import notify2
    notify2.init('DontLectureMe')
    n = notify2.Notification('DontLectureMe', 'You are being lectured')
    n.show()


def main():
    while True:
        loader = Loader("Recording audio").start()
        audio_file = record() # you can run the demo by changing this to "feynman-cut.mp3"
        loader.stop()
        # create an animation of transcribing the audio file here

        loader = Loader("Transcribing audio").start()
        transcription = transcribe(audio_file)
        print(transcription)
        loader.stop()
        if check_keywords(transcription):
            notify()

if __name__ == '__main__':
    main()
