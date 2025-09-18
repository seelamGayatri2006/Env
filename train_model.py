import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

os.makedirs("data", exist_ok=True)
os.makedirs("model", exist_ok=True)

# Create synthetic dataset for air pollution monitoring
# features: PM2.5, PM10, NO2, SO2, CO, Temperature, Humidity
def generate_sample(n):
    pm25 = np.abs(np.random.normal(60, 40, n))  
    pm10 = pm25 + np.abs(np.random.normal(10, 20, n))
    no2 = np.abs(np.random.normal(30, 20, n))
    so2 = np.abs(np.random.normal(8, 6, n))
    co = np.abs(np.random.normal(0.8, 0.6, n))
    temp = np.random.normal(25, 7, n)
    hum = np.clip(np.random.normal(60, 20, n), 5, 100)
    return np.vstack([pm25, pm10, no2, so2, co, temp, hum]).T

def label_row(row):
    pm25 = row[0]
    pm10 = row[1]
    no2 = row[2]
    so2 = row[3]
    co = row[4]
    
    score = 0
    if pm25 > 60 or pm10 > 100 or no2 > 80 or so2 > 40 or co > 2.0:
        score += 2
    elif pm25 > 35 or pm10 > 60 or no2 > 40 or so2 > 20 or co > 1.0:
        score += 1
   
    score += np.random.choice([0, 0, 1], p=[0.7,0.2,0.1])
    return min(score, 2)


n = 8000
X = generate_sample(n)
y = np.array([label_row(r) for r in X])

columns = ["PM2_5", "PM10", "NO2", "SO2", "CO", "Temperature", "Humidity"]
df = pd.DataFrame(X, columns=columns)
df["label"] = y
df.to_csv("data/synthetic_air_data.csv", index=False)
print("Saved synthetic dataset to data/synthetic_air_data.csv")

X_train, X_test, y_train, y_test = train_test_split(df[columns], df["label"], test_size=0.2, random_state=42, stratify=df["label"])


clf = RandomForestClassifier(n_estimators=120, random_state=42)
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["Good", "Moderate", "Unhealthy"]))


joblib.dump(clf, "model/model.pkl")
print("Saved model to model/model.pkl")
