import re
import difflib

def _remove_comments(code: str) -> str:
    """
    Remove common single-line and multi-line comments
    for C/Java/JS/Python-like languages.
    """
    
    code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)

    code = re.sub(r"#.*?$", "", code, flags=re.MULTILINE)
    
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    return code


def _normalize_whitespace(code: str) -> str:
    """
    Collapse all whitespace and newlines.
    """
    
    code = code.strip()
    
    code = re.sub(r"\s+", " ", code)
    return code


def type1_similarity(code_a: str, code_b: str) -> float:
    """
    Type-1 similarity:
    - remove comments
    - normalize whitespace
    - compute similarity using SequenceMatcher (0..1)

    This is still 'exact-style' but gives a graded score.
    """
    if not code_a.strip() or not code_b.strip():
        return 0.0

    a = _normalize_whitespace(_remove_comments(code_a))
    b = _normalize_whitespace(_remove_comments(code_b))

    if not a or not b:
        return 0.0

    matcher = difflib.SequenceMatcher(None, a, b)
    return matcher.ratio()
