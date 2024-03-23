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
file_path = r'C:\Users\khizr\Downloads\truth-tracker-master\pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

if 'Textual Rating' in data.columns:
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))

    if 'Title' in data.columns:  # Title is available
        # Concatenate Title and Text
        data['Title_Text'] = data['Title'].fillna('') + " " + data['Text']

        X = tfidf.fit_transform(data['Title_Text'])
    else:  # Title is not available
        X = tfidf.fit_transform(data['Text'])

    y = data['Textual Rating']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Calculate class weights
    class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

    # Define base classifiers
    base_classifiers = [
        SVC(kernel='linear', C=1.0, class_weight=dict(enumerate(class_weights))),
        RandomForestClassifier(n_estimators=100, random_state=42, class_weight=dict(enumerate(class_weights))),
        MultinomialNB(alpha=0.1),
        LogisticRegression(max_iter=1000, class_weight=dict(enumerate(class_weights)))
    ]

    # Train base classifiers
    for clf in base_classifiers:
        clf.fit(X_train, y_train)

    # Define corresponding weights for base classifiers
    weights = class_weights / np.sum(class_weights)

    # Define a function for ensemble prediction
    def ensemble_predict(text_tfidf):
        weighted_pred = np.zeros_like(base_classifiers[0].predict(X_test), dtype=np.float64)
        for clf, weight in zip(base_classifiers, weights):
            weighted_pred += clf.predict(text_tfidf) * weight
        return np.round(weighted_pred).astype(int)
    
        # Train a separate model for Publisher Site
    if 'Publisher Site' in data.columns:
         # Drop rows with empty Publisher Site values
        data.dropna(subset=['Publisher Site'], inplace=True)

         # Remove punctuation and special characters
        data['Publisher Site'] = data['Publisher Site'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))

        # convert to lowercase
        data['Publisher Site'] = data['Publisher Site'].str.lower()

        # One-hot encode Publisher Site
        one_hot_encoder = OneHotEncoder()
        publisher_sites_encoded = one_hot_encoder.fit_transform(data[['Publisher Site']])

        # Extract features and target variable
        X_publisher = publisher_sites_encoded
        y_publisher = data['Textual Rating']

        # Split data into training and testing sets
        X_train_publisher, X_test_publisher, y_train_publisher, y_test_publisher = train_test_split(
            X_publisher, y_publisher, test_size=0.2, random_state=42
        )

        # Train a Random Forest Classifier for Publisher Site
        model_publisher = RandomForestClassifier()
        model_publisher.fit(X_train_publisher, y_train_publisher)


    # Take new input
    while True:
        text = input("Enter text for classification (type 'exit' to end): ")
        if text.lower() == 'exit':
            break
        title = input("Enter title (press Enter to skip): ")
        url = input("Enter URL (press Enter to skip): ")
        publisher_site = input("Enter Publisher Site (press Enter to skip): ")
        claim_date = input("Enter Claim Date in the format 'Month Day, Year' (e.g., 'March 23, 2024'), or press Enter to skip: ")

        # Concatenate text and title if provided
        if title:
            text = title + ". " + text

        # Preprocess the new input
        text_tfidf = tfidf.transform([text])

        # Preprocess URL and Publisher Site
        url, publisher_site = preprocess_input(url, publisher_site)

        # Predict using weighted ensemble
        prediction = ensemble_predict(text_tfidf)

        # Print predicted label
        print(f"\nNew Text: {text}\nPredicted Label: {label_encoder.inverse_transform(prediction)[0]}\n")
         # Predict trustworthiness based on Publisher Site model
        if 'Publisher Site' in data.columns and publisher_site:
            if publisher_site in one_hot_encoder.categories_[0]:
                publisher_site_encoded = one_hot_encoder.transform([[publisher_site]])
                prediction_publisher = model_publisher.predict(publisher_site_encoded)
                if label_encoder.inverse_transform(prediction_publisher)[0] == 'True':
                    print("The source is likely to be trustworthy.")
                else:
                    print("The source is likely not trustworthy.")
            else:
                print("Cannot determine if source is trustworthy.")
        
        # Check if claim date is provided and older than 2018
        if claim_date and int(claim_date[-4:]) < 2018:
           try:
                if int(claim_date[-4:]) < 2018:
                    print("Warning: News might be outdated.")
           except ValueError:
                print("Invalid date format. Please enter the claim date in the format 'Month Day, Year' (e.g., 'March 23, 2024').")

else:
    print("Column 'Textual Rating' not found in the dataset.")
