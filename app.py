from flask import Flask, request, jsonify,render_template
from engine.regex_tier import RegexClassifier
from engine.ml_tier import StatisticalMLClassifier
from engine.llm_tier import LLMFallbackClassifier
from datetime import datetime

app = Flask (__name__)
regex_tier = RegexClassifier()
ml_tier = StatisticalMLClassifier()
llm_tier = LLMFallbackClassifier()
"""History storage"""
stats = {
    "Complaint" : 0,
    "Praise" : 0,
    "Question" : 0 ,
    "total" : 0,
}
history_log = []

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health" ,methods = ["GET"])
def health_check():
    return jsonify({"status": "healthy", "service":"Hybrid Classification Engine"}), 200

@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    return jsonify({"stats": stats, "history": history_log[-10:]}), 200
@app.route("/api/v1/classify", methods=["POST"])
def classify():
    payload = request.get_json()
    if not payload or "text" not in payload:
        return jsonify({"error": "Missing 'text' parameter in request body"}), 400
    
    text = payload["text"].strip()
    if not text:
        return jsonify({"error": "Text field can't be empty"}), 400

    # Tier 1: Regex
    result = regex_tier.classify(text)
    if not result:
        # Tier 2: Statistical ML
        result = ml_tier.classify(text)
    if not result:
        # Tier 3: LLM Fallback
        result = llm_tier.classify(text)

    category = result.get("category", "Question")
    
    # 1. Update stats dictionary safely
    if category in stats:
        stats[category] += 1
    else:
        stats[category] = 1
    stats["total"] += 1
    
    # 2. Append to history log
    log_entry = {
        "text": text,
        "category": category,
        "confidence": result.get("confidence", 1.0),
        "tier_executed": result.get("tier_executed", "Tier 3"),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    history_log.append(log_entry)

    return jsonify(result), 200
if __name__ == "__main__":
    print ("🚀 Hybrid Classification Pipeline API running on http://127.0.0.1:5000")
    app.run(debug=True, port = 5000)