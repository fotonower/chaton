import sounddevice as sd
import numpy as np

fs = 44100


duration = 10.5  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)

myrecording = sd.rec(int(duration * fs))
sd.wait()