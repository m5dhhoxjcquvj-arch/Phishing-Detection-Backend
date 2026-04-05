from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# تحميل النموذج (تأكد أن الاسم مطابق لملفك)
try:
    model = joblib.load('phishing_model.pkl')
except:
    model = None

@app.route('/')
def home():
    return "Backend is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    
    # هنا تحط منطق الفحص حقك (مبدئياً بنعطيه رد تجريبي)
    # بمجرد ما يشتغل الربط، بنحدث هذا الجزء بالكود حقك الفعلي
    prediction = "Safe" 
    
    return jsonify({'result': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
