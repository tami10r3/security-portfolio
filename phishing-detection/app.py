from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
import joblib
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from utils.feature_extractor import extract_features
from utils.risk_engine import hybrid_risk_score

app = Flask(__name__)
app.secret_key = "supersecretkey"

model = joblib.load("model/phishing_model.pkl")

history = []


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/risk", methods=["POST"])
def risk():

    url = request.form.get("url")

    result = hybrid_risk_score(url, model)

    result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history.append(result)

    return jsonify(result)

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)

            return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- ADMIN ----------------

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")

@app.route("/history")
def get_history():
    return jsonify(history[-50:])

@app.route("/analytics")
def analytics():

    phishing_count = sum(1 for h in history if h["final_label"] == "PHISHING")
    safe_count = sum(1 for h in history if h["final_label"] == "SAFE")

    avg_risk = (
        sum(h["risk_score"] for h in history) / len(history)
        if history else 0
    )

    return jsonify({
        "total_requests": len(history),
        "phishing_detected": phishing_count,
        "safe_detected": safe_count,
        "average_risk_score": round(avg_risk, 2)
    })

# ---------------- CSV EXPORT ----------------

@app.route("/export/csv")
@login_required
def export_csv():

    df = pd.DataFrame(history)

    filepath = "exports/history.csv"

    df.to_csv(filepath, index=False)

    return send_file(filepath, as_attachment=True)

# ---------------- PDF EXPORT ----------------

@app.route("/export/pdf")
@login_required
def export_pdf():

    filepath = "exports/report.pdf"

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Phishing Detection Report", styles['Title']))
    elements.append(Spacer(1, 12))

    for item in history[-20:]:

        text = f"""
        URL: {item['url']}<br/>
        Status: {item['final_label']}<br/>
        Risk Score: {item['risk_score']}<br/>
        Time: {item['timestamp']}<br/><br/>
        """

        elements.append(Paragraph(text, styles['BodyText']))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    return send_file(filepath, as_attachment=True)

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)