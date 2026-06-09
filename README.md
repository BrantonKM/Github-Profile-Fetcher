#  GitHub Profile Fetcher (Flask + Docker + PostgreSQL)

A sleek Flask web app that allows users to fetch real-time GitHub profile data and top repositories by simply entering a GitHub username. The app logs each search in a PostgreSQL database and runs inside Docker for easy deployment.

---

##  Features

-  Search GitHub users by username
-  Displays user profile, avatar, and top repositories
-  Logs all searches to a PostgreSQL database
-  Dockerized for full-stack container deployment
-  Responsive frontend using HTML/CSS/JS

---

##  Demo Screenshot

![screenshot](static/screenshot.png)

---

##  Tech Stack

| Layer       | Tech               |
|-------------|--------------------|
| Backend     | Flask (Python)     |
| Frontend    | HTML, CSS, JavaScript |
| Database    | PostgreSQL         |
| Container   | Docker & Docker Compose |
| API Used    | GitHub REST API v3 |

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/github-profile-fetcher.git
cd github-profile-fetcher
