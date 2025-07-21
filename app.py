from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        profile_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"

        profile_res = requests.get(profile_url)
        repos_res = requests.get(repos_url)

        if profile_res.status_code != 200:
            return render_template("index.html", error="User not found")

        profile = profile_res.json()
        repos = repos_res.json()

        return render_template("index.html", profile=profile, repos=repos)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
