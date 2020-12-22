import unicodedata
import re

def _tokenize_chinese_punctutation_chars(text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
        if _is_chinese_char(char) or _is_punctuation(char):
            output.append(" ")
            output.append(char)
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)

def _tokenize_chinese_chars(text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
        if _is_chinese_char(cp):
            output.append(" ")
            output.append(char)
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)

def _is_chinese_char(char):
    """Checks whether char is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F) or #
            (cp >= 0x3100 and cp <= 0x312F)):  #bopomofo
            
        return True

    return False

def _is_punctuation(char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
        (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


import nltk

nltk.download('punkt')

class NLTKSegmenter:
    def __init(self):
        pass

    def segment_string(self, article):
        en_segments = nltk.tokenize.sent_tokenize(article)
        final_segment = []
        for en_segment in en_segments:
            zh_segments = re.findall(r"[^。！？]+[。！？」]*", en_segment.strip())
            # print(zh_segments)
            for zh_segment in zh_segments:
                if zh_segment != "":
                    tokenized_zh_segment = _tokenize_chinese_punctutation_chars(zh_segment)
                    final_segment.append(tokenized_zh_segment)
                    # final_segment.append(zh_segment)
        return final_segment