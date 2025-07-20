from flask import Flask, render_template, request, redirect
import psycopg2
import os
import random

app = Flask(__name__)

# 🔐 Try to connect to the PostgreSQL database using DATABASE_URL
conn = None
cursor = None

if "DATABASE_URL" in os.environ:
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS quotes (id SERIAL PRIMARY KEY, quote TEXT);")
        conn.commit()
        print("✅ Connected to Railway database.")
    except Exception as e:
        print("❌ Failed to connect to database:", e)
else:
    print("⚠️ DATABASE_URL not found. Running in local test mode (no DB).")

@app.route("/", methods=["GET", "POST"])
def index():
    if not conn:
        return "⚠️ No database connection. Try this app on Railway."

    if request.method == "POST":
        new_quote = request.form["quote"]
        cursor.execute("INSERT INTO quotes (quote) VALUES (%s);", (new_quote,))
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT quote FROM quotes;")
    all_quotes = [row[0] for row in cursor.fetchall()]
    quote = random.choice(all_quotes) if all_quotes else "No quotes yet!"
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    app.run(debug=True)
