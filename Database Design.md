Database Design
Competitive Programming Tracker

Document Version: 1.0
Status: Initial Draft
Lifecycle Stage: Database Design
Previous Stage: Architecture
Next Stage: Sprint Planning

---

1. Purpose

This document defines the database design for the Competitive Programming Tracker.

It covers:

- Entity identification
- Table definitions with column names, data types, and constraints
- Primary keys and foreign keys
- Relationships between tables
- Indexing strategy
- Normalization notes

The database selected for this project is MySQL.

Django ORM will provide the application-level interface to the database.

---

2. Lifecycle Position

Architecture
    ↓
Database Design    ← This Document
    ↓
Sprint Planning

---

3. Database Technology

Database: MySQL
ORM: Django ORM
Development (local): SQLite (via django.db.backends.sqlite3)
Production: MySQL (via django.db.backends.mysql using PyMySQL)

---

4. Entity Identification

The following major entities have been identified:

Entity                  Description
-------                 -----------
User                    Application user account (authentication)
Profile                 Extended user profile information
Contest                 Codeforces contest entry for a user
Problem                 Codeforces problem definition
Submission              A user's submission to a problem
Goal                    A personal coding goal set by the user
InterviewQuestion       An interview preparation question
UserQuestionProgress    A user's progress on an interview question

---

5. Table Definitions

---

5.1 Table: users_user

This is the custom Django user model extending AbstractUser.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
username                VARCHAR(150)            NOT NULL, UNIQUE
email                   VARCHAR(254)            NOT NULL
password                VARCHAR(128)            NOT NULL  (hashed)
first_name              VARCHAR(150)            NOT NULL, DEFAULT ''
last_name               VARCHAR(150)            NOT NULL, DEFAULT ''
is_staff                TINYINT(1)              NOT NULL, DEFAULT 0
is_active               TINYINT(1)              NOT NULL, DEFAULT 1
is_superuser            TINYINT(1)              NOT NULL, DEFAULT 0
date_joined             DATETIME(6)             NOT NULL
last_login              DATETIME(6)             NULL
codeforces_handle       VARCHAR(50)             NULL, UNIQUE
is_handle_verified      TINYINT(1)              NOT NULL, DEFAULT 0

Indexes:
- PRIMARY KEY (id)
- UNIQUE (username)
- UNIQUE (codeforces_handle)

---

5.2 Table: profiles_profile

Stores extended profile information for each user.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
user_id                 INT                     NOT NULL, UNIQUE, FK → users_user(id)
bio                     LONGTEXT                NOT NULL, DEFAULT ''
location                VARCHAR(100)            NOT NULL, DEFAULT ''
github_username         VARCHAR(100)            NOT NULL, DEFAULT ''
website                 VARCHAR(200)            NOT NULL, DEFAULT ''
created_at              DATETIME(6)             NOT NULL (auto)
updated_at              DATETIME(6)             NOT NULL (auto)

Indexes:
- PRIMARY KEY (id)
- UNIQUE (user_id)
- INDEX (user_id)

---

5.3 Table: contests_contest

Stores contest participation records retrieved from Codeforces.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
user_id                 INT                     NOT NULL, FK → users_user(id)
contest_id              INT                     NOT NULL
contest_name            VARCHAR(255)            NOT NULL
rank                    INT                     NULL
old_rating              INT                     NULL
new_rating              INT                     NULL
rating_change           INT                     NULL  (computed as new_rating - old_rating)
contest_time            DATETIME(6)             NULL

Indexes:
- PRIMARY KEY (id)
- INDEX (user_id)
- UNIQUE (user_id, contest_id)

---

5.4 Table: problem_tracker_problem

Stores Codeforces problem definitions (shared, not per-user).

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
contest_id              INT                     NOT NULL
problem_index           VARCHAR(10)             NOT NULL
name                    VARCHAR(255)            NOT NULL
rating                  INT                     NULL
tags                    JSON                    NOT NULL, DEFAULT '[]'

Indexes:
- PRIMARY KEY (id)
- UNIQUE (contest_id, problem_index)
- INDEX (rating)

---

5.5 Table: submissions_submission

Stores submission records for users.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
user_id                 INT                     NOT NULL, FK → users_user(id)
submission_id           BIGINT                  NOT NULL
problem_id              INT                     NULL, FK → problem_tracker_problem(id)
verdict                 VARCHAR(50)             NOT NULL
language                VARCHAR(50)             NOT NULL, DEFAULT ''
time_seconds            BIGINT                  NULL
submitted_at            DATETIME(6)             NULL

Indexes:
- PRIMARY KEY (id)
- INDEX (user_id)
- INDEX (verdict)
- UNIQUE (user_id, submission_id)

---

5.6 Table: goals_goal

Stores personal coding goals for users.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
user_id                 INT                     NOT NULL, FK → users_user(id)
title                   VARCHAR(200)            NOT NULL
description             LONGTEXT                NOT NULL, DEFAULT ''
goal_type               VARCHAR(50)             NOT NULL, DEFAULT 'custom'
target_value            INT                     NOT NULL, DEFAULT 0
current_value           INT                     NOT NULL, DEFAULT 0
deadline                DATE                    NULL
is_completed            TINYINT(1)              NOT NULL, DEFAULT 0
created_at              DATETIME(6)             NOT NULL (auto)
updated_at              DATETIME(6)             NOT NULL (auto)

