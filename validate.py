# validate.py
import re
from config import questionnaire_reference

def validate_answer(question, answer):
    for section, qs in questionnaire_reference.items():
        if question in qs:
            pattern = qs[question]
            if "或" in pattern and any(opt in answer for opt in re.findall(r"\d+", pattern)):
                return answer.strip()
            elif "0~" in pattern or "数值" in pattern:
                digits = re.findall(r"\d+", answer)
                return digits[0] if digits else answer
            elif "位" in pattern:
                return re.sub(r"[^\w]", "", answer)
            return answer.strip()
    return answer.strip()
