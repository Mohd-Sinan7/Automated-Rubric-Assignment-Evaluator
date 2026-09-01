# Automated-Rubric-Assignment-Evaluator
PES1UG24AM165 CSE_AIML_C Software Engineering Lab 1 — Requirements Engineering &amp; UML Use-Case Modelling. Team project: Automated Rubric Assignment Evaluator. This module covers academic integrity, regrade appeals &amp; cohort analytics.


# Automated Rubric Assignment Evaluator

**PES University — Dept. of CSE**
**Lab 1: Requirements Engineering & UML Use-Case Modelling**
**Problem Statement #02 — Campus & Academic Operations**

## Problem Context

Academic evaluators require an automated workflow to process batch code submissions, execute syntax and test suites, run rubric-based scoring breakdowns, and assign peer reviews without manual distribution overhead.

**Actors:** Student, Faculty Evaluator

## This Module: Academic Integrity, Regrade Appeals & Cohort Analytics

This repository documents my team's assigned subpart of the larger Automated Rubric Assignment Evaluator system — covering plagiarism/similarity detection, integrity case handling, regrade appeals, score revision, and cohort-level analytics.

## Deliverables

- ✅ **Requirements Table** — 5 Functional Requirements (FR-001 to FR-005) + 2 Non-Functional Requirements (NFR-001, NFR-002), each with ID, Type, Description, Priority, Acceptance Criteria, and Rationale
- ✅ **UML Use-Case Diagram** — all actors and primary use cases, including at least one `«include»` and one `«extend»` relationship
- ✅ **Use-Case Flow Specification** — 1-page document for UC-08 (Review Regrade Request), including Preconditions, Postconditions, Main Success Scenario, and one Alternate Flow

## Requirements Summary

| ID | Type | Priority | Summary |
|----|------|----------|---------|
| FR-001 | Similarity Scan | High | Token-level structural similarity scan across cohort and archive |
| FR-002 | Integrity Case Workflow | High | End-to-end case lifecycle: open → evidence → response → decision |
| FR-003 | Regrade Appeal | High | 72-hour window appeal request, routed to evaluator queue |
| FR-004 | Score Revision | Medium | Revises score while retaining prior value and audit reason |
| FR-005 | Cohort Analytics & Export | Medium | Score distribution, pass rates, heat maps, CSV export |
| NFR-001 | Privacy & Access Control | High | Role-based visibility; no cross-student data leakage |
| NFR-002 | Performance & Scalability | Medium | Full cohort scan (500 submissions × 2 offerings) in <15 min |

Full details in [`docs/requirements.md`](./docs/requirements.md) or [`requirements.pdf`](./requirements.pdf).

## Use Case Diagram

Actors: **Student**, **Faculty Evaluator**

Use cases: UC-Request, UC-Respond-Integrity, UC-View-Similarity (Student side); UC-Run-Scan, UC-Open-Case, UC-Generate-Evidence-Pack, UC-Decide-Case, UC-Review-Request, UC-Revise-Score, UC-View-Analytics (Faculty side), linked via `«include»` and `«extend»` relationships.

See [`docs/use-case-diagram.png`](./docs/use-case-diagram.png).

## Use-Case Flow: UC-08 Review Regrade Request

- **Primary Actor:** Faculty Evaluator
- **Secondary Actors:** Student (requester), Notification Service
- **Trigger:** Student submits a regrade request within 72 hours of publication
- **Related Requirements:** FR-003, FR-004, FR-005, NFR-001
- **Extension:** UC-09 Revise Published Score (invoked only when upheld)

Full spec: [`docs/uc-08-review-regrade-request.md`](./docs/uc-08-review-regrade-request.md)

## Repo Structure

\`\`\`
.
├── README.md
├── requirements.pdf
├── docs/
│   ├── requirements.md
│   ├── use-case-diagram.png
│   └── uc-08-review-regrade-request.md
└── LICENSE
\`\`\`

## Team

Mohammed Sinan M T 
PES1UG24AM165
AIML C
