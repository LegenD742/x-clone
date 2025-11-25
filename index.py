from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from backend.detector.type1 import type1_similarity
from backend.detector.type2 import type2_similarity
from backend.detector.type3_ast import type3_ast_similarity

from backend.github.keywords import extract_keywords
from backend.search.ddg_lite import duckduckgo_search

import requests

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json()
    codeA = data.get("codeA", "")
    codeB = data.get("codeB", "")

    if not codeA.strip() or not codeB.strip():
        return jsonify({"error": "Both code snippets required"}), 400

    t1 = type1_similarity(codeA, codeB)
    t2 = type2_similarity(codeA, codeB)
    t3 = type3_ast_similarity(codeA, codeB)

    return jsonify({
        "t1": round(t1 * 100, 2),
        "t2": round(t2 * 100, 2),
        "t3base": round(t3 * 100, 2)
    })


@app.route("/api/github/search", methods=["POST"])
def github_search():
    data = request.get_json()
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"error": "Code required"}), 400

    keywords = extract_keywords(code)
    if not keywords:
        return jsonify({"error": "No keywords extracted"}), 400

    query = "site:github.com " + " ".join(keywords)

    links = duckduckgo_search(query, max_results=10)
    results = []

    for link in links:
        try:
            raw_url = link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            raw_code = requests.get(raw_url, timeout=4).text
        except:
            continue

        results.append({
            "url": link,
            "t1": round(type1_similarity(code, raw_code) * 100, 2),
            "t2": round(type2_similarity(code, raw_code) * 100, 2),
            "t3base": round(type3_ast_similarity(code, raw_code) * 100, 2)
        })

    return jsonify({
        "keywords": keywords,
        "results": results
    })


# Needed for gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
