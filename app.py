from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ─── SAFE API KEY LOADING ─────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise Exception("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

# ─── AI FUNCTION (SAFE) ───────────────────────────────
def ask_ai_raw(prompt):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat.choices[0].message.content
def ask_ai(prompt):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    text = chat.choices[0].message.content

    # Convert markdown bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Convert new lines ONCE only
    text = text.replace("\n", "<br>")

    return text

# ─── HOME ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─── EXPLAIN ──────────────────────────────────────────
@app.route("/explain", methods=["GET", "POST"])
def explain():
    result = None
    topic = ""

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        level = request.form.get("level", "beginner")

        if topic:
            prompt = f"""
Explain "{topic}" for a {level}-level student.
Use simple language, real-life example, and keep under 200 words.
Format clearly in paragraphs.
"""
            result = ask_ai(prompt)

    return render_template("explain.html", result=result, topic=topic)


# ─── MCQ ──────────────────────────────────────────────
@app.route("/mcq", methods=["GET", "POST"])
def mcq():
    result = None
    topic = ""

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        num = request.form.get("num", "5")

        if topic:
            prompt = f"""
Generate {num} MCQs on "{topic}".

Format:
Q1. Question
A) option
B) option
C) option
D) option
Answer: correct option

Make it university level.
"""
            result = ask_ai(prompt)

    return render_template("mcq.html", result=result, topic=topic)


# ─── SUMMARIZER ───────────────────────────────────────
@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    result = None
    notes = ""

    if request.method == "POST":
        notes = request.form.get("notes", "").strip()

        if notes:
            prompt = f"""
Summarize these notes in bullet points.
Keep under 150 words.

Notes:
{notes}
"""
            result = ask_ai(prompt)

    return render_template("summarizer.html", result=result, notes=notes)


# ─── QUIZ PAGE ────────────────────────────────────────
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/quiz/generate", methods=["POST"])
def quiz_generate():
    data = request.get_json()
    topic = data.get("topic", "").strip()
    num = int(data.get("num", 5))

    prompt = f"""
Generate exactly {num} MCQs on "{topic}".

Return ONLY valid JSON array:

[
  {{
    "question": "Question?",
    "options": ["A", "B", "C", "D"],
    "answer": 0
  }}
]

No extra text.
"""

    raw = ask_ai_raw(prompt)   # <-- use raw version

    try:
        # Improved JSON extraction (handles markdown code blocks)
        match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw, re.DOTALL)
        if match:
            clean = match.group(1)
        else:
            clean = re.search(r"\[.*\]", raw, re.DOTALL).group(0)

        questions = json.loads(clean)
        return jsonify({"success": True, "questions": questions})
    except Exception as e:
        print("JSON parse error:", e)   # helpful for debugging
        return jsonify({
            "success": False,
            "error": "Failed to parse AI response into JSON"
        })

# ─── RUN APP ──────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
    