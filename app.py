from flask import Flask, request, jsonify
import os

app = Flask(__name__)

API_KEY = "test123"   # use this in tester

@app.route("/honeypot", methods=["GET", "POST"])
def honeypot():
    if request.method == "GET":
        return jsonify({
            "message": "Honeypot API is running",
            "endpoint": "/honeypot",
            "method": "POST",
            "headers": {"x-api-key": "test123"},
            "body": {"message": "your message here"}
        })
    
    key = request.headers.get("x-api-key")

    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    data = request.json or {}
    message = data.get("message", "").lower()

    signals = []

    if "click" in message:
        signals.append("suspicious link")
    if "won" in message or "prize" in message:
        signals.append("reward bait")
    if "urgent" in message:
        signals.append("urgency")

    verdict = "scam" if signals else "unknown"

    return jsonify({
        "status": "success",
        "verdict": verdict,
        "confidence": 0.92 if verdict == "scam" else 0.50,
        "signals": signals,
        "extracted_intelligence": {
            "intent": "phishing attempt",
            "risk_level": "high" if verdict == "scam" else "medium"
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
