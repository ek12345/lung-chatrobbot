# zhipu_ai.py
from zhipuai import ZhipuAI

class ZhipuClient:
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        self.all_messages = []

    def ask(self, text: str) -> str:
        try:
            messages = [{"role": "user", "content": text}]
            response = self.client.chat.completions.create(
                model="glm-4",
                messages=self.all_messages + messages
            )
            reply = response.choices[0].message.content.strip()
            self.all_messages += messages + [{"role": "assistant", "content": reply}]
            if len(self.all_messages) > 20:
                self.all_messages = self.all_messages[-20:]
            return reply
        except Exception as e:
            print("调用ZhipuAI失败：", e)
            return "无法回答"
