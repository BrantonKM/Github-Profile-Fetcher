# app.py
from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response
import requests
import csv
import io
import psycopg2
from datetime import datetime
import logging
import os
import csv
from io import StringIO
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")  # For session security

# Database config
DB_HOST = os.environ.get("POSTGRES_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB", "githubdb")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "Kalekye1222")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def log_search_to_db(username):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id SERIAL PRIMARY KEY,
                username TEXT,
                searched_at TIMESTAMP
            );
        """)
        cur.execute(
            "INSERT INTO searches (username, searched_at) VALUES (%s, %s);",
            (username, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        logging.debug(f"Inserted search for {username}")
    except Exception as e:
        logging.error("Database error: %s", e)


@app.route("/", methods=["GET", "POST"])
def index():
    user_data = None
    repos = []
    if request.method == "POST":
        username = request.form["username"]
        user_res = requests.get(f"https://api.github.com/users/{username}")
        repos_res = requests.get(f"https://api.github.com/users/{username}/repos?sort=stars&per_page=5")

        if user_res.status_code == 200:
            user_data = user_res.json()
        if repos_res.status_code == 200:
            repos = repos_res.json()

        log_search_to_db(username)

    return render_template("index.html", user=user_data, repos=repos)


# ----------------------------
# 🔐 Login Routes
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "Kalekye1222":
            session["admin"] = True
            return redirect("/reports")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# ----------------------------
# 📊 Reports Panel (Admin)
# ----------------------------
@app.route("/reports")
def reports():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT username, searched_at FROM searches ORDER BY searched_at DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # If download is requested
        if request.args.get("download") == "1":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Username", "Searched At"])
            writer.writerows(rows)
            output.seek(0)
            response = make_response(output.read())
            response.headers["Content-Disposition"] = "attachment; filename=searches.csv"
            response.headers["Content-type"] = "text/csv"
            return response

        return render_template("reports.html", rows=rows)

    except Exception as e:
        logging.error("Error fetching reports: %s", e)
        return "An error occurred", 500
# ----------------------------
# 📥 Export to CSV
# ----------------------------
@app.route("/download")
def download_csv():
    if not session.get("admin"):
        return redirect("/login")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, searched_at FROM searches ORDER BY searched_at DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Create CSV in memory
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "Username", "Searched At"])
        writer.writerows(rows)
        csv_file.seek(0)

        return send_file(
            csv_file,
            mimetype="text/csv",
            as_attachment=True,
            download_name="searches_report.csv"
        )
    except Exception as e:
        logging.error("CSV export error: %s", e)
        return "Error downloading CSV"
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

    
