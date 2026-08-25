**Discovery**



**Competitive Programming Tracker**



**Document Version:** 1.0

**Status**: Initial Draft

**Project** **Stage**: Discovery

**Previous** **Stage**: Product Idea

**Next** **Stage**: Requirements



\---



1\. **Purpose** **of** **Discovery**



The purpose of the Discovery stage is to understand the problem, target users, existing solutions, available technical resources, project feasibility, and potential differentiation before defining detailed software requirements.



This stage is intended to answer:



* Is the identified problem real and relevant?
* Who experiences the problem?
* What solutions already exist?
* What functionality is already available in existing platforms?
* What technical resources are available?
* What limitations may affect the project?
* What opportunity exists for our proposed application?
* What should and should not be included in the first version?



\---



**2. Problem Discovery**



Competitive programmers commonly use multiple platforms and tools to practice problems and participate in contests.



Important information such as:



* ratings
* contest history
* submissions
* solved problems
* problem difficulty
* problem topics
* activity history



may be distributed across different platforms.



The discovery process identifies an opportunity to provide a centralized application for organizing and analyzing this information.



However, the investigation also shows that the general concept of a competitive-programming tracker is already implemented by several existing tools.



Therefore, the project should not be positioned simply as:



> "A website that tracks Codeforces statistics."



Instead, the product should provide a clear combination of functionality, usability, architecture, or future intelligence that differentiates it from existing trackers.



\---



**3. Existing Solutions**



The discovery process identified several existing products and projects with overlapping functionality.



**CP Tracker**



A recently published CP Tracker project provides features including importing submissions from multiple competitive-programming platforms, visual analytics, heatmaps, CSV import/export, and public profiles. It supports platforms including Codeforces, AtCoder, Luogu, and QOJ.               



**CF Tracker**



Another existing project, CF Tracker, provides Codeforces-based analytics including problem-solving progress, contest rating graphs, submission activity, verdict distribution, topic statistics, and multi-user leaderboards.



**DashCode**



DashCode is a full-stack competitive-programming analytics platform supporting multiple platforms and providing statistics, visualization, achievements, comparative analysis, and data export.



**Other Emerging Tools**



Other recent projects also provide unified coding analytics, including systems that combine data from platforms such as LeetCode, Codeforces, CodeChef, AtCoder, and other developer platforms.



\---



**4. Competitive Analysis**



The discovery indicates that basic features such as:



* profile tracking
* rating graphs
* contest history
* problem counts
* submission statistics
* heatmaps
* topic analysis



are already common in competitive-programming analytics products.



Therefore, these features should be treated as \*\*baseline functionality\*\*, rather than the primary innovation of the project.



The project should focus on building these features with a strong software-engineering architecture and leave room for additional functionality in later versions.



\---



**5. Identified Opportunity**



The project can differentiate itself by combining a well-structured full-stack platform with deeper personalization and future intelligent capabilities.



Potential areas include:



**Personalized Progress Tracking**



Instead of displaying only raw statistics, the system can organize information around individual user goals and progress.



**Unified Performance Analysis**



The platform can eventually support multiple coding platforms and provide a common view of a user's coding activity.



**Interview Preparation**



Competitive-programming data can eventually be combined with interview preparation activities to provide a broader view of technical preparation.



**Intelligent Recommendations**



Future versions can analyze user activity and recommend suitable practice areas, problems, or preparation plans.



**Agentic AI Extension**



A future version may introduce AI agents capable of analyzing user performance, selecting relevant tools/data, generating recommendations, and adapting preparation plans based on subsequent user progress.



This feature is considered a future direction during Discovery and is not assumed to be part of the initial web-development implementation.



\---



**6. Technical Feasibility**



The project is technically feasible using publicly available web technologies and APIs.



Codeforces provides an official API that exposes machine-readable JSON data. Its API includes methods such as:



* 'user.info'
* 'user.rating'
* 'user.status'
* 'contest.list'
* 'contest.ratingChanges'
* 'problemset.problems'



These APIs can provide information required for profile, rating, contest, problem, and submission-related functionality.



The Codeforces API documentation also specifies that API requests are rate-limited to at most one request every two seconds, which must be considered when designing synchronization and caching mechanisms.



This creates a technical requirement for the future architecture to avoid unnecessary repeated requests.



\---



**7. Initial Data Strategy**



For the first implementation, the project should prioritize platforms with accessible and reliable data sources.



Initial Candidate



Codeforces



Reason:

* Official API available.
* User profile information available.
* Rating history available.
* Submission history available.
* Problem information available.
* Contest information available.



Other platforms can be investigated during the Requirements and Architecture stages.



The system should not assume that every platform provides equivalent official API access.



\---



**8. Target Users Confirmed During Discovery**



The initial target users remain:



**Primary**



* College students learning competitive programming.
* Competitive programmers.
* Students preparing for coding interviews.



**Secondary**



* Students preparing for software engineering placements.
* Coding communities and college programming clubs.



\---



**9. User Problems Identified**



The discovery process identifies the following potential user problems:



P1 — Scattered Information



Users may need to visit multiple platforms to understand their overall coding activity.



P2 — Raw Statistics



Existing platforms provide substantial amounts of data, but users may still need to interpret the data themselves.



P3 — Lack of Consolidated Progress Tracking



Users may want a single place to monitor personal goals and historical progress.



P4 — Difficulty Identifying Improvement Areas



A user may know their rating or solved count without clearly understanding which areas require additional practice.



P5 — Preparation Management



Users preparing for interviews may need to manage competitive programming practice and interview preparation separately.



\---



**10. Technical Constraints Identified**



The following constraints were identified during Discovery:



**External API Dependency**



The application depends on external platform APIs for some data.



Changes to those APIs may affect the application.



**API Rate Limits**



External APIs may impose request limits. The Codeforces API currently specifies a maximum request frequency of one request every two seconds.



**Data Availability**



Not every platform necessarily exposes the same level of public data or an official API.



**Data Synchronization**



The application must determine when and how external data should be refreshed.



**Privacy**



Only appropriate publicly accessible or authorized data should be collected and stored.



\---



**11. Initial Differentiation Strategy**



Based on the discovery findings, the project should NOT compete by simply providing another rating dashboard.



The proposed differentiation direction is:



> A structured, user-centric coding progress platform that combines competitive-programming analytics, personal goals, preparation tracking, and a foundation for future intelligent assistance.\*\*



The initial implementation will establish the software foundation.



Future versions can extend the system with intelligent recommendations and agentic workflows.



\---



**12. Discovery Conclusions**



The Discovery stage confirms that:



1\. Competitive-programming analytics is a real and technically feasible product category.

2\. Existing tools already provide many basic tracking and visualization features.

3\. A simple Codeforces dashboard would not provide sufficient differentiation.

4\. Codeforces provides an official API suitable for the initial implementation.

5\. API rate limits and external-service dependency must be considered during architecture design.

6\. The project should initially focus on strong web-development and software-engineering fundamentals.

7\. Personalization, interview preparation, and intelligent/agentic capabilities can provide future differentiation.

8\. The exact MVP and functional requirements should be determined in the next stage.



\---



**13. Discovery Decision**



**Decision**: PROCEED



The project is considered feasible and worth continuing to the Requirements stage.



However, the project will \*\*not\*\* be positioned as a completely new concept.



The development objective is to create a well-engineered, modular, extensible platform with meaningful differentiation through personalization and future intelligent capabilities.



\---



**Discovery Status**: Completed

**Decision**: Proceed to Requirements

**Next Lifecycle Stage**: Requirements



