import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "System is Online"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # قائمة الحصانة الفورية (أي كلمة هنا تعطي أخضر فورا)
        if any(word in url for word in ['youtube', 'youtu', 'watch', 'google', 'hotmail', 'outlook', 'mail']):
            return jsonify({'result': 'Safe'})

        # إذا الرابط مشبوه فعلاً (طويل جداً أو فيه علامات اختراق)
        if len(url) > 300 or "@" in url:
            return jsonify({'result': 'Phishing'})

        return jsonify({'result': 'Safe'})
    except:
        return jsonify({'result': 'Safe'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
