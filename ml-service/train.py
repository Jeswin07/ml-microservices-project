import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load dataset
df = pd.read_csv("data/social_ads.csv")

df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

# Step 2: Features & labels
X = df[["Gender", "Age", "EstimatedSalary"]]
y = df["Purchased"]

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Step 4: Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# Step 6: Save model
joblib.dump(model, "model.pkl")

print("Model saved!")