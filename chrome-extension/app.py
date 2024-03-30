from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model, tfidf vectorizer, and label encoder
clf = joblib.load('ensemble_clf.joblib')
tfidf = joblib.load('tfidf_vectorizer.joblib')
label_encoder = joblib.load('label_encoder.joblib')  # Load the label encoder


@app.route('/')
def index():
    return 'Welcome to the Text Classification API'


@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    text = data['text']
    text_tfidf = tfidf.transform([text])
    prediction = clf.predict(text_tfidf)

    # Decode the prediction using the label encoder
    predicted_label = label_encoder.inverse_transform(prediction)[0]

    result = {'classification': predicted_label}
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
