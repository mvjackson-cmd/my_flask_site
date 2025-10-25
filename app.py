from flask import Flask, render_template, request, redirect, url_for
import csv, os, datetime

app = Flask(__name__)

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "messages.csv")

def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "name", "message"])  # header

def read_recent(limit=5):
    if not os.path.exists(CSV_PATH):
        return []
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "timestamp": r["timestamp"],
                "name": r["name"],
                "message": r["message"],
            })
    return list(reversed(rows))[:limit]  # newest first

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    ensure_storage()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        message = (request.form.get("message") or "").strip()
        if name and message:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([ts, name, message])
            return redirect(url_for("contact", ok="1"))
        else:
            return render_template("contact.html", flash="Please fill in both fields.", recent=read_recent())

    # GET
    flash_msg = "Thanks! Your message was saved." if request.args.get("ok") == "1" else None
    return render_template("contact.html", flash=flash_msg, recent=read_recent())

if __name__ == "__main__":
    # Local testing only
    app.run(debug=True)

