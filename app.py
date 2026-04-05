import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Phishing Detector - Final Version"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        raw_input = data.get('url', '')
        
        # 1. تنظيف الرابط من التشفير (مثلاً %20 يرجع مسافة)
        # وتحويله لحروف صغيرة
        url = urllib.parse.unquote(raw_input).lower().strip()
        
        # 2. القائمة الذهبية (أول شيء ينفذه السيرفر)
        # إذا لقى أي كلمة من هذي الكلمات، يعطي Safe فوراً ويسحب على الباقي
        safe_words = ['youtube', 'youtu.be', 'google', 'tiktok', 'speedtest', 'facebook', 'instagram']
        
        for word in safe_words:
            if word in url:
                return jsonify({'result': 'Safe'})

        # 3. فحص الروابط المجهولة (منطق أمني بسيط)
        # إذا الرابط "غريب" جداً أو طويل بزيادة بدون ما يكون من المواقع المعروفة
        suspicious_chars = ['@', '!!', 'login', 'verify', 'update-account']
        
        if any(char in url for char in suspicious_chars) or len(url) > 150:
            return jsonify({'result': 'Phishing'})
        
        # الافتراضي لأي رابط طبيعي
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
