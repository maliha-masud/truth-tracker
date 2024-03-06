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

# dataset
file_path = 'C:/Users/khizr/Downloads/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# check if the 'Textual Rating' column exists
if 'Textual Rating' in data.columns:
    # categorical labels into numerical form conversion
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # text data into TF-IDF features conversion
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])
    y = data['Textual Rating']

    # training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # individual models
    svm_model = SVC(kernel='linear', C=1.0)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    nb_model = MultinomialNB(alpha=0.1)
    lr_model = LogisticRegression(max_iter=1000)

    # voting classifier with 'hard' voting (majority voting)
    voting_classifier = VotingClassifier(
        estimators=[
            ('svm', svm_model),
            ('random_forest', rf_model),
            ('naive_bayes', nb_model),
            ('logistic_regression', lr_model)
        ],
        voting='hard'
    )

    # fit the voting classifier on the training data
    voting_classifier.fit(X_train, y_train)

    # predictions on test set
    y_pred = voting_classifier.predict(X_test)

    # accuracy of the voting classifier
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Voting Classifier Accuracy: {accuracy:.2f}")

    # evaluation metrics
    print('Voting Classifier Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))

    # loop for taking new input
    while True:
        text = input("Enter text for classification (type 'exit' to end): ")
        if text.lower() == 'exit':
            break
        # preprocess the new input
        text_tfidf = tfidf.transform([text])
        # predict the label
        prediction = voting_classifier.predict(text_tfidf)
        # display the predicted label
        print(f"\nNew Text: {text}\nPredicted Label: {label_encoder.inverse_transform(prediction)[0]}\n")

else:
    print("Column 'Textual Rating' not found in the dataset.")
