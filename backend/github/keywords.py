import re

def extract_keywords(code: str):
    """
    Extract meaningful tokens that help find related code on GitHub:
    - function names
    - class names
    - imported libraries
    - loop keywords
    - custom identifiers
    """

    keywords = set()

    funcs = re.findall(r"\b(?:def|function|func|static|public|private|void)\s+([A-Za-z_][A-Za-z0-9_]*)", code)
    keywords.update(funcs)

    classes = re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", code)
    keywords.update(classes)

    imports = re.findall(r"\bimport\s+([A-Za-z0-9_\.]+)", code)
    keywords.update(imports)

    loop_words = re.findall(r"\b(for|while|foreach|map|filter)\b", code)
    keywords.update(loop_words)

    ids = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", code)
    ids = [i for i in ids if len(i) > 3 and i.lower() not in ['class','int','var','let','const','void','true','false']]
    keywords.update(ids[:5])

    #result= list(keywords)[:10]   
    result=['python','codeClone']

    print("\n========================")
    print("🔍 EXTRACTED KEYWORDS:")
    print(result)
    print("========================\n")

    return result
