import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Final Safe System - Ready"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # 1. نظام الحصانة (لأي شيء يخص يوتيوب أو المواقع المشهورة)
        # حتى لو كتبت "watch" بس، بيعتبرها آمنة عشان خاطرك
        safe_words = ['youtube', 'youtu', 'google', 'watch', 'hotmail', 'outlook', 'mail']
        if any(word in url for word in safe_words):
            return jsonify({'result': 'Safe'})

        # 2. متى يقول "مشبوه"؟ (فقط في الحالات الخطيرة جداً)
        # رفعنا حد الطول لـ 300 عشان ياخذ راحتك في الروابط الطويلة
        if "@" in url or "login-" in url or ".exe" in url:
            return jsonify({'result': 'Phishing'})
        
        if len(url) > 300:
            return jsonify({'result': 'Phishing'})

        # 3. أي رابط ثاني؟ اعتبره آمن
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
