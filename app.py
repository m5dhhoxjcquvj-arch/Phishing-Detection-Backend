import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Final Security Engine is Live!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # تحويل الرابط لحروف صغيرة وحذف أي مسافات أو رموز غريبة في الأطراف
        url = str(data.get('url', '')).lower().strip()
        
        # قائمة "الحصانة" - أي رابط يحتوي على هذي الكلمات آمن فوراً
        # لاحظ أضفت 'youtube' و 'youtu' و 'google'
        if any(word in url for word in ['youtube', 'youtu', 'google', 'tiktok', 'speedtest']):
            return jsonify({'result': 'Safe'})
        
        # إذا الرابط مجهول (مو من القائمة اللي فوق)
        # نطبق عليه فحص الطول والرموز
        if len(url) > 100 or url.count('?') > 1:
            return jsonify({'result': 'Phishing'})
        
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
