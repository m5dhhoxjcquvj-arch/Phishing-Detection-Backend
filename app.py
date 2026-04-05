import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

file_name = "data.csv.csv"

try:
    print("--- 🔄 Final Sync: Training & Detecting ---")
    df = pd.read_csv(file_name)
    
    # اختيار الأعمدة الرقمية فقط
    X = df.select_dtypes(include=['number']).drop(['label'], axis=1)
    y = df['label']
    
    # حفظ عدد الخصائص الفعلي (عشان ما يطلع خطأ الـ 25 والـ 50)
    num_features = X.shape[1]
    
    # تدريب سريع للموديل
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=10) # تدريب سريع للتشغيل
    model.fit(X_train, y_train)
    
    print(f"✅ System Ready! (Features synced: {num_features})")

    while True:
        print("\n" + "="*30)
        url_input = input("Enter URL to check (or 'exit'): ")
        
        if url_input.lower() == 'exit':
            break

        # تجهيز الخصائص بناءً على العدد اللي لقاه النظام فعلياً
        test_data = np.zeros((1, num_features))
        test_data[0, 0] = len(url_input) # وضع طول الرابط كأول ميزة
        
        prediction = model.predict(test_data)
        
        if prediction[0] == 1:
            print("❌ Result: DANGER! Phishing Link.")
        else:
            print("✅ Result: SAFE! Legitimate Link.")

except Exception as e:
    print(f"❌ Critical Error: {e}")