# main.py
import time
import csv
import os
from config import questions, questionnaire_reference
from speech_recognition import start_one_round
from zhipu_ai import ZhipuClient
from validate import validate_answer
from tts import TTS

APPID = '1d4fb2ff'
APIKey = 'c86b1469420c71723580e9a269e7f6e3'
APISecret = 'MDdkYjMyMTRlMTcxOTEyYjg5ODFmY2Ex'
glm_key = "dc1d8d495c194b28b83568005deec678.j9pmKuQ1AeqcP676"
csv_filename = "questionnaire_answers.csv"

AI_ROLE = f"""
你是一位友善、耐心、专业的肺癌早筛问卷助手，像一位贴心的健康顾问一样与用户交流。
你的任务：
1. 逐题接收用户的回答，将语音识别结果转化为符合问卷参考格式的标准答案。
2. 如果用户的回答与问题无关（答非所问）或内容不完整，应礼貌提示并要求对方重新回答，避免直接编造。
3. 当语音识别有误、含糊或出现近音时，根据参考格式和语境选择最合理的答案。
4. 输出时只返回答案内容，不包含多余文字、解释或重复题目。
5. 保持用词温暖友好，例如称呼用户为“您”，在需要重答时使用鼓励语气（如“没关系，我们再试一次”）。
6. 严格遵循问卷参考答案格式（{questionnaire_reference}）进行输出。
7. 不进行医疗诊断或提供超出问卷范围的建议。
"""
AI_question = f"""
你是一位友善、耐心、专业的肺癌早筛问卷助手，像一位贴心的健康顾问一样与用户交流。
你的任务：
1. 在读出每一道题目时，使用温暖、鼓励性的语气，让用户放松并愿意配合作答。
2. 用“您”称呼用户，并可在读题前加入简短的过渡或鼓励话语（例如“我们继续下一题”“请您慢慢说，不着急”）。
"""

def run_questionnaire():
    tts = TTS()
    zhipu = ZhipuClient(glm_key)

    print("\n📋 开始语音问卷调查...\n")
    tts.speak("您好，我是您的肺癌早筛问卷助手，我们将开始问卷调查。")

    answers = []

    for idx, question in enumerate(questions):
        while True:
            # 读题

            read_text = f"第 {idx + 1} 题，{question}。"
            question_prompt = f"""{AI_question}

            以下是本次问卷的全部题目，请按照设定依次友善地播报：
            {chr(10).join([f"第 {i + 1} 题，{q}。" for i, q in enumerate(questions)])}

            现在请从第 {idx + 1} 题开始：
            {read_text}
            """

            norm_question = zhipu.ask(question_prompt).strip()
            valid_question = validate_answer(question, norm_question)
            print(valid_question)
            tts.speak(valid_question)
            time.sleep(1.5)

            # 识别用户回答
            result = start_one_round(APPID, APIKey, APISecret).strip()

            if not result:
                tts.speak("没有识别到语音，请再试一次。")
                time.sleep(1)
                continue

            # AI 格式化答案
            prompt = (
                f"{AI_ROLE}\n\n"
                f"问题：{question}\n"
                f"语音识别结果：{result}\n\n"
                f"最终仅返回符合问卷参考标准的答案，不包含多余文字。"
            )
            norm = zhipu.ask(prompt).strip()
            valid = validate_answer(question, norm)

            # 答非所问 / 无效答案处理
            if not valid:
                tts.speak("您的回答好像和问题不太相关，我们再试一次。")
                time.sleep(1)
                continue

            # 播报 AI 处理结果
            confirm_text = f"您的回答是：{valid}。"
            print(confirm_text)
            tts.speak(confirm_text)

            answers.append(valid)
            break  # 进入下一题

    # 保存答案到 CSV
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(questions)

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(answers)

    tts.speak("问卷完成，感谢您的配合！")

if __name__ == "__main__":
    run_questionnaire()

#更亲切一些，人格，   答非所问情况
#多智能体合作
#上传api，给同学
#ppt10页左右