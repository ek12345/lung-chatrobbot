from tts import TTS
import time
t = TTS()
for i in range(3):
    t.speak(f"第 {i+1} 题测试。")
    time.sleep(0.5)