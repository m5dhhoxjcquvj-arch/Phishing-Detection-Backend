import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. تعريف التطبيق (لازم يكون فوق)
app = Flask(__name__)
CORS(app)

# 2. تحميل الموديل (إذا فشل بيكمل السيرفر بالوضع الاحتياطي)
try:
    model = joblib.load('phishing_model.pkl')
    print("✅ Model Loaded Successfully")
except:
    model = None
    print("⚠️ Model not loaded, using basic rules")

@app.route('/')
def home():
    return "Phishing Detection API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # تنظيف الرابط وتحويله لأحرف صغيرة لضمان الدقة
        url = str(data.get('url', '')).lower().strip()
        
        # --- قائمة الحصانة الفورية (Whitelist) ---
        # أي رابط يحتوي على هذه الكلمات سيعتبر آمن فوراً
        whitelist = ['youtube.com', 'youtu.be', 'google.com', 'outlook', 'hotmail', 'gmail']
        if any(word in url for word in whitelist):
            return jsonify({'result': 'Safe'})

        # --- فحص الذكاء الاصطناعي ---
        if model:
            features = np.array([[len(url)]])
            prediction = model.predict(features)
            result = "Phishing" if prediction[0] == 1 else "Safe"
        else:
            # وضع احتياطي في حال تعطل الموديل
            result = "Phishing" if len(url) > 150 else "Safe"
            
        return jsonify({'result': result})
    except:
        return jsonify({'result': 'Safe'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
