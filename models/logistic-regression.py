import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dataset
file_path = 'D:/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# first few rows to understand the data \
print(data.head())
print(data.columns)

# Check if the 'Textual Rating' column exists
if 'Textual Rating' in data.columns:
    # Preprocessing - handle NaN values in 'Text' column and text to numerical form conversion
    data['Text'].fillna('', inplace=True)

    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(data['Text'])
    y = data['Textual Rating']  # Assuming 'Textual Rating' is the target variable

    # Non-boolean values in the target column to strings conversion
    y = y.astype(str)

    # Training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Prediction on the test set
    y_pred = model.predict(X_test)

    # Model Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Evaluation metrics and report
    print(classification_report(y_test, y_pred, zero_division=0))

    # Training and Testing Accuracy Graphs
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    plt.figure(figsize=(8, 6))
    plt.bar(['Training Accuracy', 'Testing Accuracy'], [train_acc, test_acc], color=['blue', 'orange'])
    plt.ylim(0, 1)
    plt.title('Model Training and Testing Accuracy')
    plt.ylabel('Accuracy')
    plt.show()

    # User Input for classification
    while True:
        user_input = input("Enter text for classification (type 'exit' to end): ")
        if user_input.lower() == 'exit':
            break

        # Preprocess user input
        user_input_tfidf = tfidf.transform([user_input])

        # Predictions using the trained model
        prediction = model.predict(user_input_tfidf)
        print(f"Predicted Rating: {prediction[0]}")

else:
    print("Column 'Textual Rating' not found in the dataset.")
