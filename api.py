from flask import Flask, jsonify, request
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from main import run_questionnaire

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def run():
    try:
        # 对于 GET 请求，params 可能为空
        if request.method == 'GET':
            params = {}
        else:
            params = request.get_json(force=True)

        # 参数验证逻辑
        if not params:
            return jsonify({'status': 'error', 'message': 'No parameters provided'}), 400

        # 调用核心逻辑函数
        result = run_questionnaire(params)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)