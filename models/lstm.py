import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler

# Load the dataset
file_path = '/content/pakistani_dataset_consolidated_augmented.xlsx'
data = pd.read_excel(file_path)

# Ensure the 'Textual Rating' column exists
if 'Textual Rating' in data.columns and 'Text' in data.columns:
    # Preprocessing -
    # Handle NaN values in 'Text' column
    data['Text'].fillna('', inplace=True)

    # Handle inconsistent data types in 'Textual Rating' column
    data['Textual Rating'] = data['Textual Rating'].astype(str)

    # Encode labels uniformly
    label_encoder = LabelEncoder()
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # Tokenize and pad sequences
    tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
    tokenizer.fit_on_texts(data['Text'])
    sequences = tokenizer.texts_to_sequences(data['Text'])
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, data['Textual Rating'], test_size=0.2, random_state=42
    )

    # Build the updated LSTM model
    model = Sequential()
    model.add(Embedding(input_dim=5000, output_dim=16, input_length=100))
    model.add(Bidirectional(LSTM(100, dropout=0.2, recurrent_dropout=0.2)))
    model.add(Dense(len(label_encoder.classes_), activation='softmax'))

    # Compile the model with a lower initial learning rate
    initial_learning_rate = 0.001
    lr_schedule = LearningRateScheduler(lambda epoch: initial_learning_rate * 0.9 ** epoch)
    optimizer = Adam(learning_rate=initial_learning_rate)
    
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, callbacks=[lr_schedule])

    # Evaluate on the test set
    y_pred_probs = model.predict(X_test)
    y_pred = y_pred_probs.argmax(axis=1)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Additional evaluation metrics
    print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))
