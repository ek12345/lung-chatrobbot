# speech_recognition.py
import websocket
import time
import pyaudio
import base64
import json
import hashlib
import hmac
import ssl
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import numpy as np

SILENCE_THRESHOLD = 500
MAX_SILENCE_DURATION = 5

class Ws_Param:
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {
            "domain": "iat", "language": "zh_cn", "accent": "mandarin",
            "vinfo": 1, "vad_eos": 10000
        }

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        v = {"authorization": authorization, "date": date, "host": "ws-api.xfyun.cn"}
        return url + '?' + urlencode(v)

def is_silence(data, threshold=SILENCE_THRESHOLD):
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean() < threshold

def start_one_round(APPID, APIKey, APISecret):
    wsParam = Ws_Param(APPID, APIKey, APISecret)
    ws_url = wsParam.create_url()
    result_text = ""
    silence_start = None
    status = 0  # 0: first frame, 1: continue, 2: last frame

    def on_message(ws, message):
        nonlocal result_text
        try:
            msg = json.loads(message)
            if msg.get("code") != 0:
                print("错误：", msg)
                return
            words = msg["data"]["result"]["ws"]
            result_text += ''.join(w['w'] for i in words for w in i['cw'])
            print("📝 实时识别：", result_text)
        except Exception as e:
            print("解析失败：", e)

    def on_error(ws, error):
        print("连接出错：", error)

    def on_close(ws, *args):
        print("🔒 连接已关闭")

    def on_open(ws):
        import _thread
        def run():
            nonlocal silence_start, status
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            print("🎤 识别开始（静音超5秒自动结束）")
            silence_start = None
            while True:
                buf = stream.read(8000)
                if is_silence(buf):
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > MAX_SILENCE_DURATION:
                        print("🛑 静音超时，结束识别")
                        status = 2
                else:
                    silence_start = None

                audio_base64 = base64.b64encode(buf).decode('utf-8')
                if status == 0:
                    data = {"common": wsParam.CommonArgs, "business": wsParam.BusinessArgs,
                            "data": {"status": 0, "format": "audio/L16;rate=16000", "audio": audio_base64, "encoding": "raw"}}
                    status = 1
                elif status == 1:
                    data = {"data": {"status": 1, "format": "audio/L16;rate=16000", "audio": audio_base64, "encoding": "raw"}}
                elif status == 2:
                    data = {"data": {"status": 2, "format": "audio/L16;rate=16000", "audio": ""}}
                    ws.send(json.dumps(data))
                    break

                ws.send(json.dumps(data))
                time.sleep(0.04)

            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()

        _thread.start_new_thread(run, ())

    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return result_text
