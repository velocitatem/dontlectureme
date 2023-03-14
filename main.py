import whisper

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
        audio_file = record() # you can run the demo by changing this to "feynman-cut.mp3"
        transcription = transcribe(audio_file)
        if check_keywords(transcription):
            notify()

if __name__ == '__main__':
    main()
