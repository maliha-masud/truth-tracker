#import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# load excel dataset
file_path = '/content/pakistani_dataset_consolidated_augmented.xlsx'
# store as dataframe
data = pd.read_excel(file_path)

# check for textual rating column 
if 'Textual Rating' in data.columns:
    # convert categorical labels into numerical form by using label encoding
    label_encoder = LabelEncoder()
    # textual rating column is replaced with encoded numerical values using fit_transform
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # convert text data into TF-IDF features using TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X = tfidf.fit_transform(data['Text'])
    # assign target variable
    y = data['Textual Rating']

    # split data into 80% training and 20% testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # create support vector classification model using a linear kernel
    model = SVC(kernel='linear', C=1.0)
    # fit model on training data
    model.fit(X_train, y_train)

    # make predictions on test set
    y_pred = model.predict(X_test)

    # display text of news with predicted labels for test set
    for i in range(len(y_test)):
        index = y_test.index[i]
        print(f"Text: {data['Text'].iloc[index]}\nPredicted Label: {label_encoder.inverse_transform([y_pred[i]])[0]}\n")

    # calculate and print accuracy of model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # print additional evaluation metrics in form of classification report
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
