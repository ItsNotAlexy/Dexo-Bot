import re

def isSpam(text):
    repeated_word_pattern = r"\b(\w+)\b(?:.*\b\1\b){2,}"
    if re.search(repeated_word_pattern, text):
        return True
    
    repeated_char_pattern = r"(.)\1{3,}"
    if re.search(repeated_char_pattern, text):
        return True
    
    url_pattern = r"http[s]?://"
    if re.search(url_pattern, text):
        return True

    return False