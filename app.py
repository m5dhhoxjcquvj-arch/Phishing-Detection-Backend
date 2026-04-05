import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. أولاً: تعريف التطبيق (هذا اللي كان ناقص في السطر الأول)
app = Flask(__name__)
CORS(app)

# 2. تحميل الموديل (مع معالجة الخطأ إذا مو موجود)
try:
    model = joblib.load('phishing_model.pkl')
    print("✅ Model Loaded Successfully")
except Exception as e:
    model = None
    print(f"❌ Error loading model: {e}")

@app.route('/')
def home():
    return "Phishing Detection API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # قائمة الحصانة الفورية (يوتيوب وجوجل)
        whitelist = ['youtube', 'youtu', 'watch', 'google', 'hotmail', 'outlook', 'mail']
        if any(word in url for word in whitelist):
            return jsonify({'result': 'Safe'})

        # فحص الذكاء الاصطناعي
        if model:
            features = np.array([[len(url)]])
            prediction = model.predict(features)
            result = "Phishing" if prediction[0] == 1 else "Safe"
        else:
            # خطة بديلة لو الموديل ما تحمل
            result = "Phishing" if len(url) > 150 else "Safe"
            
        return jsonify({'result': result})
    except:
        return jsonify({'result': 'Safe'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
