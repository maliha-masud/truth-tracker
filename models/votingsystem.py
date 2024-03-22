#import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

file_path = 'pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)
    
if 'Textual Rating' in data.columns:
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])
        
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])
    y = data['Textual Rating']

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
    )

    svm_model = SVC(kernel='linear', C=1.0)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    nb_model = MultinomialNB(alpha=0.1)
    lr_model = LogisticRegression(max_iter=1000)

    voting_classifier = VotingClassifier(
    estimators=[
        ('svm', svm_model),
        ('random_forest', rf_model),
        ('naive_bayes', nb_model),
        ('logistic_regression', lr_model)
        ],
        voting='hard'
    )

    voting_classifier.fit(X_train, y_train)

def votingsystem(mytext):
    y_pred = voting_classifier.predict(X_test)
    text_tfidf = tfidf.transform([mytext])
    prediction = voting_classifier.predict(text_tfidf)
    return (label_encoder.inverse_transform(prediction)[0])