goal_type choices: problems_solved, rating, contests, custom

Indexes:
- PRIMARY KEY (id)
- INDEX (user_id)
- INDEX (is_completed)

---

5.7 Table: interview_interviewquestion

Stores interview preparation questions (admin-managed).

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
title                   VARCHAR(300)            NOT NULL
description             LONGTEXT                NOT NULL, DEFAULT ''
category                VARCHAR(50)             NOT NULL, DEFAULT 'other'
difficulty              VARCHAR(20)             NOT NULL, DEFAULT 'medium'
link                    VARCHAR(200)            NOT NULL, DEFAULT ''
created_at              DATETIME(6)             NOT NULL (auto)

category choices: arrays, strings, dp, graphs, trees, sorting, binary_search, greedy, math, other
difficulty choices: easy, medium, hard

Indexes:
- PRIMARY KEY (id)
- INDEX (category)
- INDEX (difficulty)

---

5.8 Table: interview_userquestionprogress

Tracks each user's progress on each interview question.

Column                  Type                    Constraints
------                  ----                    -----------
id                      INT AUTO_INCREMENT      PRIMARY KEY
user_id                 INT                     NOT NULL, FK → users_user(id)
question_id             INT                     NOT NULL, FK → interview_interviewquestion(id)
is_completed            TINYINT(1)              NOT NULL, DEFAULT 0
is_bookmarked           TINYINT(1)              NOT NULL, DEFAULT 0
notes                   LONGTEXT                NOT NULL, DEFAULT ''
completed_at            DATETIME(6)             NULL

Indexes:
- PRIMARY KEY (id)
- UNIQUE (user_id, question_id)
- INDEX (user_id)
- INDEX (question_id)
- INDEX (is_completed)

---

6. Entity Relationships

6.1 User → Profile (One-to-One)

One User has exactly one Profile.
A Profile belongs to exactly one User.
A Profile is automatically created when a User registers (via Django signal).

6.2 User → Contest (One-to-Many)

One User can have many Contest records.
Each Contest belongs to exactly one User.
Contests are created or updated during Codeforces synchronization.

6.3 User → Submission (One-to-Many)

One User can have many Submission records.
Each Submission belongs to exactly one User.

6.4 Submission → Problem (Many-to-One)

Many Submissions can reference the same Problem.
A Problem can have many Submissions across different users.
Problems are shared records (not per-user).

6.5 User → Goal (One-to-Many)

One User can have many Goals.
Each Goal belongs to exactly one User.

6.6 User → UserQuestionProgress (One-to-Many)

One User can have progress records for many InterviewQuestions.

6.7 InterviewQuestion → UserQuestionProgress (One-to-Many)

One InterviewQuestion can have progress records from many Users.

---

7. Entity Relationship Diagram (Text Format)

users_user
    |
    |--< profiles_profile         (one-to-one)
    |
    |--< contests_contest         (one-to-many via user_id)
    |
    |--< submissions_submission   (one-to-many via user_id)
    |         |
    |         >-- problem_tracker_problem  (many-to-one via problem_id)
    |
    |--< goals_goal               (one-to-many via user_id)
    |
    |--< interview_userquestionprogress  (one-to-many via user_id)
                |
                >-- interview_interviewquestion  (many-to-one via question_id)

---

8. Normalization

The database design follows Third Normal Form (3NF).

8.1 First Normal Form (1NF)
All tables have a primary key.
All columns contain atomic values.
Note: tags in problem_tracker_problem uses JSON type. This is an accepted modern database pattern for flexible tag storage and is not a 1NF violation in practice.

8.2 Second Normal Form (2NF)
All non-key columns are fully dependent on the primary key.
No partial dependencies exist.

8.3 Third Normal Form (3NF)
No transitive dependencies exist between non-key columns.
For example, rating_change in contests_contest is derived from old_rating and new_rating. This is stored for performance but should be kept in sync during writes.

---

9. Indexing Strategy

Index                               Reason
-----                               ------
users_user(username)               Unique lookup during authentication
users_user(codeforces_handle)      Unique lookup when connecting a platform account
profiles_profile(user_id)          Fast profile retrieval for authenticated user
contests_contest(user_id)          Retrieve all contests for a specific user
contests_contest(user_id, contest_id)  Prevent duplicate contest records per user
problem_tracker_problem(rating)    Filter problems by difficulty rating
submissions_submission(user_id)    Retrieve all submissions for a user
submissions_submission(verdict)    Filter submissions by verdict
goals_goal(user_id)                Retrieve goals for a specific user
interview_interviewquestion(category)   Filter questions by category
interview_interviewquestion(difficulty) Filter questions by difficulty
interview_userquestionprogress(user_id, question_id)  Prevent duplicate progress records

---

10. Analytics App

The analytics app (analytics/) does not have its own database tables.

It reads and aggregates data from:
- submissions_submission
- problem_tracker_problem
- contests_contest

Analytics are calculated at query time from the stored data.

---

11. Codeforces App

The codeforces app (codeforces/) does not have its own database tables.

It provides API endpoints that trigger synchronization using the service layer in users/services.py.

---

12. Database Design Status

Database Version: 1.0
Status: Initial Complete Design
Database: MySQL (SQLite for local development)
Previous Lifecycle Stage: Architecture
Next Lifecycle Stage: Sprint Planning
