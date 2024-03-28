import spacy
from collections import Counter

def ner(text):
    nlp = spacy.load("en_core_web_sm")  # Load English language model
    doc = nlp(text)  # Process the text with the NLP pipeline
    
    # Extract named entities & their labels
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Create a dictionary to store the importance score of each entity
    entity_scores = {}
    
    # Iterate through each entity in the text
    for ent_text, ent_label in entities:
        # Initialize the importance score for the current entity
        entity_scores[(ent_text, ent_label)] = 0
        
        # Iterate through each sentence in the document
        for sent in doc.sents:
            # Check if the entity appears in the current sentence
            if ent_text.lower() in sent.text.lower():
                # Calculate the importance score based on the position of the entity in the sentence
                # Entities mentioned earlier in the sentence or with higher frequency are given higher scores
                entity_scores[(ent_text, ent_label)] += (1 / (doc.text.lower().index(ent_text.lower()) + 1))
    
    # Multiply the scores by 10 and round to 2 decimal places
    for entity, score in entity_scores.items():
        entity_scores[entity] = round(score * 10, 2)
    
    # Define a dictionary to map entity types to their full forms
    entity_labels = {
        'PERSON': 'PERSON',
        'NORP': 'NORP (Nationalities, religious, or political groups)',
        'FAC': 'FACILITY',
        'ORG': 'ORGANIZATION',
        'GPE': 'GPE (Geopolitical Entity)',
        'LOC': 'LOCATION (Non-Geopolitical Entity)',
        'PRODUCT': 'PRODUCT',
        'EVENT': 'EVENT',
        'WORK_OF_ART': 'WORK OF ART',
        'LAW': 'LAW',
        'LANGUAGE': 'LANGUAGE',
        'DATE': 'DATE',
        'TIME': 'TIME',
        'PERCENT': 'PERCENTAGE',
        'MONEY': 'MONEY',
        'QUANTITY': 'QUANTITY',
        'ORDINAL': 'ORDINAL',
        'CARDINAL': 'CARDINAL'
    }
    
    # Sort entities based on their importance scores (highest score first)
    ranked_entities = sorted(entity_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Replace entity labels with their full forms
    ranked_entities = [((entity[0], entity_labels[entity[1]]), score) for entity, score in ranked_entities]
    
    return entities, ranked_entities

# #Example usage:
# text = ""
# entities, ranked_entities = ner(text)

# print("Entities:", entities)
# print("Ranked Entities:", ranked_entities)
