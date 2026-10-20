# CodePulse ⚡
> Full-Stack Competitive Programming Analytics & Performance Tracking Platform.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1+-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.18+-red?style=flat)](https://www.django-rest-framework.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4+-FF6384?style=flat&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

---

## 📖 Overview

**CodePulse** consolidates competitive programming progress into a clean, actionable web dashboard. By integrating directly with the **Codeforces Public API**, it continuously synchronizes rating progression, contest rankings, topic solve rates, and recent submissions.

### ✨ Key Features
- **Public Front / Landing Page**: High-impact editorial landing page (`/`) introducing platform capabilities with a live Codeforces telemetry radar badge, system benchmark strip, and dynamic Call-to-Actions.
- **Personalized Onboarding & Welcome Flow**:
  - **New Users**: Celebratory Mint Green onboarding card (`🎉 Welcome to CodeTrack AI, {user}!`) with guided handle setup.
  - **Returning Users**: Sky Blue greeting banner (`👋 Welcome back, {user}!`) with immediate access to updated analytics.
  - **Context-Aware Navigation**: Header and home page dynamically reflect authentication state.
- **Coders' Compass Neo-Brutalist Design**: Full visual overhaul inspired by [Coders' Compass](https://coderscompass.org/) featuring *Work Sans* typography, warm peach navbar, coordinate grid background, and tactile drop shadows (`3px 3px 0px #0E2433`).
- **Centralized Analytics Dashboard**: Live Codeforces rating, historical peak rank, solve counts, and active contest records.
- **Dynamic Rating Trajectory**: Interactive multi-stop gradient line chart powered by Chart.js displaying rating milestones and contest deltas.
- **Weak Topic Identification**: Calculates solve rates across 22+ algorithm tags (`dp`, `greedy`, `graphs`, `math`, `trees`) and prioritizes practice areas.
- **Verdict Distribution**: 5-slice doughnut visualization showing accepted vs. failed submissions (AC, WA, TLE, MLE, CE).
- **Difficulty Rating Ladder**: Categorizes solved problems into 9 Codeforces difficulty brackets (`< 1000` to `2600+`).
- **On-Demand & Background Sync**: Sync profile submissions through the dashboard button or schedule cron jobs using custom Django management commands.
- **Built-in Authentication & Live Demo**: Secure registration and login with pre-seeded demo credentials (`demo_coder` / `coderscompass123`).

---

## 🛠️ Architecture & Tech Stack

| Layer | Technology | Responsibility |
| :--- | :--- | :--- |
| **Backend Language** | Python 3.11+ | Business logic, Codeforces data processing, analytics engine |
| **Web Framework** | Django | Request routing, ORM, authentication, security |
| **API Framework** | Django REST Framework (DRF) | Modular JSON REST APIs |
| **Database** | MySQL / SQLite | Persistent storage (supports seamless SQLite fallback for local dev) |
| **Frontend UI** | Tailwind CSS + HTML5 | Modern dark-themed dashboard components & responsive design |
| **Visualizations** | Chart.js | Interactive rating progression, verdict doughnut, difficulty bars |
| **External Integration** | Codeforces API | Profile stats, contest history, and submission logs |

---

## ⚡ Live Demo Account (Instant Testing)

For evaluators, reviewers, and local testing, CodePulse includes a pre-seeded high-activity competitive programming profile:

* **URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Username**: `demo_coder`
* **Password**: `coderscompass123`
* **Codeforces Handle**: `Errichto` (Grandmaster tier, 20 contests, 56 problems, 120 submissions pre-seeded)

Alternatively, register a new account on `/accounts/register/` to experience the **New User Onboarding** welcome flow!

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```powershell
git clone https://github.com/anxious0ne/CodePulse.git
cd CodePulse
```

### 2. Set Up Virtual Environment (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell says scripts are disabled, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
By default, `.env` is configured to use **SQLite** for instant zero-config setup. If you wish to use **MySQL**, update `.env`:
```ini
DB_ENGINE=mysql
DB_NAME=codepulse_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Run Database Migrations
```powershell
python manage.py migrate
```

### 6. Start the Development Server
```powershell
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 💻 Codeforces Data Synchronization

### Option A: From Web Interface
1. Register and sign in to your CodePulse account.
2. Enter your Codeforces handle (e.g., `tourist`, `Benq`) in the top banner.
3. Click **Sync Now**. All contests, problems, and submission history will be fetched and visualized in real time.

### Option B: From Command Line
Run the custom Django management command:
```powershell
python manage.py sync_codeforces <username> [--handle <codeforces_handle>]
```
Example:
```powershell
python manage.py sync_codeforces john_coder --handle tourist
```

---

## 📡 REST API Endpoints

All API endpoints are protected and require session authentication:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/dashboard/` | `GET` | User summary metrics (rating, max rating, solve rate, rank badge) |
| `/api/contests/` | `GET` | Filtered contest rating history with rating deltas |
| `/api/analytics/topics/` | `GET` | Tag-wise attempt vs. solved stats and accuracy rates |
| `/api/analytics/verdicts/` | `GET` | Aggregated breakdown of submission verdicts |
| `/api/analytics/ratings/` | `GET` | Solved problem distribution across rating brackets |
| `/api/submissions/recent/` | `GET` | Latest submissions with problem details and verdict filter |
| `/api/codeforces/sync/` | `POST` | Triggers Codeforces API synchronization |
| `/api/codeforces/handle/` | `POST` | Updates active Codeforces handle |

---

## 🧪 Running Automated Tests

Run the full Django test suite (models, views, services, analytics):
```powershell
python manage.py test
```

---

## 📂 Project Structure

```text
CodePulse/
├── config/                  # Master project settings & root URLs
├── accounts/                # Registration, login, logout views & templates
├── users/                   # Custom User model, Codeforces sync engine & CLI command
├── contests/                # Contest history tracking & REST endpoints
├── problem_tracker/         # Problem catalog with ratings & tags
├── submissions/             # Submission logger with verdicts & language tracking
├── analytics/               # Aggregation service for weak areas & distributions
├── templates/               # HTML templates (dashboard, accounts)
├── static/                  # Client-side JavaScript (Chart.js dashboard script)
├── requirements.txt         # Project dependencies
└── manage.py                # Django CLI management entrypoint
```
