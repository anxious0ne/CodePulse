# CHANGELOG

All notable changes to the Competitive Programming Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- **Public Front / Landing Page (`/`)** — Comprehensive discovery landing page (`templates/home.html`) featuring:
  - Technical editorial hero section with Work Sans typography and peach accent ribbons
  - Live Codeforces telemetry radar badge with operational status indicator and rating range tags
  - Platform benchmark strip (20+ contests, 9 tiers, 22 topics, <1s sync)
  - 4 core feature quadrant cards (Rating Trajectory, Weak Topic Discovery, Verdict Distribution, Difficulty Progression)
  - Contextual authentication CTAs (Sign In / Register for guests, Dashboard shortcut for authenticated users)
- **Personalized Welcome & Onboarding State Machine**:
  - `is_new_user` session flag tracking across `register_view` and `login_view`
  - New User Onboarding Banner in Mint Green (`#90EE90`) with handle setup guidance and direct CTA
  - Returning User Greeting Banner in Sky Blue (`#7BD4FF`) with motivational welcome back message
  - Fallback heuristic detecting newly joined accounts (< 2h) with 0 submissions
- **Coders' Compass Neo-Brutalist Design System**:
  - Work Sans Google Font typography integration
  - Semantic color palette (Warm Peach `#F8D7B0`, Warm Amber `#EFBF80`, Sky Blue `#7BD4FF`, Mint Green `#90EE90`, Pink `#FFB4C8`)
  - Blueprint coordinate graph grid background (`32px` interval)
  - Tactile neo-brutalist buttons, badge pills, and solid offset drop-shadows
- **Persistent Header Navigation (`templates/base.html`)**:
  - Brand identity linked to Home (`/`)
  - Dynamic navigation links (`Home`, `Dashboard` when authenticated)
  - Profile initial avatar badge and logout controls
- **Pre-Seeded Demo Account**:
  - Username: `demo_coder`, Password: `coderscompass123` with 20 contests, 56 problems, 120 submissions pre-populated for instant testing
- `profiles` app — User profile model with bio, location, GitHub username, website
- `profiles` app — Auto-create profile on user registration (Django signal)
- `profiles` app — GET/PUT /api/profile/ endpoint
- `goals` app — Goal model with type, target/current values, progress percentage
- `goals` app — Full CRUD API: GET/POST /api/goals/, GET/PUT/DELETE /api/goals/<id>/
- `interview` app — InterviewQuestion and UserQuestionProgress models
- `interview` app — Question list with category and difficulty filtering
- `interview` app — User progress tracking (completed, bookmarked, notes)
- `codeforces` app — Clean API layer for Codeforces connect, sync, and status endpoints
- `problem_tracker` app — ProblemListView and ProblemDetailView implemented
- `problem_tracker` app — ProblemSerializer created
- `problem_tracker` app — URL routes added (/api/problems/)
- Test suite expanded to 61 tests across all apps
- Database Design document
- Sprint Planning document
- API Specification document
- Deployment Guide document
- CHANGELOG document

### Fixed
- `users/models.py` — Removed duplicate `from django.db import models` import
- `.gitignore` — Fixed merged typo `db.sqlite3.venv/` to two separate lines

---

## [0.2.0] — 2026-10-14

### Added
- Complete authentication system — register, login, logout views and templates
- Codeforces API integration with SHA-512 HMAC signed requests (apiKey + apiSecret)
- Full dashboard UI with dark Tailwind CSS theme
- Dashboard KPI cards — current rating, max rating, problems solved, contests
- Rating progression chart (Chart.js line chart)
- Verdict distribution chart (Chart.js doughnut chart)
- Difficulty breakdown chart (Chart.js bar chart)
- Topic performance table (weak topics)
- Recent submissions feed on dashboard
- Analytics REST API endpoints:
  - GET /api/analytics/topics/
  - GET /api/analytics/verdicts/
  - GET /api/analytics/ratings/
- Async sync button on dashboard with spinner feedback
- Verdict filter dropdown on submissions
- Custom Django admin panels for all models (list_display, search, filters)
- Test suite — 12 tests across users, contests, submissions, analytics
- `requirements.txt` — reproducible dependency file
- `.env.example` — safe configuration template for new developers
- `CODEFORCES_API_KEY` and `CODEFORCES_API_SECRET` in settings and .env
- README completely rewritten with badges, features, architecture, and API reference

### Fixed
- Removed entire unused `contest/` skeleton directory
- Removed entire unused `problems/` skeleton directory
- Removed duplicate `users/model.py` (misplaced duplicate)
- Removed `submissions/model.py` (duplicate file)
- Removed `submissions/model,py.txt` (typo artifact)

### Security
- `SECRET_KEY` now loaded from `.env` via python-decouple
- `DEBUG` now loaded from `.env`
- `ALLOWED_HOSTS` now loaded from `.env`
- Codeforces API credentials stored in `.env` (not hardcoded)
- `.env` excluded from version control via `.gitignore`

---

## [0.1.0] — Initial Commit

### Added
- Django project initialized with `config/` as the root configuration module
- Custom `User` model extending `AbstractUser` with `codeforces_handle` and `is_handle_verified` fields
- Initial app structure created:
  - `accounts` — authentication
  - `users` — user data and Codeforces service layer
  - `contests` — contest records
  - `problem_tracker` — problem definitions
  - `submissions` — submission records
  - `analytics` — performance analytics calculations
- Basic dashboard route and HTML template
- Initial database models and migrations for all apps
- Django REST Framework configured
- MySQL/SQLite switchable database configuration
- Git repository initialized and pushed to GitHub
