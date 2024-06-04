from googletrans import Translator

def translate_and_map_urdu_to_english(urdu_sentence):
    translator = Translator()
    
    # Translate the entire sentence
    translated_sentence = translator.translate(urdu_sentence, src='ur', dest='en').text
    
    # Split the sentences into words
    urdu_words = urdu_sentence.split()
    english_words = translated_sentence.split()
    
    # Translate each word individually
    word_map = {}
    for word in urdu_words:
        translated_word = translator.translate(word, src='ur', dest='en').text
        word_map[word] = translated_word
    
    return translated_sentence, word_map

# # Example usage
# urdu_sentence = "میں یہ کام کرنے کی کوشش کر رہا ہوں۔"
# translated_sentence, word_map = translate_and_map_urdu_to_english(urdu_sentence)

# print("Translated Sentence:", translated_sentence)
# print("Word Map:", word_map)
