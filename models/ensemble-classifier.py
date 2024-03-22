#import necessary libraries
import pandas as pd
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

    # calculate class weights
    class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

    svm_model = SVC(kernel='linear', C=1.0, class_weight=dict(enumerate(class_weights)))
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=dict(enumerate(class_weights)))
    nb_model = MultinomialNB(alpha=0.1)
    lr_model = LogisticRegression(max_iter=1000, class_weight=dict(enumerate(class_weights)))

    # train base classifiers
    svm_model.fit(X_train, y_train)
    rf_model.fit(X_train, y_train)
    nb_model.fit(X_train, y_train)
    lr_model.fit(X_train, y_train)

    # make predictions on test set
    svm_pred = svm_model.predict(X_test)
    rf_pred = rf_model.predict(X_test)
    nb_pred = nb_model.predict(X_test)
    lr_pred = lr_model.predict(X_test)

    # define base classifiers and their corresponding weights
    base_classifiers = [svm_model, rf_model, nb_model, lr_model]
    weights = class_weights

    # calculate accuracy of the weighted ensemble
    weighted_pred = np.sum([clf.predict(X_test) * weight for clf, weight in zip(base_classifiers, weights)], axis=0)
    weighted_pred /= np.sum(weights)  # Normalize by dividing by sum of weights
    weighted_pred = np.round(weighted_pred).astype(int)
    accuracy = accuracy_score(y_test, weighted_pred)
    print(f"Weighted Ensemble Classifier Accuracy: {accuracy:.2f}")

    # print classification report
    print('Weighted Ensemble Classifier Classification Report:\n', classification_report(y_test, weighted_pred))

    # take new input
    while True:
        text = input("Enter text for classification (type 'exit' to end): ")
        if text.lower() == 'exit':
            break
        # preprocess the new input
        text_tfidf = tfidf.transform([text])
        # predict the label using weighted ensemble
        weighted_pred = np.sum([clf.predict(text_tfidf) * weight for clf, weight in zip(base_classifiers, weights)], axis=0)
        weighted_pred /= np.sum(weights)  # normalize by dividing by sum of weights
        prediction = np.round(weighted_pred).astype(int)
        # predicted label
        print(f"\nNew Text: {text}\nPredicted Label: {label_encoder.inverse_transform(prediction)[0]}\n")

else:
    print("Column 'Textual Rating' not found in the dataset.")
