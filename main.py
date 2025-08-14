# main.py
import time
import csv
import os
from config import questions, questionnaire_reference
from speech_recognition import start_one_round
from zhipu_ai import ZhipuClient
from validate import validate_answer
from tts import TTS
import datetime
import json

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
1. 在读出每一道题目时，使用温暖、鼓励性的语气，让用户放松并愿意配合作答，要求简洁。
2. 用“您”称呼用户，并可在读题前加入简短的过渡或鼓励话语（例如“我们继续下一题”“请您慢慢说，不着急”）。
"""

def run_questionnaire():
    tts = TTS()
    zhipu = ZhipuClient(glm_key)

    print("\n📋 开始语音问卷调查...\n")
    tts.speak("您好，我是您的肺癌早筛问卷助手，我们将开始问卷调查。")

    answers = {}
    user_name = None  # 第一题答案作为用户名

    for idx, q in enumerate(questions):
        # 跳题逻辑
        if "condition" in q and not q["condition"](answers):
            continue  # 条件不满足，跳过此题

        while True:
            # 读题
            question_prompt = f"""
            {AI_question}

            请将以下题目用温暖、鼓励的语气转换成适合语音播报的方式：
            第 {idx + 1} 题：{q['text']}
            只返回朗读文本，保证在语气温暖的情况下，字数简短。
            """
            read_text = zhipu.ask(question_prompt).strip()

            # 播报
            print(read_text)
            tts.speak(read_text)
            time.sleep(0.5)

            # 识别用户回答
            result = start_one_round(APPID, APIKey, APISecret).strip()
            if not result:
                tts.speak("没有识别到语音，请再试一次。")
                time.sleep(1)
                continue

            # AI 格式化答案
            prompt = (
                f"{AI_ROLE}\n\n"
                f"问题：{q['text']}\n"
                f"语音识别结果：{result}\n\n"
                f"最终仅返回符合问卷参考标准的答案，不包含多余文字。"
            )
            norm = zhipu.ask(prompt).strip()
            valid = validate_answer(q['text'], norm)

            if not valid:
                tts.speak("您的回答好像和问题不太相关，我们再试一次。")
                time.sleep(1)
                continue

            # 播报确认
            confirm_text = f"您的回答是：{valid}。"
            print(confirm_text)
            tts.speak(confirm_text)

            # 第一题作为用户名
            if idx == 0:
                user_name = valid if valid else "匿名用户"
                # 清理文件名中非法字符
                safe_user_name = "".join(c for c in user_name if c.isalnum() or c in "_-")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_filename = f"{safe_user_name}_{timestamp}.csv"
                json_filename = f"{safe_user_name}_{timestamp}.json"
                print(f"问卷文件将保存为：{csv_filename} / {json_filename}")

            answers[q['id']] = valid
            break  # 下一题

        # 保存 CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([q['text'] for q in questions])
        writer.writerow([answers.get(q['id'], "") for q in questions])

        # 保存 JSON
    with open(json_filename, mode='w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

    tts.speak("问卷完成，感谢您的配合！")
    return user_name  # 返回用户名，消除未使用变量警告

if __name__ == "__main__":
    run_questionnaire()
