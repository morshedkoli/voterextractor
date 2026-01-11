import re

def fix_broken_conjuncts(text: str, field_type: str = "conservative") -> str:
    """
    Fix broken Bengali conjuncts that were separated during OCR/PDF extraction.
    
    Args:
        text: Input Bengali text with potentially broken conjuncts
        field_type: "aggressive" or "conservative" - determines fixing confidence level
    
    Returns:
        Fixed Bengali text with restored conjuncts
    """
    if not text or not isinstance(text, str):
        return text
    
    # Updated High-confidence conjuncts including missing ones inferred from examples
    high_confidence_conjuncts = {
        # Common 2-letter conjuncts
        ('ক', 'ষ'): 'ক্ষ',
        ('ক', 'ত'): 'ক্ত',  # Added from example "শক্তি"
        ('ত', 'র'): 'ত্র',
        ('জ', 'ঞ'): 'জ্ঞ',
        ('শ', 'র'): 'শ্র',
        ('ন', 'ত'): 'ন্ত',
        ('ন', 'দ'): 'ন্দ',
        ('ন', 'ধ'): 'ন্ধ',
        ('ঙ', 'গ'): 'ঙ্গ',
        ('ঙ', 'ঘ'): 'ঙ্ঘ',
        ('ঞ', 'চ'): 'ঞ্চ',
        ('ঞ', 'ছ'): 'ঞ্ছ',
        ('ঞ', 'জ'): 'ঞ্জ',
        ('ঞ', 'ঝ'): 'ঞ্ঝ',
        ('ষ', 'ট'): 'ষ্ট',
        ('ষ', 'ঠ'): 'ষ্ঠ',
        ('স', 'ত'): 'স্ত',
        ('স', 'থ'): 'স্থ',
        ('স', 'ক'): 'স্ক',
        ('স', 'প'): 'স্প',
        ('দ', 'ধ'): 'দ্ধ',
        ('দ', 'ব'): 'দ্ব',
        ('দ', 'গ'): 'দ্গ',
        ('দ', 'ভ'): 'দ্ভ',
        ('দ', 'ম'): 'দ্ম',
        ('দ', 'দ'): 'দ্দ',
        ('ম', 'প'): 'ম্প',
        ('ম', 'ফ'): 'ম্ফ',
        ('ম', 'ব'): 'ম্ব',
        ('ম', 'ভ'): 'ম্ভ',
        ('ণ', 'ড'): 'ণ্ড',
        ('ণ', 'ঢ'): 'ণ্ঢ',
        ('ণ', 'ঠ'): 'ণ্ঠ',
        ('ণ', 'ণ'): 'ণ্ণ',
        ('ল', 'প'): 'ল্প',
        ('ল', 'ক'): 'ল্ক',
        ('ল', 'গ'): 'ল্গ',
        ('ল', 'ট'): 'ল্ট',
        ('ল', 'ড'): 'ল্ড',
        ('ল', 'ম'): 'ল্ম',
        ('র', 'ক'): 'র্ক',
        ('র', 'গ'): 'র্গ',
        ('র', 'চ'): 'র্চ',
        ('র', 'ত'): 'র্ত',
        ('র', 'দ'): 'র্দ',
        ('র', 'ন'): 'র্ন',
        ('র', 'ম'): 'র্ম',
        ('র', 'য'): 'র্য',
        ('র', 'ল'): 'র্ল',
    }
    
    # 3-letter conjuncts
    three_letter_conjuncts = {
        ('স', 'ত', 'র'): 'স্ত্র',
    }
    
    # Regex to find digits
    digit_pattern = re.compile(r'[০-৯0-9]')
    
    result = text
    
    def safe_replace(match, replacement):
        # Check context: 2 chars before and after match
        start, end = match.span()
        # Look back 2 chars (safely)
        lookback_start = max(0, start - 2)
        lookahead_end = min(len(result), end + 2)
        
        context_before = result[lookback_start:start]
        context_after = result[end:lookahead_end]
        
        # If digit is active in context -> SKIP
        if digit_pattern.search(context_before) or digit_pattern.search(context_after):
            return match.group(0) # Return original text
            
        return replacement

    # Fix 3-letter conjuncts first
    for (c1, c2, c3), conjunct in three_letter_conjuncts.items():
        pattern = f'({c1}\\s+{c2}\\s+{c3})'
        result = re.sub(pattern, lambda m: safe_replace(m, conjunct), result)
    
    # Fix 2-letter conjuncts
    for (c1, c2), conjunct in high_confidence_conjuncts.items():
        pattern = f'({c1}\\s+{c2})'
        # Optimized callback replacement
        result = re.sub(pattern, lambda m: safe_replace(m, conjunct), result)
        
    return result.strip()
