#import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Dataset
file_path = 'D:/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Check if the 'Textual Rating' column exists in the data
if 'Textual Rating' in data.columns:
    # Categorical labels into numerical form conversion
    label_encoder = LabelEncoder()
    # Textual rating column is replaced with encoded numerical values
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # Text data into TF-IDF features conversion
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])
    # Target variable
    y = data['Textual Rating']

    # Training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Support vector classification model
    model = SVC(kernel='linear', C=1.0)
    # fit model on training data
    model.fit(X_train, y_train)

    # Predictions on test set
    y_pred = model.predict(X_test)

    # Text of news with predicted labels for test set
    for i in range(len(y_test)):
        index = y_test.index[i]
        print(f"Text: {data['Text'].iloc[index]}\nPredicted Label: {label_encoder.inverse_transform([y_pred[i]])[0]}\n")

    # Accuracy of model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # evaluation metrics
    print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))

    # test on new input
    while True:
        text = input("Enter text for classification (type 'exit' to end): ")
        if text.lower() == 'exit':
            break
        # preprocess the new input
        text_tfidf = tfidf.transform([text])
        # predict the label
        prediction = model.predict(text_tfidf)
        # display the predicted label
        print(f"\nNew Text: {text}\nPredicted Label: {label_encoder.inverse_transform(prediction)[0]}\n")

else:
    print("Column 'Textual Rating' not found in the dataset.")
