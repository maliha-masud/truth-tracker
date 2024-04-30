import re
from langdetect import detect

def is_gibberish(text):
    # Check for long strings of numbers or letters
    if re.search(r'\b(\w{15,}|[0-9]{15,})\b', text):
        return True

    # Check for repetitive characters (e.g., "aaaaaa")
    if re.search(r'(.)\1{5,}', text):
        return True

    # Check for common keyboard sequences (e.g., "qwerty")
    common_sequences = ["qwerty", "asdfgh", "zxcvbn", "poiuyt", "mnbvcx"]
    for sequence in common_sequences:
        if sequence in text.lower():
            return True

    # # Check for too many consonants in a row without a vowel
    # if re.search(r'[^aeiouyAEIOUY ]{6,}', text):  # Increased threshold for consonants
    #     return True

    return False

def length_validation(text):
    # Split the text into words using whitespace as delimiter
    words = text.split()
    
    # Check if the number of words is at least 3
    if len(words) >= 3:
        return True
    else:
        return False


def language_detection(text):
    language = detect(text)
    return language

# # Example usage:
# text = "What would i know?"
# print(language_detection(text)) #en

# # Example usage
# input_text = input("Enter text to validate: ")
# if is_gibberish(input_text):
#     print("The input appears to be gibberish.")
# else:
#     print("The input seems valid.")
    
# # Example usage
# input_text = input("Enter text to validate: ")
# if length_validation(input_text):
#     print("The input contains at least 5 words.")
# else:
#     print("The input does not contain at least 5 words.")
