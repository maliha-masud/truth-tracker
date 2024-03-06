# Import necessary libraries
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler

# Dataset
file_path = 'D:/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Check if 'Textual Rating' and 'Text' columns exists
if 'Textual Rating' in data.columns and 'Text' in data.columns:
    # Categorical labels into numerical form conversion
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # Text tokenization and sequence padding
    tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
    tokenizer.fit_on_texts(data['Text'])
    sequences = tokenizer.texts_to_sequences(data['Text'])
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    # Training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, data['Textual Rating'], test_size=0.2, random_state=42
    )

    # A sequential LSTM model
    model = Sequential()
    model.add(Embedding(input_dim=5000, output_dim=16, input_length=100))
    model.add(Bidirectional(LSTM(100, dropout=0.2, recurrent_dropout=0.2)))
    model.add(Dense(len(label_encoder.classes_), activation='softmax'))

    # Compile the LSTM model
    initial_learning_rate = 0.001
    lr_schedule = LearningRateScheduler(lambda epoch: initial_learning_rate * 0.9 ** epoch)
    optimizer = Adam(learning_rate=initial_learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Fit the model on training data
    model.fit(X_train, y_train, epochs=2, batch_size=32, validation_split=0.1, callbacks=[lr_schedule])

    # Predictions on the test set
    y_pred_probs = model.predict(X_test)
    y_pred = y_pred_probs.argmax(axis=1)

    # Accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Evaluation metrics
    print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))

    # Test on new input
    while True:
        text = input("Enter text for classification (type 'exit' to end): ")

        if text.lower() == 'exit':
            break

        # Preprocess the new input
        text_sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(text_sequence, maxlen=100, padding='post', truncating='post')

        # Prediction using the trained model
        user_input_pred_probs = model.predict(padded_sequence)
        user_input_pred = user_input_pred_probs.argmax(axis=1)

        # Predictions
        predicted_label = label_encoder.inverse_transform(user_input_pred)[0]
        print(f"\nNew Text: {text}\nPredicted Label: {predicted_label}\n")


    print("\nExiting the program.")

else:
    print("Column 'Textual Rating' not found in the dataset.")
