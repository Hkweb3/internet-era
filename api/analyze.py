from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import InternetEraEngine

app = Flask(__name__)
CORS(app)

engine = InternetEraEngine()

@app.route('/api/analyze', methods=['POST'])
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    answers = data.get('answers', [])
    if not answers or len(answers) != 8:
        return jsonify({"error": "Need exactly 8 answers"}), 400
    
    try:
        result = engine.analyze(answers)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
