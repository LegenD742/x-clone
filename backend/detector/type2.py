import re
from collections import Counter
import math

STOPWORDS = {
    "for", "if", "else", "elif", "while", "return", "break", "continue",
    "switch", "case",
    "public", "private", "protected", "class", "def", "function", "void",
    "int", "float", "char", "double", "var", "let", "const", "static",
    "try", "catch", "except", "final"
}

def normalize_code(code):
    code = code.lower()

    code = re.sub(r'"[^"]*"', " STR ", code)
    code = re.sub(r"'[^']*'", " STR ", code)

    code = re.sub(r'\b\d+\b', " NUM ", code)

    code = re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*\b', " ID ", code)

    
    code = re.sub(r'[+\-*/%=<>!&|^~]', ' ', code)

    
    tokens = re.findall(r'\b\w+\b', code)

    
    tokens = [t for t in tokens if t not in STOPWORDS]

    return tokens


def weighted_jaccard(a, b):
    ca = Counter(a)
    cb = Counter(b)

    all_tokens = set(ca) | set(cb)

    num = 0
    den = 0

    for tok in all_tokens:
        num += min(ca[tok], cb[tok])
        den += max(ca[tok], cb[tok])

    if den == 0:
        return 0.0

    return num / den


def type2_similarity(code_a, code_b):
    tokA = normalize_code(code_a)
    tokB = normalize_code(code_b)

    if not tokA or not tokB:
        return 0.0

    return weighted_jaccard(tokA, tokB)
