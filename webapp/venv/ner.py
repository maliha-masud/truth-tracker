import spacy

def ner(text):
    nlp = spacy.load("en_core_web_sm") # Load English language model
    doc = nlp(text) # Process the text with the NLP pipeline
    entities = [(ent.text, ent.label_) for ent in doc.ents] # Extract named entities & their labels
    
    return entities

# # Example usage
# text = "Hoshi of SEVENTEEN has inspired people around the world to exercise their creativity and maintain disclipine."
# entities = ner(text)
# print(entities)
