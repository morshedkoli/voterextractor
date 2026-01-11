import re

def replace_cids(text: str) -> str:
    """
    Replaces common PDF CID codes with their Bengali equivalents.
    Comprehensive mapping for Bengali conjuncts (যুক্তাক্ষর).
    """
    # Comprehensive CID mapping for Bengali conjuncts
    # Note: These mappings are specific to the user's PDF font
    cid_map = {
        # Vowel signs
        "(cid:207)": "\u09c7",  # ে (e-kar)
        
        # Consonants with vowels
        "(cid:387)": "\u09a6\u09c1",  # দু (da + u-kar)
        
        # Common conjuncts (যুক্তাক্ষর)
        "(cid:215)": "\u0995\u09cd\u09a4",  # ক্ত (k + virama + t)
        "(cid:216)": "\u0995\u09cd\u09b7",  # ক্ষ (k + virama + sh)
        "(cid:293)": "\u09a8\u09cd\u09ae",  # ন্ম (n + virama + m)
        "(cid:324)": "\u09ae\u09cd\u09ac",  # ম্ব (m + virama + b)
        "(cid:340)": "\u09b6\u09cd\u099a",  # শ্চ (sha + virama + cha)
        "(cid:214)": "\u0995\u09cd\u0995",  # ক্ক (k + virama + k)
        "(cid:233)": "\u09a8\u09cd\u09a4",  # ন্ত (n + virama + t)
        "(cid:234)": "\u09a8\u09cd\u09a5",  # ন্থ (n + virama + th)
        "(cid:235)": "\u09a8\u09cd\u09a6",  # ন্দ (n + virama + d)
        "(cid:236)": "\u09a8\u09cd\u09a7",  # ন্ধ (n + virama + dh)
        "(cid:237)": "\u09a8\u09cd\u09a8",  # ন্ন (n + virama + n)
        "(cid:255)": "\u09aa\u09cd\u09a4",  # প্ত (p + virama + t)
        "(cid:256)": "\u09aa\u09cd\u09aa",  # প্প (p + virama + p)
        "(cid:257)": "\u09aa\u09cd\u09b0",  # প্র (p + virama + r)
        "(cid:276)": "\u09b8\u09cd\u09a4",  # স্ত (s + virama + t)
        "(cid:277)": "\u09b8\u09cd\u09a5",  # স্থ (s + virama + th)
        "(cid:278)": "\u09b8\u09cd\u09aa",  # স্প (s + virama + p)
        "(cid:279)": "\u09b8\u09cd\u09ab",  # স্ফ (s + virama + ph)
        "(cid:217)": "\u0997\u09cd\u09a7",  # গ্ধ (g + virama + dh)
        "(cid:218)": "\u0997\u09cd\u09b0",  # গ্র (g + virama + r)
        "(cid:241)": "\u09a6\u09cd\u09a6",  # দ্দ (d + virama + d)
        "(cid:242)": "\u09a6\u09cd\u09a7",  # দ্ধ (d + virama + dh)
        "(cid:243)": "\u09a6\u09cd\u09ac",  # দ্ব (d + virama + b)
        "(cid:244)": "\u09a6\u09cd\u09ad",  # দ্ভ (d + virama + bh)
        "(cid:245)": "\u09a6\u09cd\u09ae",  # দ্ম (d + virama + m)
        "(cid:265)": "\u09b2\u09cd\u09aa",  # ল্প (l + virama + p)
        "(cid:266)": "\u09b2\u09cd\u09ab",  # ল্ফ (l + virama + ph)
        "(cid:267)": "\u09b2\u09cd\u09ac",  # ল্ব (l + virama + b)
        "(cid:268)": "\u09b2\u09cd\u09ae",  # ল্ম (l + virama + m)
        "(cid:269)": "\u09b2\u09cd\u09b2",  # ল্ল (l + virama + l)
        "(cid:283)": "\u09b9\u09cd\u09a3",  # হ্ণ (h + virama + n-dot)
        "(cid:284)": "\u09b9\u09cd\u09a8",  # হ্ন (h + virama + n)
        "(cid:285)": "\u09b9\u09cd\u09ae",  # হ্ম (h + virama + m)
        "(cid:286)": "\u09b9\u09cd\u09b2",  # হ্ল (h + virama + l)
        "(cid:220)": "\u099c\u09cd\u099c",  # জ্জ (j + virama + j)
        "(cid:221)": "\u099c\u09cd\u099e",  # জ্ঞ (j + virama + ny)
        "(cid:222)": "\u099f\u09cd\u099f",  # ট্ট (tt + virama + tt)
        "(cid:223)": "\u09a3\u09cd\u09a0",  # ণ্ঠ (n-dot + virama + tth)
        "(cid:224)": "\u09a3\u09cd\u09a1",  # ণ্ড (n-dot + virama + dd)
        "(cid:225)": "\u09a3\u09cd\u09a2",  # ণ্ঢ (n-dot + virama + ddh)
        "(cid:226)": "\u09a3\u09cd\u09a3",  # ণ্ণ (n-dot + virama + n-dot)
        "(cid:227)": "\u09a4\u09cd\u09a4",  # ত্ত (t + virama + t)
        "(cid:228)": "\u09a4\u09cd\u09a5",  # ত্থ (t + virama + th)
        "(cid:229)": "\u09a4\u09cd\u09a8",  # ত্ন (t + virama + n)
        "(cid:230)": "\u09a4\u09cd\u09ae",  # ত্ম (t + virama + m)
        "(cid:231)": "\u09a4\u09cd\u09b0",  # ত্র (t + virama + r)
        "(cid:258)": "\u09ac\u09cd\u09a6",  # ব্দ (b + virama + d)
        "(cid:259)": "\u09ac\u09cd\u09a7",  # ব্ধ (b + virama + dh)
        "(cid:260)": "\u09ac\u09cd\u09ac",  # ব্ব (b + virama + b)
        "(cid:261)": "\u09ac\u09cd\u09af",  # ব্য (b + virama + y)
        "(cid:262)": "\u09ac\u09cd\u09b0",  # ব্র (b + virama + r)
        "(cid:263)": "\u09ad\u09cd\u09b0",  # ভ্র (bh + virama + r)
        "(cid:270)": "\u09b6\u09cd\u099a",  # শ্চ (sh + virama + ch)
        "(cid:271)": "\u09b6\u09cd\u099b",  # শ্ছ (sh + virama + chh)
        "(cid:272)": "\u09b6\u09cd\u09a4",  # শ্ত (sh + virama + t)
        "(cid:273)": "\u09b6\u09cd\u09a8",  # শ্ন (sh + virama + n)
        "(cid:274)": "\u09b6\u09cd\u09ae",  # শ্ম (sh + virama + m)
        "(cid:275)": "\u09b6\u09cd\u09b0",  # শ্র (sh + virama + r)
        "(cid:280)": "\u09b7\u09cd\u0995",  # ষ্ক (sh-dot + virama + k)
        "(cid:281)": "\u09b7\u09cd\u099f",  # ষ্ট (sh-dot + virama + tt)
        "(cid:282)": "\u09b7\u09cd\u09a0",  # ষ্ঠ (sh-dot + virama + tth)
        "(cid:246)": "\u09b0\u09cd\u09ac",  # র্ব (r + virama + b) - in পূর্ব
        "(cid:247)": "\u09af\u09bc",  # য় (ya + nukta/yo-phala) - in বাড়ি
        "(cid:219)": "\u099e\u09cd\u099c",  # ঞ্জ (nya + virama + ja)
        "(cid:232)": "\u09a8\u09cd\u09a5",  # ন্থ (n + virama + th)
        "(cid:264)": "\u09ac\u09cd\u09b0",  # ব্র (b + virama + r) - in ব্রাহ্মণ
        "(cid:287)": "\u09a1\u09bc",  # ড় (dda with nukta) - in বাড়ি
        "(cid:288)": "\u09a2\u09bc",  # ঢ় (ddha with nukta)
        "(cid:248)": "\u09b9\u09cd\u09ae",  # হ্ম (h + virama + m) - in ব্রাহ্ম
        "(cid:289)": "\u09a6\u09cd\u09a6",  # দ্দ (d + virama + d) - in উদ্দিন
        "(cid:290)": "\u09b8\u09cd\u099f",  # স্ট (s + virama + tt) - in মাস্টার
        "(cid:291)": "\u09a6\u09cd\u09b0\u09bf",  # দ্রি (d + virama + r + i-kar) - in ইদ্রিছ
        "(cid:292)": "\u09a6\u09cd\u09a6\u09bf",  # দ্দি (d + virama + d + i-kar) - in উদ্দিন
        "(cid:293)": "\u09a8\u09cd\u09ae",  # ন্ম (n + virama + m) - duplicate for safety
        "(cid:294)": "\u09a6\u09cd\u09a6\u09bf\u09a8",  # দ্দিন (full উদ্দিন ending)
        "(cid:295)": "\u0989\u09a6\u09cd\u09a6\u09bf\u09a8",  # উদ্দিন (complete word)
    }
    
    # Debug: Log any remaining CIDs for troubleshooting
    import re
    remaining_cids = re.findall(r'\(cid:\d+\)', text)
    if remaining_cids:
        unique_cids = set(remaining_cids)
        print(f"[DEBUG] Found unmapped CID codes: {unique_cids}")
    
    for cid, char in cid_map.items():
        text = text.replace(cid, char)
    
    # Fallback: Remove any remaining unknown CID codes to prevent display issues
    # This regex will match any (cid:XXX) pattern
    text = re.sub(r'\(cid:\d+\)', '', text)
        
    return text

