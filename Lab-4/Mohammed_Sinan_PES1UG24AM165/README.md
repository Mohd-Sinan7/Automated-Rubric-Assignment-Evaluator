# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Student:** Mohammed Sinan M T (PES1UG24AM165)
**Jira project:** Evaluator-Integrity (key `EE`), Scrum template, company-managed
**Scenario:** Problem Statement #02, Test Case 4: Academic Integrity, Regrade Appeals & Cohort Analytics

## What this lab is about

The functional requirements from Lab 1 were turned into an Agile backlog in Jira: grouped into Epics, written as User Stories, prioritised, estimated with story points, and then run through two simulated sprints. Burndown charts were used to review progress.

## Contents

| File | Description |
|------|-------------|
| `PES1UG24AM165_Mohammed_Sinan_Jira_Lab2.pdf` | Full submission: epics, stories, screenshots, burndown charts, reflection |
| `README.md` | This summary |

## How it was done

1. **Created the project.** New Scrum project in Jira (Software development, company-managed) named Evaluator-Integrity with key `EE`.
2. **Created Epics.** Grouped the Lab 1 requirements into four themes and created them as Epics in the Backlog.
3. **Wrote User Stories.** Three stories per Epic in the "As a / I want / So that" format, each linked to its Epic as the parent.
4. **Prioritised the backlog.** Set each story to Highest, High or Medium based on user impact and the priority of the requirement it covers, and ordered the backlog accordingly.
5. **Estimated with story points.** Used the Fibonacci scale (3 and 5 points) based on complexity, effort and uncertainty, in the spirit of Planning Poker.
6. **Ran two sprints.** Created EE Sprint 1 and EE Sprint 2 (1-week duration), moved selected stories into each, started the sprint, moved cards To Do → In Progress → Done, then completed the sprint.
7. **Generated burndown charts.** Reports → Burndown Chart for each sprint, using Story Points as the statistic.

## Epics

| Key | Epic | Requirements covered | Stories | Points |
|-----|------|----------------------|---------|--------|
| EE-1 | Epic 1: Similarity Detection | FR-001, NFR-002 | EE-5, EE-6, EE-7 | 13 |
| EE-2 | Epic 2: Integrity Case Management | FR-002 | EE-8, EE-9, EE-10 | 13 |
| EE-3 | Epic 3: Regrade Appeals & Score Revision | FR-003, FR-004 | EE-11, EE-12, EE-13 | 13 |
| EE-4 | Epic 4: Analytics, Export & Privacy | FR-005, NFR-001, NFR-002 | EE-14, EE-15, EE-16 | 13 |

## User Stories, priority, points and sprint

| Key | Story | Epic | Priority | Points | Sprint |
|-----|-------|------|----------|--------|--------|
| EE-5 | Story 1.1: Structural Similarity Scan | EE-1 | Highest | 5 | Sprint 1 |
| EE-6 | Story 1.2: Matched-Fragment Report | EE-1 | High | 3 | Sprint 1 |
| EE-7 | Story 1.3: Background Scan Job | EE-1 | Medium | 5 | Sprint 2 |
| EE-8 | Story 2.1: Open Case with Evidence Pack | EE-2 | Highest | 5 | Sprint 1 |
| EE-9 | Story 2.2: Student Response Window | EE-2 | High | 3 | Sprint 1 |
| EE-10 | Story 2.3: Record Decision with Justification | EE-2 | High | 5 | Sprint 2 |
| EE-11 | Story 3.1: Submit Regrade Request | EE-3 | Highest | 3 | Sprint 1 |
| EE-12 | Story 3.2: Review Appeal Queue | EE-3 | High | 5 | Sprint 1 |
| EE-13 | Story 3.3: Revise Score with History | EE-3 | Medium | 5 | Sprint 2 |
| EE-14 | Story 4.1: Cohort Analytics Dashboard | EE-4 | Medium | 5 | Sprint 2 |
| EE-15 | Story 4.2: CSV Export | EE-4 | Medium | 3 | Sprint 2 |
| EE-16 | Story 4.3: Role-Based Privacy | EE-4 | Highest | 5 | Sprint 1 |

**Total:** 52 points (Sprint 1 = 29, Sprint 2 = 23).

## Sprint summary

| Sprint | Stories | Committed | Completed | Simulated run time |
|--------|---------|-----------|-----------|--------------------|
| EE Sprint 1 | 7 | 29 points | 29 points | 04 Oct 2026, 10:03 PM to 10:18 PM |
| EE Sprint 2 | 5 | 23 points | 23 points | 04 Oct 2026, 10:21 PM to 10:28 PM |

Sprint 1 took every Highest and High story except EE-10, which depends on a case being opened and answered first (EE-8, EE-9). Sprint 2 held the Medium stories that build on Sprint 1, plus EE-10.

## Key takeaways from the reflection

- **Estimates:** Only 3 and 5 were used. EE-7 (background scan job) and EE-14 (analytics dashboard) carry more uncertainty and would likely be 8 points, or be split, in a real project.
- **Prioritisation:** Mostly sound. Priorities follow the requirement table, and dependencies decided the sprint split. All four Epics kept the default Medium priority.
- **Plan vs. actual:** Both sprints finished exactly as planned with no scope added or removed. The sprints were simulated in minutes, so this does not show real delivery.
- **Burndown:** The red line drops far below the guideline almost immediately because of the compressed simulation. It does give a planned velocity of 29 and 23 points per sprint, an average of 26, as a baseline for a real team. Estimates must be entered before a sprint starts for the chart to start at the correct value.

The full written answers are in Section 8 of the PDF.
