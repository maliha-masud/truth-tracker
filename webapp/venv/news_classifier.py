from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

# Load pre-trained BERT model and tokenizer
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def classify_as_news(text, threshold=0.5):
    # Tokenize and preprocess the text
    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    # Make prediction
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1).detach().numpy()

    # Check if the probability of being news is above the threshold
    news_label_index = tokenizer.encode('news', add_special_tokens=False)[0]  # Get the index of the 'news' label
    is_news = probs[0][news_label_index] > threshold

    return is_news, probs[0][1]

# Example usage
# input_text = input("Enter the text you want to classify: ")
# is_news, confidence = classify_as_news(input_text)

# if is_news:
#     print(f"The provided input is classified as news with confidence: {confidence:.2%}")
# else:
#     print("The provided input is not classified as news.")
