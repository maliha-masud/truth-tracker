import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
file_path = '/content/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Ensure the 'Textual Rating' column exists
if 'Textual Rating' in data.columns:
    # Preprocessing - 
    # Handle NaN values in 'Text' column
    data['Text'].fillna('', inplace=True)

    # Handle inconsistent data types in 'Textual Rating' column
    data['Textual Rating'] = data['Textual Rating'].astype(str)

    # Encode labels uniformly
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])
    y = data['Textual Rating']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(
        X, y, data.index, test_size=0.2, random_state=42
    )

    # Initialize and train the SVM model
    model = SVC(kernel='linear', C=1.0)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Display news with their predicted labels after testing
    for i in range(len(indices_test)):
        idx = indices_test[i]
        print(f"Text: {data['Text'][idx]}\nPredicted Label: {label_encoder.inverse_transform([y_pred[i]])[0]}\n")

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Additional evaluation metrics
    print('Classification Report:\n',classification_report(y_test, y_pred, zero_division=1))

else:
    print("Column 'Textual Rating' not found in the dataset.")
