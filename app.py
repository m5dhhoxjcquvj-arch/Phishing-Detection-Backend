import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "AI Detection System - Ready"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # تنظيف الرابط من المسافات وتحويله لحروف صغيرة
        url = str(data.get('url', '')).lower().strip()
        
        # قائمة "الحصانة" - أي كلمة هنا تخلي الرابط آمن فوراً
        # أضفت لك 'watch' و 'mail' عشان يوتيوب وهوتميل
        safe_keywords = [
            'youtube', 'youtu', 'google', 'gmail', 
            'hotmail', 'outlook', 'live', 'microsoft', 
            'tiktok', 'watch', 'mail'
        ]

        # فحص وجود الكلمات الآمنة
        if any(word in url for word in safe_keywords):
            return jsonify({'result': 'Safe'})
        
        # منطق "الشك" للروابط الطويلة والمشبوهة
        if len(url) > 120 or url.count('?') > 1:
            return jsonify({'result': 'Phishing'})
            
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
