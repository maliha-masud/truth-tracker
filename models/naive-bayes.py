import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Dataset
file_path = 'D:/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Check if the 'Textual Rating' column exists
if 'Textual Rating' in data.columns:
    # Preprocessing - handle NaN values in 'Text' column
    data['Text'].fillna('', inplace=True)

    # Handling inconsistent data types in 'Textual Rating' column
    data['Textual Rating'] = data['Textual Rating'].astype(str)

    # Encoding labels uniformly
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data['Textual Rating']).ravel()  # Flatten the array

    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])

    # Training and testing sets
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(
        X, y, data.index, test_size=0.2, random_state=42
    )

    #  Naive Bayes model training
    model = MultinomialNB(alpha=0.1)  # Alpha value for better performance
    model.fit(X_train, y_train)

    # Prediction on the test set
    y_pred = model.predict(X_test)

    # News with their predicted labels after testing
    for i in range(len(indices_test)):
        idx = indices_test[i]
        print(f"Text: {data['Text'][idx]}\nPredicted Label: {label_encoder.inverse_transform([y_pred[i]])[0]}\n")

    # Calculate accuracy and print at the end
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Additional evaluation metrics and report
    print(classification_report(y_test, y_pred, zero_division=1))

    # Input loop for additional text classification
    while True:
        user_input = input("Enter text for classification (type 'exit' to end): ")
        if user_input.lower() == 'exit':
            break

        # Preprocess user input
        user_input_tfidf = tfidf.transform([user_input])

        # Predict using the trained model
        prediction = model.predict(user_input_tfidf)
        print(f"Predicted Label: {label_encoder.inverse_transform([prediction])[0]}\n")

else:
    print("Column 'Textual Rating' not found in the dataset.")
