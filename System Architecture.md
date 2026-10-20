### **System Architecture**

**Competitive Programming Tracker**



**Document Version:** 1.0

**Status**: Initial Draft

**Lifecycle Stage:** Architecture

**Previous Stage:** Product Backlog

**Next Stage**: Database Design



##### **1. Purpose**



This document defines the technical architecture of the Competitive Programming Tracker.



It explains:



* technologies used by the system
* responsibilities of each technology
* system components
* frontend and backend structure
* API communication
* database interaction
* Codeforces integration
* authentication
* data synchronization
* security
* deployment considerations
* architectural decisions



The purpose is to establish the technical foundation before implementation begins.



##### **2. Architecture Goals**



The architecture should provide:



1. Clear separation between frontend, backend, and database.
2. Maintainable Django application structure.
3. Reliable integration with the Codeforces API.
4. Secure user authentication and data handling.
5. Efficient storage and retrieval of competitive-programming data.
6. Reusable REST APIs.
7. Responsive user interface.
8. Testable application components.
9. Ability to extend the system with additional coding platforms later.
10. A structure suitable for deployment and future scaling.





##### **3. Selected Technology Stack**

###### **Layer			Technology		Primary Responsibility**

Backend Language	Python			Application and business logic

Backend Framework	Django			Web application framework

API Framework		Django REST Framework	REST API development

Database		MySQL			Persistent data storage

Database Access		Django ORM		Communication between Django and MySQL

Frontend Structure	HTML5			Webpage structure

Frontend Styling	CSS + Custom Tokens	Styling & Coders' Compass Theme Tokens

UI Framework		Tailwind CSS		Utility-based UI development with Work Sans typography

Frontend Logic		JavaScript		Browser-side interaction

Visualization		Chart.js		Charts and analytics visualization

External Integration	Codeforces API		Competitive-programming data

HTTP Client		Requests		Backend HTTP communication

Version Control		Git			Source-code version control

Repository		GitHub			Code hosting and collaboration

Testing			Django Test Framework/  Automated testing

&#x09;		pytest-django	



Additional technologies such as Docker, Redis, Celery, CI/CD tools, and cloud infrastructure may be introduced later if justified by project requirements.



##### **4. Technology Responsibilities**

###### **4.1 Python**



Python is the primary backend programming language.



It will be responsible for:



* business logic
* data processing
* API integration
* analytics calculations
* validation
* database interaction through Django
* automated tests



###### **4.2 Django**



Django provides the core backend framework.



It will manage:



* URL routing
* request and response processing
* authentication
* application structure
* database models
* validation
* security mechanisms
* administrative functionality



###### **4.3 Django REST Framework**



Django REST Framework will be used to expose application functionality through REST APIs.



For example:



GET /api/profile/

GET /api/contests/

GET /api/problems/

GET /api/analytics/

POST /api/codeforces/sync/



The API will generally exchange data using JSON.



###### **4.4 MySQL**



MySQL will provide persistent storage for application data.



It will store information such as:



* users
* profiles
* coding-platform accounts
* contests
* problems
* submissions
* goals
* interview-preparation data
* synchronization information



###### **4.5 Django ORM**



Django ORM will provide the application-level interface to MySQL.



Conceptually:



Python

&#x20;  ↓

Django ORM

&#x20;  ↓

SQL

&#x20;  ↓

MySQL



The application will primarily use Django models and ORM operations rather than manually writing SQL for normal database operations.



###### **4.6 HTML5**



HTML5 will define the structure of web pages.



It will be used for:



* forms
* navigation
* tables
* cards
* dashboard components
* page layouts



###### **4.7 CSS and Tailwind CSS**



CSS provides the underlying styling technology.



Tailwind CSS will provide reusable utility classes for:



* spacing
* typography
* layout
* responsive design
* buttons
* forms
* cards
* navigation
* dashboard components



###### **4.8 JavaScript**



JavaScript will provide browser-side functionality.



It will handle:



