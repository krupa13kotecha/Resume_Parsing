# ================================
# Resume Classification Training
# ================================

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------------------------------
# Step 1: Load Dataset
# -------------------------------
df = pd.read_csv("dataset.csv")

print("Dataset Loaded!")
print(df.columns)

# -------------------------------
# Step 2: Clean Data
# -------------------------------
df = df.dropna()

# Use correct columns
X_text = df["Resume_str"]
y = df["Category"]

# -------------------------------
# Step 3: Text → Numbers
# -------------------------------
vectorizer = TfidfVectorizer(max_features=5000)

X = vectorizer.fit_transform(X_text)

print("Vectorization Done!")

# -------------------------------
# Step 4: Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Step 5: Train Model
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

print("Model Trained!")

# -------------------------------
# Step 6: Evaluate
# -------------------------------
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# -------------------------------
# Step 7: Save Model
# -------------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Saved model & vectorizer!")

# -------------------------------
# Step 8: Test Sample
# -------------------------------
sample_resume = """
Experienced Java developer with Spring Boot, REST APIs, MySQL,
and frontend technologies like HTML, CSS, JS.
"""

sample_vec = vectorizer.transform([sample_resume])
predicted_category = model.predict(sample_vec)[0]

print("\nPredicted Category:", predicted_category)