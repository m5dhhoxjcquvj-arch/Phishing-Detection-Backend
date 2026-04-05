import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tldextract

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Security Engine - Hotmail Ready!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url', '').lower().strip()
        
        # استخراج اسم الموقع الحقيقي (الدومين)
        # مثلاً: https://outlook.live.com بيطلع منها كلمة 'outlook'
        ext = tldextract.extract(url)
        domain = ext.domain 

        # قائمة "الحصانة القصوى" للهوت ميل وجماعته
        # أضفت لك كل مشتقات مايكروسوفت وجوجل
        safe_domains = [
            'outlook', 'hotmail', 'live', 'microsoft', 'msn', 
            'google', 'gmail', 'youtube', 'youtu', 
            'tiktok', 'facebook', 'instagram', 'speedtest'
        ]

        # فحص إذا كان الدومين موجود في القائمة
        if domain in safe_domains:
            return jsonify({'result': 'Safe'})
        
        # إذا الرابط مجهول (مو من الكبار) نطبق فحص أمني
        # الروابط اللي فيها أرقام كثيرة أو رموز مريبة في الدومين
        if len(url) > 150 or url.count('-') > 5:
            return jsonify({'result': 'Phishing'})
            
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
