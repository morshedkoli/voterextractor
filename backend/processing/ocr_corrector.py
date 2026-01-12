import os
import difflib
from typing import List, Dict

# Global dictionary cache
_DICTIONARY_CACHE = None

def load_dictionary() -> List[str]:
    """
    Loads the approved Bengali dictionary from file.
    """
    global _DICTIONARY_CACHE
    if _DICTIONARY_CACHE is not None:
        return _DICTIONARY_CACHE
        
    try:
        # Resolve path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Up one level to backend, then into data
        dict_path = os.path.join(current_dir, '..', 'data', 'bengali_dictionary.txt')
        
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            _DICTIONARY_CACHE = words
            return words
    except Exception as e:
        print(f"[WARNING] Failed to load dictionary: {e}")
        
    return []

def fix_ocr_corruptions(text: str) -> str:
    """
    Fixes severely corrupted Bengali words based on an approved dictionary.
    
    1. Replaces known specific corruptions (hardcoded map).
    2. Scans text for words close to dictionary entries and auto-corrects them.
    """
    if not text:
        return ""
        
    # 1. Hardcoded Map for known garbage strings
    corruption_map = {
        "ছিসি্ফর": "ছিদ্দিকুর",
        "ছিসি্ফক": "ছিদ্দিক",
        "উসি্ফন": "উদ্দিন",
        "ইষি্টস": "ইদ্রিছ",
        "ইষি্টছ": "ইদ্রিছ",
        "আুল": "আব্দুল",
        "কামাহার": "কামরুন্নাহার",
        "খদ্দকিার": "খন্দকার",
    }
    
    for corrupt, correct in corruption_map.items():
        if corrupt in text:
            text = text.replace(corrupt, correct)

    # 2. Fuzzy Dictionary Matching
    # Load dictionary
    dictionary = load_dictionary()
    if not dictionary:
        return text
        
    # Split text into tokens to check against dictionary
    # We use a simple space split, preserving original tokens for replacement
    tokens = text.split()
    corrected_tokens = []
    
    for token in tokens:
        # Skip very short tokens or numbers
        if len(token) < 3 or token.isnumeric():
            corrected_tokens.append(token)
            continue
            
        # Check for exact match first
        if token in dictionary:
            corrected_tokens.append(token)
            continue
            
        # Fuzzy match
        # get_close_matches(word, possibilities, n, cutoff)
        # cutoff=0.8 means 80% similarity required
        matches = difflib.get_close_matches(token, dictionary, n=1, cutoff=0.85)
        
        if matches:
            # Replace with the best match
            corrected_tokens.append(matches[0])
        else:
            corrected_tokens.append(token)
            
    return " ".join(corrected_tokens)
