# Import necessary libraries
import pandas as pd
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import class_weight
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import re
import joblib

# Function to extract Publisher Site from URL
def extract_publisher_site_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else None

# Function to preprocess user input
def preprocess_input(url, publisher_site):
    if url:
        if not publisher_site:
            # Extract Publisher Site from URL
            publisher_site = extract_publisher_site_from_url(url)
            print("Extracted Publisher Site:", publisher_site)  # Print the extracted domain

    return url, publisher_site

# Load the dataset
file_path = r'D:\pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Fill NaN values with empty strings for text processing
data.fillna('', inplace=True)

# Check and print the unique values in 'Textual Rating' to understand what's in there
print(data['Textual Rating'].unique())

# Encode the 'Textual Rating' column (Ensure that all values are strings)
label_encoder = LabelEncoder()
data['Encoded Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'].astype(str))

# Save the label encoder
joblib.dump(label_encoder, 'label_encoder.joblib')

# Check if the 'Title' column exists and combine with 'Text' column if it does
data['Combined Text'] = data['Title'].fillna('') + " " + data['Text'].fillna('')

# Extract features with TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
X = tfidf.fit_transform(data['Combined Text'])

# Encode the target variable
y = data['Encoded Textual Rating']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calculate class weights
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

# Define base classifiers
classifiers = [
    SVC(kernel='linear', C=1.0, class_weight=dict(enumerate(class_weights))),
    RandomForestClassifier(n_estimators=100, random_state=42, class_weight=dict(enumerate(class_weights))),
    MultinomialNB(alpha=0.1),
    LogisticRegression(max_iter=1000, class_weight=dict(enumerate(class_weights)))
]

# Train each classifier and store them in a dictionary
trained_classifiers = {}
for clf in classifiers:
    clf_name = clf.__class__.__name__
    print(f"Training {clf_name}...")
    clf.fit(X_train, y_train)
    trained_classifiers[clf_name] = clf

    # Predict on the test set
    y_pred = clf.predict(X_test)

    # Print the classification report
    print(f"Classification Report for {clf_name}:")
    print(classification_report(y_test, y_pred))

# Assuming you have chosen one classifier as your best model, or you could ensemble them
# For simplicity, let's say the RandomForestClassifier was chosen
best_model = trained_classifiers['RandomForestClassifier']

# Save the best model and the tfidf vectorizer to disk for later use in Flask app
joblib.dump(best_model, 'ensemble_clf.joblib')
joblib.dump(tfidf, 'tfidf_vectorizer.joblib')

print("Model and vectorizer have been saved.")
