Deployment Guide
Competitive Programming Tracker

Document Version: 1.0
Status: Initial Draft

---

1. Purpose

This document describes how to set up and run the Competitive Programming Tracker
for local development and production deployment.

---

2. Prerequisites

Tool              Minimum Version
----              ---------------
Python            3.10+
pip               latest
Git               any recent version
MySQL             8.0+ (for production)
Virtual Env       via python -m venv or venv module

---

3. Local Development Setup

---

3.1 Clone the Repository

  git clone https://github.com/anxious0ne/CodePulse.git
  cd CodePulse

---

3.2 Create a Virtual Environment

  python -m venv .venv

Activate on Windows (PowerShell):

  .\.venv\Scripts\Activate.ps1

If PowerShell blocks scripts:

  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

---

3.3 Install Dependencies

  pip install -r requirements.txt

---

3.4 Create the .env File

Copy the example file:

  copy .env.example .env

Then edit .env with your values. See Section 4 for all variables.

---

3.5 Configure the Database

For local development (SQLite — default):

  No additional configuration is needed.
  DB_ENGINE=sqlite in your .env

For MySQL (optional for local):

  Create a MySQL database:
  CREATE DATABASE codepulse CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

  Set in .env:
  DB_ENGINE=mysql
  DB_NAME=codepulse
  DB_USER=root
  DB_PASSWORD=yourpassword
  DB_HOST=127.0.0.1
  DB_PORT=3306

---

3.6 Run Migrations

  python manage.py migrate

---

3.7 Create a Superuser (Admin)

  python manage.py createsuperuser

Follow the prompts to set username, email, and password.

---

3.8 Run the Development Server

  python manage.py runserver

Open your browser at: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

---

4. Environment Variables Reference

All sensitive configuration is stored in the .env file.
Never commit .env to version control.

Variable                    Purpose                                 Example Value
--------                    -------                                 -------------
SECRET_KEY                  Django secret key                       a-long-random-string
DEBUG                       Enable/disable debug mode               True (local), False (prod)
ALLOWED_HOSTS               Comma-separated allowed hosts           127.0.0.1,localhost
DB_ENGINE                   Database engine (sqlite or mysql)       sqlite
DB_NAME                     MySQL database name                     codepulse
DB_USER                     MySQL username                          root
DB_PASSWORD                 MySQL password                          yourpassword
DB_HOST                     MySQL host                              127.0.0.1
DB_PORT                     MySQL port                              3306
CODEFORCES_API_KEY          Codeforces API key                      your-api-key
CODEFORCES_API_SECRET       Codeforces API secret                   your-api-secret

---

5. Running Tests

Run the full test suite:

  python manage.py test --verbosity=2

Run tests for a specific app:

  python manage.py test accounts
  python manage.py test goals
  python manage.py test interview

---

6. Syncing Codeforces Data (Development)

To manually sync a user's Codeforces data via management command:

  python manage.py sync_codeforces <django_username> --handle <codeforces_handle>

Example:

  python manage.py sync_codeforces admin --handle tourist

---

7. Production Deployment

---

7.1 Set Environment Variables for Production

In your .env on the production server:

  DEBUG=False
  SECRET_KEY=<a-strong-random-key-at-least-50-characters>
  ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  DB_ENGINE=mysql
  DB_NAME=codepulse_prod
  DB_USER=codepulse_db_user
  DB_PASSWORD=<strong-db-password>
  DB_HOST=127.0.0.1
  DB_PORT=3306

---

7.2 Configure MySQL for Production

Log in to MySQL:

  mysql -u root -p

Create database and user:

  CREATE DATABASE codepulse_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  CREATE USER 'codepulse_db_user'@'localhost' IDENTIFIED BY 'strong-password';
  GRANT ALL PRIVILEGES ON codepulse_prod.* TO 'codepulse_db_user'@'localhost';
  FLUSH PRIVILEGES;

---

7.3 Collect Static Files

  python manage.py collectstatic --noinput

---

7.4 Run Migrations

  python manage.py migrate

---

7.5 Gunicorn (WSGI Server)

Install gunicorn:

  pip install gunicorn

Run:

  gunicorn config.wsgi:application --bind 0.0.0.0:8000

For production, run as a systemd service.

---

7.6 Nginx Configuration (Example)

server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/CodePulse/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

---

7.7 HTTPS

Use Certbot with Let's Encrypt to obtain a free SSL certificate:

  sudo certbot --nginx -d yourdomain.com

---

8. Production Security Checklist

Run Django's built-in deployment check:

  python manage.py check --deploy

Required before going live:

[ ] DEBUG=False in .env
[ ] SECRET_KEY is a strong, unique value (not the default)
[ ] ALLOWED_HOSTS is set to your domain (not *)
[ ] .env is NOT committed to Git
[ ] db.sqlite3 is NOT committed to Git
[ ] HTTPS is enabled in production
[ ] Database uses a dedicated user (not root)
[ ] Static files are served by Nginx (not Django)
[ ] Superuser password is strong and unique

---

9. Database Backup

To back up the production MySQL database:

  mysqldump -u codepulse_db_user -p codepulse_prod > backup_$(date +%Y%m%d).sql

To restore:

  mysql -u codepulse_db_user -p codepulse_prod < backup_20261014.sql

---

10. Common Issues and Solutions

Issue                                   Solution
-----                                   --------
ModuleNotFoundError: decouple           pip install python-decouple
Scripts cannot be loaded (PowerShell)   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
ALLOWED_HOSTS error in prod             Add your domain to ALLOWED_HOSTS in .env
Static files not found in prod          Run collectstatic and configure Nginx static path
Database connection refused             Check DB_HOST, DB_PORT, and MySQL is running
Codeforces sync returns 400             Verify API key and secret in .env are correct

---

Deployment Guide Version: 1.0
Status: Initial Draft
