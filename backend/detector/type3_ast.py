import re
import math
from collections import Counter


KEYWORDS = [
    "if", "else", "elif", "for", "while", "switch", "case",
    "try", "catch", "except", "def", "class", "function",
    "return", "break", "continue"
]

OPERATORS = [
    "+", "-", "*", "/", "%", "&&", "||", "and", "or",
    "==", "!=", "<", ">", "<=", ">=", "=", "+=", "-="
]


def _clean(code: str):
    """Remove comments + normalize whitespace."""
    code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)
    code = re.sub(r"#.*?$", "", code, flags=re.MULTILINE)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    return code


def _extract_features(code: str) -> Counter:
    """
    Produce a richer, more reliable structural signature:
    - keyword frequencies
    - operator frequencies
    - nesting depth
    - number of blocks
    - cyclomatic complexity (rough)
    - loop count
    - conditional count
    - function calls
    """
    feats = Counter()
    code = _clean(code)

    lines = [ln for ln in code.splitlines() if ln.strip()]
    feats["lines"] = len(lines)

    lower = code.lower()

    for kw in KEYWORDS:
        feats[f"kw_{kw}"] = len(re.findall(rf"\b{kw}\b", lower))

    for op in OPERATORS:
        feats[f"op_{op}"] = lower.count(op)

    feats["func_calls"] = len(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\s*\(", code))

    feats["loops"] = len(re.findall(r"\bfor\b|\bwhile\b", lower))

    feats["conditionals"] = len(re.findall(r"\bif\b|\bswitch\b", lower))

    branch_tokens = re.findall(r"\bif\b|\bfor\b|\bwhile\b|\bcase\b|\bcatch\b|\|\||&&", lower)
    feats["cyclomatic"] = 1 + len(branch_tokens)  

    indent_depth = 0
    max_depth = 0
    for line in lines:
        depth = len(re.match(r"^\s*", line).group())
        if depth > max_depth:
            max_depth = depth
    feats["nesting"] = max_depth

    return feats


def _cosine(a: Counter, b: Counter):
    """Vector cosine similarity."""
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(a[k] ** 2 for k in keys))
    nb = math.sqrt(sum(b[k] ** 2 for k in keys))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


def _length_penalty(a_lines: int, b_lines: int):
    """Penalize large length differences."""
    if a_lines == 0 or b_lines == 0:
        return 0
    ratio = min(a_lines, b_lines) / max(a_lines, b_lines)
    return ratio ** 0.5   # 0.3–1.0


def type3_ast_similarity(codeA: str, codeB: str) -> float:
    """
    Improved Type-3 structural similarity:
    - weighted structural vectors
    - nesting + complexity
    - strong penalties for unrelated structures
    """
    if not codeA.strip() or not codeB.strip():
        return 0.0

    featsA = _extract_features(codeA)
    featsB = _extract_features(codeB)

    base = _cosine(featsA, featsB)

    lp = _length_penalty(featsA["lines"], featsB["lines"])
    base *= lp

    diff = abs(featsA["cyclomatic"] - featsB["cyclomatic"])
    comp_penalty = 1 / (1 + diff)
    base *= comp_penalty

    return max(0.0, min(base, 1.0))
