from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import json
import re
from dotenv import load_dotenv
 
load_dotenv()
 
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
def ask_ai(prompt):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat.choices[0].message.content
 
# ─── Home Page ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")
 
# ─── Topic Explainer ─────────────────────────────────────────
@app.route("/explain", methods=["GET", "POST"])
def explain():
    result = None
    topic = ""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        level = request.form.get("level", "beginner")
        if topic:
            prompt = f"""Explain the topic "{topic}" for a {level}-level student.
Use simple language, give a real-life example, and keep it under 200 words.
Format with clear paragraphs."""
            result = ask_ai(prompt)
    return render_template("explain.html", result=result, topic=topic)
 
# ─── MCQ Generator ───────────────────────────────────────────
@app.route("/mcq", methods=["GET", "POST"])
def mcq():
    result = None
    topic = ""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        num = request.form.get("num", "5")
        if topic:
            prompt = f"""Generate {num} multiple choice questions on the topic: "{topic}".
Format each question like this:
Q1. [Question]
A) option
B) option
C) option
D) option
Answer: [correct option]
 
Make questions suitable for a university AI student."""
            result = ask_ai(prompt)
    return render_template("mcq.html", result=result, topic=topic)
 
# ─── Notes Summarizer ────────────────────────────────────────
@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    result = None
    notes = ""
    if request.method == "POST":
        notes = request.form.get("notes", "").strip()
        if notes:
            prompt = f"""Summarize the following notes in a clear, concise way.
Use bullet points for key concepts.
Keep it under 150 words.
 
Notes:
{notes}"""
            result = ask_ai(prompt)
    return render_template("summarizer.html", result=result, notes=notes)
 
# ─── Quiz Mode ───────────────────────────────────────────────
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")
 
@app.route("/quiz/generate", methods=["POST"])
def quiz_generate():
    data = request.get_json()
    topic = data.get("topic", "").strip()
    num = data.get("num", 5)
 
    prompt = f"""Generate exactly {num} multiple choice quiz questions on: "{topic}".
 
Return ONLY a valid JSON array. No explanation, no markdown, no extra text.
Format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]
 
"answer" is the index (0-3) of the correct option.
Make questions suitable for university-level AI students."""
 
    raw = ask_ai(prompt)
 
    # Strip markdown code fences if present
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("```").strip()
 
    try:
        questions = json.loads(clean)
        return jsonify({"success": True, "questions": questions})
    except Exception:
        return jsonify({"success": False, "error": "Could not parse questions. Try again."})
 
if __name__ == "__main__":
    app.run(debug=True)
 