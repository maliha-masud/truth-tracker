from textblob import TextBlob
import spacy

def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0.5:
        sentiment = 'Strongly Positive'
    elif sentiment_score > 0:
        sentiment = 'Moderately Positive'
    elif sentiment_score < -0.5:
        sentiment = 'Strongly Negative'
    elif sentiment_score < 0:
        sentiment = 'Moderately Negative'
    else:
        sentiment = 'Neutral'

    return sentiment, round(sentiment_score, 2)

def classify_personal_statement(text):
    nlp = spacy.load("en_core_web_sm") # Load the English language model
    doc = nlp(text) # Process the text using spaCy
    
    # Initialize flags for personal characteristics
    has_personal_subject = False
    has_personal_object = False
    has_personal_verb = False
    
    # Define personal pronouns
    personal_pronouns = ["I", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"]
    
    # Check for personal subject, object, and verb
    for token in doc:
        if token.text.lower() in personal_pronouns and token.dep_ in ["nsubj", "nsubjpass"]:
            has_personal_subject = True
        elif token.text.lower() in personal_pronouns and token.dep_ == "dobj":
            has_personal_object = True
        elif token.text.lower() in personal_pronouns and token.pos_ == "VERB":
            has_personal_verb = True
            
    # Classify based on the presence of personal characteristics
    if has_personal_subject or has_personal_object or has_personal_verb:
        classification = 1 #"Personal Statement"
    else:
        classification = 0 #"Objective Statement"
        
    return classification

# # Example usage:
# text = "It is raining outside. That throws a wrench in my plans."
# sentiment, score = sentiment_analysis(text)
# print(f"Sentiment: {sentiment}, Score: {score}")
