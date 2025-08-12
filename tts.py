# tts.py
import pyttsx3
import threading

# class TTS:
#     def __init__(self):
#         self.engine = pyttsx3.init()
#         self.engine.setProperty('rate', 170)
#         self.lock = threading.Lock()
#
#     def speak(self, text: str):
#         with self.lock:
#             self.engine.say(text)
#             self.engine.runAndWait()
class TTS:
    def __init__(self, rate=170):
        self.rate = rate
        self.lock = threading.Lock()

    def speak(self, text: str):
        with self.lock:
            eng = pyttsx3.init()
            eng.setProperty('rate', self.rate)
            eng.say(text)
            eng.runAndWait()
            eng.stop()