* user interactions
* asynchronous API requests
* dynamic page updates
* form interactions
* dashboard updates
* communication with REST APIs



###### **4.9 Chart.js**



Chart.js will be used to visualize analytics data.



Possible visualizations include:



* rating progression
* problem difficulty distribution
* topic distribution
* contest performance
* activity trends



The data flow will be:



MySQL

&#x20; ↓

Django

&#x20; ↓

REST API

&#x20; ↓

JSON

&#x20; ↓

JavaScript

&#x20; ↓

Chart.js

&#x20; ↓

Visualization



###### **4.10 Codeforces API**



The Codeforces API will initially be the primary external data source.



It will provide relevant information such as:



###### user profile information

###### rating history

###### contest information

###### submissions

###### problem information



The application will access the external API through the Django backend.



##### **5. High-Level System Architecture**



The system will follow a layered web architecture.



&#x20;                        USER

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌────────────────┐

&#x20;               │     FRONTEND       │

&#x20;               │                    │

&#x20;               │ HTML5              │

&#x20;               │ Tailwind CSS       │

&#x20;               │ JavaScript         │

&#x20;               │ Chart.js           │

&#x20;               └─────────┬──────┘

&#x20;                         │

&#x20;                     HTTP / JSON

&#x20;                         │

&#x20;                         ▼

&#x20;               ┌────────────────┐

&#x20;               │      BACKEND       │

&#x20;               │                    │

&#x20;               │ Python             │

&#x20;               │ Django             │

&#x20;               │ Django REST        │

&#x20;               │ Framework          │

&#x20;               └─────────┬──────┘

&#x20;                            │

&#x20;               ┌─────────┴──────────┐

&#x20;               │                         │

&#x20;               ▼                         ▼

&#x20;         ┌────────────┐       ┌──────────────┐

&#x20;         │   MySQL       │       │      Codeforces  │

&#x20;         │  Database     │       │       API        │

&#x20;         └────────────┘       └──────────────┘



##### **6. Architectural Layers**

###### **6.1 Presentation Layer**

Responsible for all user-facing interactions, visual presentation, and client-side data rendering.

The Presentation Layer is structured into two distinct surfaces:

1. **Public Presentation Surface (`/` -> `templates/home.html`)**:
   * Designed for discovery, orientation, and onboarding.
   * Delivers technical marketing copy, live telemetry radar widgets, platform statistics, and instant Call-to-Action routes (Register, Login, Live Demo).
   * Context-aware: dynamically adapts CTA banners for authenticated sessions.

2. **Private Analytics Surface (`/dashboard/` -> `templates/dashboard.html`)**:
   * Protected cockpit accessible only to authenticated users (`@login_required`).
   * Hosts high-density KPI cards, interactive Chart.js visualizations (Rating Progression, Verdicts Doughnut, Difficulty Distribution), problem topic mastery tables, submission audit feeds, and Codeforces handle synchronization controls.
   * Integrates the dynamic Onboarding & Welcome Back greeting banner.

3. **Authentication Surface (`/accounts/*`)**:
   * Neo-brutalist authentication cards for Login (`templates/accounts/login.html`) and Registration (`templates/accounts/register.html`).
   * Provides 1-click live demo account auto-fill (`demo_coder`) for rapid evaluation.

**Technologies**:
* HTML5 (Semantic document outline)
* Vanilla CSS & Tailwind CSS (Design tokens, coordinate grid, and neo-brutalist utilities)
* Google Font: *Work Sans* (Primary geometric typeface) & Monospace fonts (Telemetry data)
* JavaScript (ES6+ modular DOM controllers and async fetch clients)
* Chart.js 4.4+ (Custom-themed responsive data visualizations)



###### **6.2 Application Layer**



Responsible for application behavior.



Technologies:



Python

Django

Django REST Framework



Responsibilities include:



* authentication
* business rules
* validation
* API endpoints
* synchronization
* analytics
* data processing



###### **6.3 Data Layer**



Responsible for persistent storage.



Technology:



MySQL



Django ORM will provide the application interface to this layer.



###### **6.4 External Integration Layer**



Responsible for communication with external competitive-programming platforms.



Initial integration:



Codeforces API



The architecture should allow additional platforms to be integrated later without significantly modifying unrelated application components.



##### **7. Django Project Structure**



The planned Django structure is:



competitive\_tracker/

│

├── manage.py

│

├── config/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

├── accounts/

├── profiles/

├── codeforces/

├── contests/

├── problems/

├── analytics/

├── goals/

└── interview/



##### **8. Django Application Responsibilities**

**Django App	Responsibility**

accounts	Registration, login, logout, authentication

profiles	User profile and coding-account association

codeforces	Codeforces API communication

contests	Contest and rating-related data

problems	Problems and submissions

analytics	Statistics and analytical calculations

goals		Personal coding goals

interview	Interview preparation



The applications should have clearly separated responsibilities.



##### **9. Frontend Architecture**

The frontend will initially use a server-oriented Django web application combined with JavaScript and Chart.js for dynamic dashboard functionality.

```
Browser
   │
   ├─ HTML5 Structure
   ├─ Tailwind CSS + Coders' Compass Design Tokens
   └─ JavaScript & Chart.js
         │
         ▼
     REST API
         │
         ▼
      Django
```

We are intentionally not introducing React or another heavy frontend framework at this stage. This keeps the technology stack manageable while establishing solid web fundamentals.

###### **9.1 UI/UX Design System Specification (Coders' Compass Aesthetic)**

