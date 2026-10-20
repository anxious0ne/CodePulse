API Specification
Competitive Programming Tracker

Document Version: 1.0
Status: Initial Draft
Lifecycle Stage: Development
Previous Stage: Architecture

---

1. Purpose

This document defines the REST API specification for the Competitive Programming Tracker.

It describes every API endpoint including:

- HTTP method and URL
- Authentication requirement
- Request body fields
- Success response format
- Error response format
- HTTP status codes

---

2. General Information

Base URL (development):     http://127.0.0.1:8000/
Authentication Method:      Django Session Authentication + CSRF tokens
Response Format:            JSON
Content-Type:               application/json

---

3. HTTP Status Codes

Code    Meaning
----    -------
200     OK — Request succeeded
201     Created — Resource created successfully
204     No Content — Resource deleted
400     Bad Request — Invalid input or missing required fields
401     Unauthorized — Authentication required
403     Forbidden — Authenticated but not authorized
404     Not Found — Resource does not exist
503     Service Unavailable — External API (Codeforces) unavailable

---

4. Standard Error Response Format

{
  "error": "Human-readable error message"
}

or for validation errors:

{
  "field_name": ["Error message for this field."]
}

---

5. Authentication Endpoints

Base path: /accounts/

---

5.1 Register

Method:    POST
URL:       /accounts/register/
Auth:      Not required

Request Body:
  username          string    required
  email             string    optional
  password          string    required (min 6 characters)
  confirm_password  string    required (must match password)
  codeforces_handle string    optional

Success Response (302 redirect to /dashboard/):
  Redirects authenticated user to the dashboard after registration.

Error Response (200 with form errors):
  {
    "errors": ["Username is required.", "Passwords do not match."]
  }

---

5.2 Login

Method:    POST
URL:       /accounts/login/
Auth:      Not required

Request Body:
  username    string    required
  password    string    required

Success Response (302 redirect to /dashboard/ or next URL):
  Redirects authenticated user.

Error Response (200 with error):
  {
    "error": "Invalid username or password. Please try again."
  }

---

5.3 Logout

Method:    POST
URL:       /accounts/logout/
Auth:      Required (session)

Success Response (302 redirect to /login/):
  Logs out user and redirects.

---

6. Profile Endpoints

Base path: /api/profile/

---

6.1 Get Own Profile

Method:    GET
URL:       /api/profile/
Auth:      Required

Success Response (200):
  {
    "id": 1,
    "username": "vishal",
    "email": "vishal@example.com",
    "bio": "Competitive programmer",
    "location": "India",
    "github_username": "anxious0ne",
    "website": "https://github.com/anxious0ne",
    "created_at": "2026-10-14T10:00:00Z",
    "updated_at": "2026-10-14T10:00:00Z"
  }

Error Response (401):
  {"detail": "Authentication credentials were not provided."}

---

6.2 Update Own Profile

Method:    PUT / PATCH
URL:       /api/profile/
Auth:      Required

Request Body (any combination of):
  bio               string    optional
  location          string    optional
  github_username   string    optional
  website           string    optional

Success Response (200):
  Updated profile object (same structure as GET response)

---

7. Codeforces Endpoints

Base path: /api/codeforces/

---

7.1 Connect Codeforces Handle

Method:    POST
URL:       /api/codeforces/connect/
Auth:      Required

Request Body:
  handle    string    required (Codeforces username)

Success Response (200):
  {
    "message": "Handle updated to tourist. Use /api/codeforces/sync/ to fetch data.",
    "handle": "tourist"
  }

Error Response (400):
  {
    "error": "Codeforces handle is required."
  }

---

7.2 Sync Codeforces Data

Method:    POST
URL:       /api/codeforces/sync/
Auth:      Required

Request Body: None required

Success Response (200):
  {
    "message": "Sync complete for handle: tourist",
    "result": { ... sync statistics ... }
  }

Error Response (400 — no handle connected):
  {
    "error": "No Codeforces handle connected. Use /api/codeforces/connect/ first."
  }

Error Response (503 — Codeforces unavailable):
  {
    "error": "Sync failed: Could not connect to Codeforces API."
  }

---

7.3 Get Connection Status

Method:    GET
URL:       /api/codeforces/status/
Auth:      Required

Success Response (200):
  {
    "handle": "tourist",
    "is_handle_verified": true,
    "connected": true
  }

  or if no handle connected:

  {
    "handle": null,
    "is_handle_verified": false,
    "connected": false
  }

---

8. Dashboard Endpoint

---

8.1 Get Dashboard Summary

Method:    GET
URL:       /api/dashboard/
Auth:      Required

Success Response (200):
  {
    "username": "vishal",
    "codeforces_handle": "tourist",
    "current_rating": 3822,
    "max_rating": 3979,
    "rank": "legendary grandmaster",
    "total_contests": 309,
    "problems_solved": 5499,
    "total_submissions": 5464,
    "last_synced": "2026-10-14T10:00:00Z"
  }

---

9. Contests Endpoints

Base path: /api/contests/

---

9.1 List User Contests

Method:    GET
URL:       /api/contests/
Auth:      Required

Success Response (200):
  [
    {
      "id": 1,
      "contest_id": 1900,
      "contest_name": "Codeforces Round 900",
      "rank": 15,
      "old_rating": 3800,
      "new_rating": 3822,
      "rating_change": 22,
      "contest_time": "2026-09-15T14:35:00Z"
    },
    ...
  ]

---

10. Problems Endpoints

Base path: /api/problems/

