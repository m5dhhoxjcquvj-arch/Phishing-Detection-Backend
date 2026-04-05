import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Final Test Version is Live!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # تحويل الرابط لحروف صغيرة وحذف أي مسافات زائدة
        url = data.get('url', '').lower().strip()
        
        # القائمة الذهبية - بمجرد وجود الكلمة في الرابط يعتبر آمن
        # أضفت لك كل الاحتمالات عشان ما يغلط
        if 'youtube' in url or 'youtu.be' in url or 'google' in url or 'tiktok' in url or 'speedtest' in url:
            return jsonify({'result': 'Safe'})
        
        # إذا الرابط ما فيه الكلمات اللي فوق، نطبق عليه فحص بسيط
        # إذا فيه رموز غريبة كثير أو طويل بزيادة يعتبر مشبوه
        if url.count('.') > 3 or len(url) > 100:
            return jsonify({'result': 'Phishing'})
        
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