def reorder_bengali_vowels(text: str) -> str:
    """
    Fixes visual ordering issues where pre-base vowels (e-kar, i-kar etc.) 
    appear BEFORE the consonant in the text stream, but should be AFTER in Unicode.
    
    Target Vowels: 
    - ে (e-kar) \u09c7
    - ৈ (oi-kar) \u09c8
    - ি (i-kar) \u09bf
    
    Pattern: [VOWEL][CONSONANT] -> [CONSONANT][VOWEL]
    """
    
    # Define range for Bengali Consonants: \u0995-\u09b9 (approx, covering k-h)
    # Plus য়, ড়, ঢ়, ৎ (\u09af-\u09ce)
    # Includes Khanda-ta, Anusvara etc? Usually Pre-base vowels attach to base consonants.
    
    consonant_pattern = r'[\u0995-\u09b9\u09af-\u09ce]'
    
    # Pre-base vowels
    pre_vowels = r'[\u09c7\u09c8\u09bf]' 
    
    # CASE 1: Simple Vowel + Consonant -> Consonant + Vowel
    # e.g. ি + ক -> ক + ি
    # Use capturing groups to swap
    # Regex: (pre_vowel)(consonant)
    
    # Note: We loop because multiple swaps might be needed and regex overlaps can be tricky,
    # but a single pass substitution usually works for distinct pairs.
    
    pattern = f"({pre_vowels})({consonant_pattern})"
    
    # We replace group 1 (vowel) group 2 (consonant) with group 2 group 1
    return re.sub(pattern, r'\2\1', text)