---

10.1 List Problems

Method:    GET
URL:       /api/problems/
Auth:      Required

Query Parameters:
  rating    integer    optional — filter by problem rating
  tag       string     optional — filter by problem tag

Success Response (200):
  [
    {
      "id": 1,
      "contest_id": 1234,
      "problem_index": "A",
      "name": "Two Arrays",
      "rating": 800,
      "tags": ["greedy", "math"]
    },
    ...
  ]

---

10.2 Get Problem Detail

Method:    GET
URL:       /api/problems/<id>/
Auth:      Required

Success Response (200):
  {
    "id": 1,
    "contest_id": 1234,
    "problem_index": "A",
    "name": "Two Arrays",
    "rating": 800,
    "tags": ["greedy", "math"]
  }

Error Response (404):
  {"detail": "No Problem matches the given query."}

---

11. Submissions Endpoints

Base path: /api/submissions/

---

11.1 List Recent Submissions

Method:    GET
URL:       /api/submissions/recent/
Auth:      Required

Query Parameters:
  verdict    string    optional — filter by verdict (e.g. OK, WRONG_ANSWER)

Success Response (200):
  [
    {
      "id": 1,
      "submission_id": 987654321,
      "verdict": "OK",
      "language": "GNU G++17",
      "time_seconds": 1654000000,
      "submitted_at": "2026-10-10T12:00:00Z"
    },
    ...
  ]

---

12. Analytics Endpoints

Base path: /api/analytics/

---

12.1 Topic Analytics

Method:    GET
URL:       /api/analytics/topics/
Auth:      Required

Success Response (200):
  [
    {
      "tag": "dp",
      "count": 120
    },
    {
      "tag": "greedy",
      "count": 98
    },
    ...
  ]

---

12.2 Verdict Analytics

Method:    GET
URL:       /api/analytics/verdicts/
Auth:      Required

Success Response (200):
  {
    "OK": 450,
    "WRONG_ANSWER": 120,
    "TIME_LIMIT_EXCEEDED": 45,
    "COMPILATION_ERROR": 12
  }

---

12.3 Rating Distribution

Method:    GET
URL:       /api/analytics/ratings/
Auth:      Required

Success Response (200):
  [
    {
      "range": "800-1000",
      "count": 80
    },
    {
      "range": "1000-1200",
      "count": 145
    },
    ...
  ]

---

13. Goals Endpoints

Base path: /api/goals/

---

13.1 List Goals

Method:    GET
URL:       /api/goals/
Auth:      Required

Success Response (200):
  [
    {
      "id": 1,
      "title": "Solve 100 problems",
      "description": "",
      "goal_type": "problems_solved",
      "target_value": 100,
      "current_value": 64,
      "deadline": "2026-12-31",
      "is_completed": false,
      "progress_percentage": 64,
      "created_at": "2026-10-01T10:00:00Z",
      "updated_at": "2026-10-14T10:00:00Z"
    },
    ...
  ]

---

13.2 Create Goal

Method:    POST
URL:       /api/goals/
Auth:      Required

Request Body:
  title           string    required
  description     string    optional
  goal_type       string    optional (problems_solved, rating, contests, custom)
  target_value    integer   required
  current_value   integer   optional (default 0)
  deadline        date      optional (YYYY-MM-DD)
  is_completed    boolean   optional (default false)

Success Response (201):
  Created goal object (same as list item)

---

13.3 Get Goal Detail

Method:    GET
URL:       /api/goals/<id>/
Auth:      Required

Success Response (200):
  Single goal object

Error Response (404):
  {"detail": "No Goal matches the given query."}

---

13.4 Update Goal

Method:    PUT / PATCH
URL:       /api/goals/<id>/
Auth:      Required

Request Body: Any fields to update

Success Response (200):
  Updated goal object

---

13.5 Delete Goal

Method:    DELETE
URL:       /api/goals/<id>/
Auth:      Required

Success Response (204):
  No content

---

14. Interview Endpoints

Base path: /api/interview/

---

14.1 List Interview Questions

Method:    GET
URL:       /api/interview/questions/
Auth:      Required

Query Parameters:
  category      string    optional (arrays, strings, dp, graphs, trees, sorting, binary_search, greedy, math, other)
  difficulty    string    optional (easy, medium, hard)

Success Response (200):
  [
    {
      "id": 1,
      "title": "Two Sum",
      "description": "Find two numbers that add to target.",
      "category": "arrays",
      "difficulty": "easy",
      "link": "https://leetcode.com/problems/two-sum/",
      "created_at": "2026-10-01T10:00:00Z"
    },
    ...
  ]

---

14.2 Get or Update User Progress on a Question

Method:    GET / PUT
URL:       /api/interview/progress/<question_id>/
Auth:      Required

GET Success Response (200):
  {
    "id": 1,
    "question": 1,
    "question_title": "Two Sum",
    "question_category": "arrays",
    "question_difficulty": "easy",
    "is_completed": false,
    "is_bookmarked": true,
    "notes": "Remember to use a hashmap.",
    "completed_at": null
  }

PUT Request Body (any combination):
  is_completed      boolean   optional
  is_bookmarked     boolean   optional
  notes             string    optional

PUT Success Response (200):
  Updated progress object

Error Response (404 — question not found):
  {"detail": "Question not found."}

---

15. API Versioning Note

The current API is unversioned (v1 implicit).

Future versions may be introduced at /api/v2/ when breaking changes are required.

---

API Specification Version: 1.0
Status: Initial Draft
