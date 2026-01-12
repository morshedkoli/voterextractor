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
        # Removed risky ones that start with common word-ending letters (র, ন, ল, ম, স etc)
        # to prevent merging separate words like "Abdur Rahman" -> "Abdurrahman"
        ('ক', 'ষ'): 'ক্ষ',
        ('ক', 'ত'): 'ক্ত',
        ('ক', 'র'): 'ক্র',
        ('ক', 'ল'): 'ক্ল',
        ('ক', 'ব'): 'ক্ব',
        ('ক', 'ম'): 'ক্ম',
        ('খ', 'র'): 'খ্র',
        ('গ', 'ধ'): 'গ্ধ',
        ('গ', 'র'): 'গ্র',
        ('গ', 'ল'): 'গ্ল',
        ('গ', 'ন'): 'গ্ন',
        ('ঘ', 'র'): 'ঘ্র',
        ('ঘ', 'ন'): 'ঘ্ন',
        ('ঙ', 'ক'): 'ঙ্ক',
        ('ঙ', 'খ'): 'ঙ্খ',
        ('ঙ', 'গ'): 'ঙ্গ',
        ('ঙ', 'ঘ'): 'ঙ্ঘ',
        ('চ', 'চ'): 'চ্চ',
        ('চ', 'ছ'): 'চ্ছ',
        ('চ', 'ঞ'): 'চ্ঞ',
        ('জ', 'জ'): 'জ্জ',
        ('জ', 'ঝ'): 'জ্ঝ',
        ('জ', 'ঞ'): 'জ্ঞ',
        ('জ', 'ব'): 'জ্ব',
        ('ঞ', 'চ'): 'ঞ্চ',
        ('ঞ', 'ছ'): 'ঞ্ছ',
        ('ঞ', 'জ'): 'ঞ্জ',
        ('ঞ', 'ঝ'): 'ঞ্ঝ',
        ('ট', 'ট'): 'ট্ট',
        ('ড', 'ড'): 'ড্ড',
        ('ণ', 'ট'): 'ণ্ট',
        ('ণ', 'ঠ'): 'ণ্ঠ',
        ('ণ', 'ড'): 'ণ্ড',
        ('ণ', 'ঢ'): 'ণ্ঢ',
        ('ণ', 'ণ'): 'ণ্ণ',
        ('ত', 'ত'): 'ত্ত',
        ('ত', 'থ'): 'ত্থ',
        ('ত', 'ন'): 'ত্ন',
        ('ত', 'ব'): 'ত্ব',
        ('ত', 'ম'): 'ত্ম',
        ('ত', 'র'): 'ত্র',
        ('থ', 'র'): 'থ্র',
        ('দ', 'গ'): 'দ্গ',
        ('দ', 'ঘ'): 'দ্ঘ',
        ('দ', 'দ'): 'দ্দ',
        ('দ', 'ধ'): 'দ্ধ',
        ('দ', 'ব'): 'দ্ব',
        ('দ', 'ভ'): 'দ্ভ',
        ('দ', 'ম'): 'দ্ম',
        ('দ', 'র'): 'দ্র',
        ('ধ', 'ন'): 'ধ্ন',
        ('ধ', 'র'): 'ধ্র',
        ('ধ', 'ব'): 'ধ্ব',
        # Re-enabled safe 'n' conjuncts
        ('ন', 'ত'): 'ন্ত',
        ('ন', 'দ'): 'ন্দ',
        ('ন', 'ধ'): 'ন্ধ',
        ('ন', 'ন'): 'ন্ন', # For Kamrunnahar
        ('প', 'ত'): 'প্ত',
        ('প', 'প'): 'প্প',
        ('প', 'ল'): 'প্ল',
        ('প', 'স'): 'প্স',
        ('প', 'র'): 'প্র',
        ('ফ', 'ল'): 'ফ্ল',
        ('ফ', 'র'): 'ফ্র',
        ('ব', 'জ'): 'ব্জ',
        ('ব', 'দ'): 'ব্দ', # For Abdullah
        ('ব', 'ধ'): 'ব্ধ',
        ('ব', 'ব'): 'ব্ব',
        ('ব', 'ল'): 'ব্ল',
        ('ব', 'র'): 'ব্র',
        ('ভ', 'র'): 'ভ্র',
        ('ম', 'প'): 'ম্প',
        ('ম', 'ফ'): 'ম্ফ',
        ('ম', 'ব'): 'ম্ব',
        ('ম', 'ভ'): 'ম্ভ',
        ('ম', 'ম'): 'ম্ম',
        ('ম', 'র'): 'ম্র',
        ('ম', 'ল'): 'ম্ল',
        ('য', 'র'): 'য্র', 
        # Re-enabled safe 'l' conjuncts
        ('ল', 'ক'): 'ল্ক',
        ('ল', 'গ'): 'ল্গ',
        ('ল', 'প'): 'ল্প',
        ('ল', 'ফ'): 'ল্ফ',
        ('ল', 'ম'): 'ল্ম',
        ('ল', 'ল'): 'ল্ল', # For Abdullah
        ('ল', 'ব'): 'ল্ব',
        ('শ', 'চ'): 'শ্চ',
        ('শ', 'ছ'): 'শ্ছ',
        ('শ', 'ন'): 'শ্ন',
        ('শ', 'ব'): 'শ্ব',
        ('শ', 'ম'): 'শ্ম',
        ('শ', 'ল'): 'শ্ল',
        ('শ', 'র'): 'শ্র',
        ('ষ', 'ক'): 'ষ্ক',
        ('ষ', 'ট'): 'ষ্ট',
        ('ষ', 'ঠ'): 'ষ্ঠ',
        ('ষ', 'ণ'): 'ষ্ণ',
        ('ষ', 'প'): 'ষ্প',
        ('ষ', 'ফ'): 'ষ্ফ',
        ('ষ', 'ম'): 'ষ্ম',
        ('স', 'ক'): 'স্ক',
        ('স', 'খ'): 'স্খ',
        ('স', 'ট'): 'স্ট',
        ('স', 'ত'): 'স্ত',
        ('স', 'থ'): 'স্থ',
        ('স', 'ন'): 'স্ন',
        ('স', 'প'): 'স্প',
        ('স', 'ফ'): 'স্ফ',
        ('স', 'ব'): 'স্ব',
        ('স', 'ম'): 'স্ম',
        ('স', 'ল'): 'স্ল',
        ('স', 'র'): 'স্র',
        ('হ', 'ণ'): 'হ্ণ',
        ('হ', 'ন'): 'হ্ন',
        ('হ', 'ম'): 'হ্ম',
        ('হ', 'ল'): 'হ্ল',
        ('হ', 'ব'): 'হ্ব',
        ('হ', 'র'): 'হ্র',
        ('ক', 'ষ'): 'ক্ষ',
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