def normalize_bengali_text(text: str) -> str:
    """
    Standardizes Bengali text by fixing common PDF extraction issues.
    """
    if not text:
        return ""
    
    # 0. Fix broken conjuncts BEFORE other processing
    from .conjunct_fixer import fix_broken_conjuncts
    text = fix_broken_conjuncts(text, field_type="aggressive")
        
    # 1. Replace CIDs
    text = replace_cids(text)
    
    # 1.5 Fix specific OCR word corruptions (Dictionary-based)
    from .ocr_corrector import fix_ocr_corruptions
    text = fix_ocr_corruptions(text)
    
    # 2. Fix Broken Vowel Ordering (Visual -> Logical)
    text = reorder_bengali_vowels(text)
    
    # 3. Fix 'o-kar' composition
    # Often 'e-kar' + 'a-kar' -> 'o-kar'
    # logical order: Consonant + e-kar + a-kar ? No.
    # Standard Unicode: Consonant + o-kar (\u09cb).
    # If we have Consonant + e-kar + a-kar, we should merge.
    # AFTER reordering, we might have: ক + ে + া 
    # This should become ক + ো
    # \u09c7 (e-kar) + \u09be (a-kar) -> \u09cb (o-kar)
    text = text.replace('\u09c7\u09be', '\u09cb')

    return text.strip()

def convert_bengali_to_english_numerals(text: str) -> str:
    """
    Converts Bengali numerals (০-৯) to English numerals (0-9).
    """
    if not text:
        return text
    
    bengali_to_english = {
        '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
        '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
    }
    
    result = text
    for bengali, english in bengali_to_english.items():
        result = result.replace(bengali, english)
    
    return result
