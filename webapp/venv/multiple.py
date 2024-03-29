import pandas as pd
from myapp.management.commands.preload import dataset
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

# Initialize necessary resources during module import
label_encoder = LabelEncoder()
tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
base_classifiers = [
    SVC(kernel='linear', C=1.0),
    RandomForestClassifier(n_estimators=100, random_state=42),
    MultinomialNB(alpha=0.1),
    LogisticRegression(max_iter=1000)
]
weights = None
one_hot_encoder = None
model_publisher = None

def extract_publisher_site_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else None

def preprocess_input(url, publisher_site):
    if url:
        if not publisher_site:
            publisher_site = extract_publisher_site_from_url(url)
    return url, publisher_site

def ensemble_predict(text_tfidf):
    weighted_pred = np.zeros_like(base_classifiers[0].predict(text_tfidf), dtype=np.float64)
    for clf, weight in zip(base_classifiers, weights):
        weighted_pred += clf.predict(text_tfidf) * weight
    return np.round(weighted_pred).astype(int)

def multiple_inputs(text_input, title=None, URL=None, publisher_site=None, claim_date=None):
    global weights, one_hot_encoder, model_publisher
    if 'Textual Rating' in dataset.columns:
        global label_encoder, tfidf, base_classifiers
        dataset['Textual Rating'] = label_encoder.fit_transform(dataset['Textual Rating'])

        if 'Title' in dataset.columns:
            dataset['Title_Text'] = dataset['Title'].fillna('') + " " + dataset['Text']
            X = tfidf.fit_transform(dataset['Title_Text'])
        else:
            X = tfidf.fit_transform(dataset['Text'])

        y = dataset['Textual Rating']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

        for clf in base_classifiers:
            clf.fit(X_train, y_train)

        global weights
        weights = class_weights / np.sum(class_weights)

        if 'Publisher Site' in dataset.columns:
            global one_hot_encoder, model_publisher
            dataset.dropna(subset=['Publisher Site'], inplace=True)
            dataset['Publisher Site'] = dataset['Publisher Site'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
            dataset['Publisher Site'] = dataset['Publisher Site'].str.lower()
            one_hot_encoder = OneHotEncoder()
            publisher_sites_encoded = one_hot_encoder.fit_transform(dataset[['Publisher Site']])
            X_publisher = publisher_sites_encoded
            y_publisher = dataset['Textual Rating']
            X_train_publisher, X_test_publisher, y_train_publisher, y_test_publisher = train_test_split(
                X_publisher, y_publisher, test_size=0.2, random_state=42
            )
            model_publisher = RandomForestClassifier()
            model_publisher.fit(X_train_publisher, y_train_publisher)

        text = text_input
        if title:
            text = title + ". " + text

        text_tfidf = tfidf.transform([text])

        url, publisher_site = preprocess_input(URL, publisher_site)

        prediction = ensemble_predict(text_tfidf)

        result = label_encoder.inverse_transform(prediction)[0]

        trustworthiness = None
        if 'Publisher Site' in dataset.columns and publisher_site:
            if publisher_site in one_hot_encoder.categories_[0]:
                publisher_site_encoded = one_hot_encoder.transform([[publisher_site]])
                prediction_publisher = model_publisher.predict(publisher_site_encoded)
                trustworthiness = label_encoder.inverse_transform(prediction_publisher)[0]

        outdated_warning = None
        if claim_date and claim_date != "Enter claim date here":
            try:
                if int(claim_date[-4:]) < 2018:
                    outdated_warning = "News might be outdated."
            except ValueError:
                pass

        # Convert result, trustworthiness, and outdated_warning to string for JSON serialization
        result = str(result)
        if trustworthiness is not None:
            trustworthiness = str(trustworthiness)
        if outdated_warning is not None:
            outdated_warning = str(outdated_warning)

        return result, trustworthiness, outdated_warning

    else:
        return "Column 'Textual Rating' not found in the dataset.", None, None
