import json
import pickle
from collections import Counter
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

# -----------------------------
# Load dataset
# -----------------------------
with open("wikidata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

X = [d["text"] for d in data]
y = [d["relation"] for d in data]
groups = [d["person"] for d in data]  # ensures same person not in train/test

print("Class distribution in dataset:", Counter(y))

# -----------------------------
# 2️Split into train/test (grouped)
# -----------------------------
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42) # ensures no data leakage by person 
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train = [X[i] for i in train_idx]
y_train = [y[i] for i in train_idx]
X_test = [X[i] for i in test_idx]
y_test = [y[i] for i in test_idx]

print("Train class distribution:", Counter(y_train))
print("Test class distribution:", Counter(y_test))

# -----------------------------
#  Build pipeline (TF-IDF + LogisticRegression)
# -----------------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), lowercase=True)),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
])

# -----------------------------
# Train classifier
# -----------------------------
pipeline.fit(X_train, y_train)

# -----------------------------
#  Evaluate
# -----------------------------
y_pred = pipeline.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0, digits=4))

print("\nConfusion Matrix:")
labels = ["mother", "father", "child", "spouse", "sibling"]
print(confusion_matrix(y_test, y_pred, labels=labels))

cm = confusion_matrix(y_test, y_pred, labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot()
plt.title("Confusion Matrix")
plt.show()

# -----------------------------
#  Save classifier
# -----------------------------
with open("relation_classifier.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("\n Classifier saved as relation_classifier.pkl")