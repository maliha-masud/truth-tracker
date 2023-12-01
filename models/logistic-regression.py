import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset from Excel file
file_path = 'D:/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows to understand the data and check columns
print(data.head())
print(data.columns)

# Ensure the 'Textual Rating' column exists in your data
if 'Textual Rating' in data.columns:
    # Preprocessing - handle NaN values in 'Text' column and convert text to numerical form using TF-IDF
    data['Text'].fillna('', inplace=True)  # Replace NaN values with empty strings

    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(data['Text'])  # Assuming 'Text' is the column containing the textual data
    y = data['Textual Rating']  # Assuming 'Textual Rating' is the target variable

    # Convert non-boolean values in the target column to strings
    y = y.astype(str)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Additional evaluation metrics and report
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

else:
    print("Column 'Textual Rating' not found in the dataset.")