The user interface follows a modern **Technical Editorial & Neo-Brutalist** aesthetic inspired directly by the design system of [Coders' Compass](https://coderscompass.org/).

Key visual principles include:
* **Warm Technical Palette**: Balanced contrast between deep atmospheric blues (`Navy`, `Navy Deep`), warm grounding tones (`Peach`, `Amber`, `Cream`), and energetic accents (`Sky Blue`, `Mint Green`, `Pink`).
* **Tactile Neo-Brutalist Geometry**: Cards, buttons, and badges utilize crisp solid borders (1.5px to 2px) and sharp, flat offset drop-shadows (`3px 3px 0px var(--color-navy-darker)`) without diffuse blur, providing clear visual hierarchy and an engineering-grade tactile feel.
* **Tight Border Radii**: Components feature subtle corner rounding (`3px` to `4px`) rather than pill shapes or extreme rounded corners.
* **Technical Background Grid**: Subtle graph/coordinate grid lines (`32px` grid intervals) evoking architectural blueprints and engineering graph paper.

###### **9.2 Color Tokens & Palette Hierarchy**

The application defines semantic color variables mapped to functional roles:

| Token Name | Hex Code | Light Theme Role | Dark Theme Role | Functional Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `--color-peach` | `#F8D7B0` | Primary Brand Card / Highlight | Warm Accent / Subtitle | Brand accents, key container titles |
| `--color-amber` | `#EFBF80` | Breadcrumb Bg / Borders | Highlight / Stat Values | KPI highlights, breadcrumbs, rating tags |
| `--color-cream` | `#F2F0EC` | Main Page Background | — | Warm paper neutral background |
| `--color-brown-dark` | `#392518` | Primary Headings / Strong Borders | Contrast Framing | High contrast framing and solid shadows |
| `--color-charcoal` | `#333333` | Body Text | — | Crisp readable text in light mode |
| `--color-navy` | `#17415C` | Hero Background / Contrast | Main Card / Container Surface | Dashboard panel backgrounds |
| `--color-navy-deep` | `#243A45` | Drop Shadows | Main Page Background | Deep canvas background |
| `--color-off-white` | `#F3F2F2` | Surface Inputs | Primary Text | High-contrast text on dark surfaces |
| `--color-sky` | `#7BD4FF` | Primary Action (CTA) | Primary Action (CTA) | Primary buttons, active tabs, focus ring |
| `--color-sky-deep` | `#288CBE` | Button Hover State | Button Hover State | CTA hover and active states |
| `--color-green` | `#90EE90` | Secondary Action / Success | Secondary Action / Success | Positive deltas, verified pills, secondary CTA |
| `--color-green-deep` | `#409540` | Success Dark / Active | Success Dark / Active | Hover for secondary actions |
| `--color-pink` | `#FF90E8` | Category Badges | Category Badges | Special tags, algorithm difficulty badges |
| `--color-violet` | `#C9A0EC` | Visited Links / Master Tier | Visited Links / Master Tier | Candidate Master & higher ranks |
| `--color-error` | `#FF6B6B` | Error / Alert / Loss | Error / Alert / Loss | Validation errors, negative rating changes |

###### **9.3 Typography Scale**

* **Primary Font Family**: `'Work Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
  * Work Sans delivers an open, geometric, highly legible modern grotesque aesthetic suited for dense data interfaces.
  * Weights utilized: `400` (Regular body), `500` (Medium labels & table headers), `600` (Semibold cards & buttons), `700` (Bold KPI values & titles).
* **Monospace Font Family**: `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`
  * Applied to Codeforces handles, ratings, rank deltas, timestamps, and problem codes.

###### **9.4 Component Design Standards**

1. **Primary Buttons (CTA)**:
   * Background: `--color-sky` (`#7BD4FF`) with text `--color-brown-dark` (`#392518`)
   * Border: `1.5px solid var(--color-brown-dark)`
   * Shadow: `3px 3px 0 var(--color-navy-darker)`
   * Hover: `--color-sky-deep` (`#288CBE`) with text `--color-off-white`
   * Active: Translates `1px 1px` with shadow reduced to `2px 2px 0`
2. **Secondary Buttons**:
   * Background: `--color-green` (`#90EE90`) with hover `--color-green-deep` (`#409540`)
   * Shadow: `3px 3px 0 var(--color-navy-darker)`
3. **Dashboard Metric & Analytics Cards**:
   * Background: `--color-navy` (`#17415C`)
   * Border: `1px solid rgba(239, 191, 128, 0.22)`
   * Shadow: `3px 3px 0 #0E2433`
   * Border Radius: `4px`
4. **Data Tables (Contests & Submissions)**:
   * Header: Sticky top bar with `--color-amber` (`#EFBF80`) titles on dark navy background.
   * Hairline Dividers: `1px solid rgba(239, 191, 128, 0.15)`.
5. **Tag Badges**:
   * Distinct colored pills with `3px` radius for problem tags (e.g. `dp`, `graphs`, `math`, `greedy`).

###### **9.5 Chart.js Visualization Standards**

* **Rating Progression (Line Chart)**:
  * Stroke: `--color-sky` (`#7BD4FF`) with 2.5px width.
  * Fill: Vertical gradient from `rgba(123, 212, 255, 0.16)` to transparent.
  * Data Points: Radius 3.5px with `--color-sky` fill and `--color-navy-deep` outline.
  * Grid lines: Subtle warm tone `rgba(242, 240, 236, 0.08)`.
* **Verdicts Distribution (Doughnut Chart)**:
  * OK / Accepted: `--color-green` (`#90EE90`)
  * Wrong Answer: `--color-error` (`#FF6B6B`)
  * Time Limit Exceeded: `--color-amber` (`#EFBF80`)
  * Memory Limit / Runtime Error: `--color-pink` (`#FF90E8`)
  * Compilation Error: `--color-violet` (`#C9A0EC`)
* **Difficulty Distribution (Bar Chart)**:
  * Bars: Gradient from `--color-amber` (`#EFBF80`) to `--color-peach` (`#F8D7B0`), hover state in `--color-sky` (`#7BD4FF`).

###### **9.6 Page Hierarchy & Route Architecture**

The application presents a clearly delineated routing and information hierarchy:

| Route | View Controller | Template | Access Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `users.views.home_page` | `templates/home.html` | Public | Front landing page with feature cards, telemetry radar, and auth CTAs |
| `/dashboard/` | `users.views.dashboard_page` | `templates/dashboard.html` | Authenticated | Main analytics dashboard with charts, KPI cards, and sync controls |
| `/accounts/login/` | `accounts.views.login_view` | `templates/accounts/login.html` | Anonymous (guest) | Login page with credential form and 1-click demo filler |
| `/accounts/register/` | `accounts.views.register_view` | `templates/accounts/register.html` | Anonymous (guest) | Sign-up page with handle binding and initial sync trigger |
| `/accounts/logout/` | `accounts.views.logout_view` | — | Authenticated | Terminates user session and redirects to login |
| `/api/*` | DRF ViewSets / APIViews | JSON Payload | Authenticated / Token | Modular REST endpoints serving chart and sync data |

```
                       [ Incoming Visitor ]
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
        [ Anonymous Guest ]          [ Authenticated User ]
                   │                           │
                   ├─ GET / (Landing Page)     ├─ GET / (Personalized Home)
                   ├─ GET /accounts/login/     ├─ GET /dashboard/ (Analytics)
                   └─ GET /accounts/register/  └─ POST /accounts/logout/
```

###### **9.7 Public Landing Page Design Specification**

The landing page (`templates/home.html`) serves as the editorial gateway to the platform. Built on the Coders' Compass neo-brutalist design tokens, it contains four structured tiers:

1. **Editorial Hero Section**:
   * **Badge Ribbon**: Eyebrow badge in Warm Peach (`#F8D7B0`) with `#392518` border: `Coders' Compass Edition • Codeforces Tracker`.
   * **Punchy Typography**: Massive geometric headline (`text-4xl` to `text-6xl`, font-black, uppercase) featuring color-accented keywords:
     * *Master* in Sky Blue (`#7BD4FF`)
     * *Climb* in Peach (`#F8D7B0`)
   * **Interactive CTA Switcher**:
     * For Guests: Dual brutalist action buttons: Primary Sky Blue *"Create Free Account →"* (`btn-compass-primary`) and Warm Amber *"Sign In"* (`btn-compass-secondary`), accompanied by a live demo credential hint.
     * For Authenticated Users: Direct *"Go to Your Dashboard →"* primary button and a *"Welcome back, {username}!"* indicator chip.
   * **Live Telemetry Radar Badge**:
     * Circular compass emblem with slow CSS rotation animation (`animate-spin-slow`).
     * Live metrics chips displaying supported Codeforces Rating Range (`800 – 3500+`) and Algorithm Topics (`22+ Tags`).
     * Real-time pulsing operational status indicator (`API Status: Fully Operational`).

2. **Key Platform Metrics Strip**:
   * Four neo-brutalist metric cards displaying high-impact system benchmarks:
     * `20+` Official Contest Rounds (Sky Blue border)
     * `9 Tiers` Difficulty Brackets (Amber border)
     * `22 Tags` Algorithmic Topics (Mint Green border)
     * `< 1s` Direct Codeforces Sync (Pink border)

3. **Core Feature Quadrants**:
   * Four distinct neo-brutalist cards highlighting the analytical engine:
     1. **Official Contest Rating Trajectory**: Visualizing progression from Pupil to Grandmaster with multi-stop gradient line charts.
     2. **Topic-Wise Weak Area Discovery**: Aggregating solve rates across DP, Graphs, Trees, Math, and Greedy to prioritize practice.
     3. **Verdict & Accuracy Distribution**: Identifying submission friction points (WA, TLE, MLE) via vibrant doughnut charts.
     4. **Difficulty Ladder Progression**: Tracking comfort levels across rating brackets from 800 to 2600+.

4. **Closing Conversion Strip**:
   * Full-width card with Warm Peach top border (`border-t-8 border-t-compass-peach`) prompting the user to explore the live dashboard.

###### **9.8 Personalized Greeting & Onboarding State Machine**

To provide a distinct, personalized experience for first-time versus returning users, the application implements an onboarding state machine managed across the session and presentation layers:

```
                  ┌──────────────────────────────┐
                  │      User Authenticates      │
                  └──────────────┬───────────────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
       [ Registration Flow ]              [ Login Flow ]
                │                                 │
    session['is_new_user'] = True    session['is_new_user'] = False
                │                                 │
                └────────────────┬────────────────┘
                                 ▼
                     GET /dashboard/ View
                                 │
              ┌──────────────────┴──────────────────┐
              ▼                                     ▼
      is_new_user == True                  is_new_user == False
              │                                     │
    ┌───────────────────────────┐         ┌───────────────────────────┐
    │  Green Onboarding Banner  │         │  Sky Blue Greeting Banner │
    │  "🎉 Welcome to           │         │  "👋 Welcome back,        │
    │   CodeTrack AI, {user}!"  │         │   {user}!"                │
    │  [Set Handle → CTA]       │         │                           │
    └───────────────────────────┘         └───────────────────────────┘
```

1. **New User State (`is_new_user = True`)**:
   * **Trigger**: Activated when a user completes registration via `accounts.views.register_view`. The view injects `request.session['is_new_user'] = True`.
   * **Fallback Heuristic**: If the session flag has expired, `users.views.dashboard_page` checks whether `user.date_joined` is within the last 2 hours and whether total submissions count is `0`.
   * **Visual Presentation**:
     * Container: Deep emerald gradient (`from-compass-navy to-[#133526]`) with an `8px` Mint Green (`#90EE90`) left border.
     * Chip: High-contrast `NEW CODER` pill in `#90EE90` with dark brown text.
     * Headline: *"🎉 Welcome to CodeTrack AI, {{ user.username }}!"*
     * Subtext: Educational prompt guiding the user to bind their Codeforces handle and perform their first synchronization.
     * Action CTA: Direct *"Set Handle →"* button linking to `#handle-input` for instant focus.

2. **Returning User State (`is_new_user = False`)**:
   * **Trigger**: Activated when an existing user signs in via `accounts.views.login_view`. The view sets `request.session['is_new_user'] = False`.
   * **Visual Presentation**:
     * Container: Deep cyan gradient (`from-compass-navy to-[#122e42]`) with an `8px` Sky Blue (`#7BD4FF`) left border.
     * Icon Badge: Waving hand icon with Sky Blue background.
     * Headline: *"👋 Welcome back, {{ user.username }}!"*
     * Subtext: Motivational greeting highlighting latest rating trends and solved problem updates.

3. **Contextual Home Page Recognition**:
   * When an authenticated user visits `/`, the public hero recognizes the active session and renders a personalized chip: *"Welcome back, {{ user.username }}!"*, swapping the registration CTA with *"Go to Your Dashboard →"*.

###### **9.9 Global Navigation & Header Standards**

The top navigation bar (`templates/base.html`) provides persistent orientation across all pages:
* **Background & Border**: Warm Peach (`#F8D7B0`) with a 4px solid Dark Brown (`#392518`) bottom border and an Amber (`#EFBF80`) highlight ribbon.
* **Brand Identity**: Stylized compass logo (`fa-compass` inside an Amber circular badge with `2px` solid drop-shadow) linking to `/`.
* **Dynamic Nav Links**:
  * `Home` (Always visible)
  * `Dashboard` (Rendered when `user.is_authenticated`)
* **User Profile & Session Controls**:
  * Displays user handle / username in a neo-brutalist tag badge with initial avatar circle.
  * Direct tactile `Logout` button with hover state transitions.




##### **10. Backend Architecture**



The backend will follow Django's application structure.



Conceptually:



HTTP Request

&#x20;    ↓

URL Router

&#x20;    ↓

View / API View

&#x20;    ↓

Serializer / Validation

&#x20;    ↓

Business Logic

&#x20;    ↓

Django ORM

&#x20;    ↓

MySQL



For external API operations:



HTTP Request

&#x20;    ↓

Django API

&#x20;    ↓

Codeforces Service

&#x20;    ↓

Codeforces API

&#x20;    ↓

JSON Response

&#x20;    ↓

Validation

&#x20;    ↓

Database



##### **11. REST API Architecture**



The backend will expose APIs grouped by functionality.



Example structure:



/api/

│

├── auth/

├── profile/

├── codeforces/

├── contests/

├── problems/

├── analytics/

├── goals/

└── interview/



Example endpoints:



POST   /api/auth/register/

POST   /api/auth/login/

POST   /api/auth/logout/



GET    /api/profile/

PUT    /api/profile/



POST   /api/codeforces/connect/

POST   /api/codeforces/sync/



GET    /api/contests/

GET    /api/problems/

GET    /api/analytics/

GET    /api/goals/

POST   /api/goals/



The exact API specification will be designed later in the API Specification document.



##### **12. Request and Response Flow**



A normal dashboard request will follow:



User

&#x20;↓

Browser

&#x20;↓

HTTP Request

&#x20;↓

Django URL Router

&#x20;↓

API View

&#x20;↓

Business Logic

&#x20;↓

Django ORM

&#x20;↓

MySQL

&#x20;↓

Data

&#x20;↓

Serializer

&#x20;↓

JSON Response

&#x20;↓

JavaScript

&#x20;↓

Dashboard



##### **13. Codeforces Integration Architecture**



The browser will not directly manage the Codeforces API integration.



Instead:



Browser

&#x20;  ↓

Django Backend

&#x20;  ↓

Codeforces Service

&#x20;  ↓

Codeforces API

&#x20;  ↓

JSON Response

&#x20;  ↓

Validation

&#x20;  ↓

Data Transformation

&#x20;  ↓

MySQL



This provides a central location for:



* API requests
* error handling
* validation
* synchronization logic
* rate-limit management
* data transformation



##### **14. Data Synchronization Architecture**



When a user requests synchronization:



User clicks "Sync"

&#x20;       ↓

Frontend sends request

&#x20;       ↓

Django receives request

&#x20;       ↓

Codeforces API is contacted

&#x20;       ↓

Response is validated

&#x20;       ↓

Data is transformed

&#x20;       ↓

Existing records are checked

&#x20;       ↓

New/updated records are stored

&#x20;       ↓

Synchronization timestamp updated

&#x20;       ↓

Response sent to frontend

&#x20;       ↓

Dashboard updated



The synchronization mechanism should avoid unnecessary duplicate records.



##### **15. Authentication Architecture**

The authentication architecture balances security, session isolation, and personalized user onboarding:

```
                            [ User ]
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
    [ Registration View ]               [ Login View ]
               │                               │
    • Validates unique user/email       • Authenticates credentials
    • Verifies Codeforces handle        • Enforces CSRF token
    • Creates User model record         • Initializes session
    • Sets session['is_new_user'] = T   • Sets session['is_new_user'] = F
               │                               │
               └───────────────┬───────────────┘
                               ▼
                   [ Django auth_login() ]
                               │
                               ▼
                  [ Authenticated Session ]
                               │
                               ▼
                   [ Redirect to /dashboard/ ]
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
      is_new_user == True             is_new_user == False
               │                               │
    [ New User Onboarding ]         [ Returning User Welcome ]
    • Mint Green Welcome Banner     • Sky Blue Welcome Back Banner
    • Direct Handle Setup CTA       • Direct Analytics Cockpit
```

**Key Authentication Security Measures**:
1. **Password Hashing**: Django's PBKDF2 with SHA-256 password hasher with salt generation.
2. **CSRF Protection**: All form submissions (login, registration, handle updates) require strict `{% csrf_token %}` verification.
3. **Session Cookie Isolation**: HTTP-only session cookies with configurable expiry and secure transport flags.
4. **Login Redirection**: Unauthenticated attempts to access `@login_required` views (e.g. `/dashboard/`) automatically capture `?next=` parameters for seamless post-login redirection.



Authorization will determine which functionality a normal user and administrator can access.



##### **16. Security Architecture**



The system will consider:



* password security
* authentication
* authorization
* input validation
* CSRF protection
* secure session handling
* environment variables
* protection of database credentials
* protection of secret keys
* HTTPS in production
* prevention of unauthorized access



Sensitive configuration should not be committed to GitHub.



Example:



.env



will remain outside version control.



A safe example configuration can be provided through:



.env.example





##### **17. Error Handling Architecture**



Errors may originate from:



User Input

&#x20;    ↓

Application Logic

&#x20;    ↓

Database

&#x20;    ↓

External API



The system should provide appropriate handling for:



* invalid input
* authentication failure
* database errors
* unavailable Codeforces API
* invalid Codeforces username
* synchronization failure
* duplicate data
* unexpected server errors



External API failures should not expose internal implementation details to the user.



##### **18. Performance Considerations**



Initial performance considerations include:



* efficient database queries
* appropriate database indexing
* avoiding unnecessary API calls
* minimizing duplicate synchronization
* pagination for large datasets
* efficient API responses
* frontend asset optimization



Advanced caching and asynchronous processing can be introduced later if actual requirements justify them.



##### **19. Scalability Considerations**



The initial system will be designed so that additional coding platforms can potentially be added later.



Conceptually:

&#x20;

&#x20;                  Platform Integration

&#x20;                           │

&#x20;         ┌─────────────┼─────────────┐

&#x20;         ▼                ▼                ▼

&#x20;    Codeforces      Platform B    Platform C



The first implementation will focus on Codeforces rather than attempting to support every competitive-programming platform simultaneously.



20\. Deployment Architecture



The production architecture is expected to follow:



&#x20;                   INTERNET

&#x20;                      │

&#x20;                      ▼

&#x20;                Web Server

&#x20;                      │

&#x20;                      ▼

&#x20;             Django Application

&#x20;                      │

&#x20;         ┌─────────┴─────────┐

&#x20;         ▼                        ▼

&#x20;        MySQL                  Codeforces

&#x20;        Database               API



The exact hosting provider, web server, containerization strategy, and CI/CD configuration will be selected during the deployment stage.



##### **21. Architecture Decisions**

**Decision		Selected Approach	Reason**

Backend			Django			Strong Python web framework and suitable for project 						scope

API			Django REST Framework	Structured REST API development

Database		MySQL			Familiar relational database and suitable for project 						requirements

Frontend		HTML/CSS/JavaScript	Builds strong web fundamentals

UI			Tailwind CSS		Efficient responsive UI development

Charts			Chart.js		Lightweight and suitable for dashboard visualizations

Initial platform	Codeforces		Provides accessible competitive-programming data 						through an API

Frontend framework	None initially		Avoid unnecessary complexity

Architecture		Layered architecture	Clear separation of responsibilities



##### **22. Architectural Principles**



The project will follow these principles:



###### Separation of Concerns



Each component should have a clear responsibility.



###### Modularity



Features should be separated into logical Django applications.



###### Reusability



Common functionality should be implemented in reusable components.



###### Security by Design



Security should be considered during development rather than added only at the end.



###### Maintainability



Code should be understandable and easy to modify.



###### Testability



Important business logic and application behavior should be testable independently.



###### Incremental Development



The system should be developed through manageable Agile increments.





##### **23. Architecture Boundary**



The architecture document defines the technical structure of the system.



It does not yet define the detailed database schema.



The next document will define:



Entities

↓

Tables

↓

Columns

↓

Primary Keys

↓

Foreign Keys

↓

Relationships

↓

Indexes

↓

Constraints





##### **24. Architecture Status**



**Architecture Version**: 1.0

**Status**: Initial Complete Draft

**Database**: MySQL

**Backend**: Python + Django + Django REST Framework

**Frontend**: HTML5 + CSS + Tailwind CSS + JavaScript + Chart.js

**External** Integration: Codeforces API



**Next Lifecycle Stage**: Database Design

