#import necessary libraries
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

# load excel dataset
file_path = '/content/pakistani_dataset_consolidated_augmented.xlsx'
# store as dataframe
data = pd.read_excel(file_path)

# check for textual rating column 
if 'Textual Rating' in data.columns and 'Text' in data.columns:
    # convert categorical labels into numerical form by using label encoding
    label_encoder = LabelEncoder()
    # textual rating column is replaced with encoded numerical values using fit_transform
    data['Textual Rating'] = label_encoder.fit_transform(data['Textual Rating'])

    # perform text tokenization and sequence padding
    tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
    # fit tokenizer on text data
    tokenizer.fit_on_texts(data['Text'])
    #convert text data into sequences of integers
    sequences = tokenizer.texts_to_sequences(data['Text'])
    #pad sequences to ensure uniform length
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    # split data into 80% training and 20% testing set
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, data['Textual Rating'], test_size=0.2, random_state=42
    )

    # create sequential lstm model
    model = Sequential()
    # convert integer-encoded vocabulary into dense vectors
    model.add(Embedding(input_dim=5000, output_dim=16, input_length=100))
    # lstm layer can process input sequences in both forward and backward directions
    model.add(Bidirectional(LSTM(100, dropout=0.2, recurrent_dropout=0.2)))
    #a fully connected layer with a softmax activation function
    model.add(Dense(len(label_encoder.classes_), activation='softmax'))

    # compile lstm model with initial learning rate
    initial_learning_rate = 0.001
    # schedule learning rate (decreases learning rate by 10% every epoch).
    lr_schedule = LearningRateScheduler(lambda epoch: initial_learning_rate * 0.9 ** epoch)
    # optimize model using optimization algorithm
    optimizer = Adam(learning_rate=initial_learning_rate)

    #configure model for training
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # fit model on training data
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, callbacks=[lr_schedule])

    # make predictions on test set
    y_pred_probs = model.predict(X_test)
    y_pred = y_pred_probs.argmax(axis=1)

    # calculate and print accuracy of model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # print additional evaluation metrics in form of classification report
    print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))
    
else:
    print("Column 'Textual Rating' not found in the dataset.")
