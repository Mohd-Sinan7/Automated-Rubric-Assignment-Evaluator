# Automated Rubric Assignment Evaluator

**PES University — Dept. of CSE**
**Lab 1: Requirements Engineering & UML Use-Case Modelling**
**Problem Statement #02 · Campus & Academic Operations**

---

## 📖 Problem Context

Academic evaluators require an automated workflow to process batch code submissions, execute syntax and test suites, run rubric-based scoring breakdowns, and assign peer reviews without manual distribution overhead.

**Actors:** Student · Faculty Evaluator

---

## 🧩 My Contribution

This was a team lab assignment. My part covers the **Academic Integrity, Regrade Appeals & Cohort Analytics** module of the larger Automated Rubric Assignment Evaluator system. I authored:

- The complete Requirements Table for this module (5 FRs + 2 NFRs)
- The UML Use-Case Diagram for this module
- The full Use-Case Flow Specification for **UC-08: Review Regrade Request**

📄 All three deliverables are combined in **[`PES1UG24AM165_Mohammed_Sinan.pdf`](./PES1UG24AM165_Mohammed_Sinan.pdf)**.

---

## ✅ Deliverables

| Deliverable | Status |
|---|---|
| Requirements Table — 5 FRs (FR-001–FR-005) + 2 NFRs (NFR-001, NFR-002) | ✅ |
| UML Use-Case Diagram — actors, use cases, `«include»` & `«extend»` | ✅ |
| Use-Case Flow Spec — UC-08, with Preconditions, Postconditions, Main Flow, Alternate Flow | ✅ |

---

## 📋 Requirements Table

| ID | Type | Priority | Description |
|---|---|---|---|
| **FR-001** | Similarity Scan | High | Token-level structural similarity scan of every submission against the cohort and the archive of previous offerings, producing a similarity % and matched-fragment report. |
| **FR-002** | Integrity Case Workflow | High | Faculty Evaluator opens an integrity case from a flagged pair, attaches an auto-assembled evidence pack, notifies students, accepts a written response, and records a justified decision. |
| **FR-003** | Regrade Appeal | High | Accepts a regrade request from a Student within 72 hours of publication, routes it to the Faculty Evaluator queue, and records the outcome. |
| **FR-004** | Score Revision | Medium | On an upheld appeal/integrity decision, revises the published score while retaining the previous value, reason, and deciding evaluator. |
| **FR-005** | Cohort Analytics & Export | Medium | Presents score distribution, criterion-wise mean/pass rate, and a test-failure heat map; exports results, outcomes, and audit log as CSV. |
| **NFR-001** | Privacy & Access Control | High | Similarity reports, cases, and analytics are visible in identified form only to Faculty Evaluators; Students see only their own data. |
| **NFR-002** | Performance & Scalability | Medium | Full cross-cohort similarity scan (500 submissions × 2 prior offerings) completes within 15 minutes as a background job; analytics queries return within 5s. |

*Full acceptance criteria and rationale for each requirement are in [`PES1UG24AM165_Mohammed_Sinan.pdf`](./PES1UG24AM165_Mohammed_Sinan.pdf).*

---

## 🗺️ Use-Case Diagram

**Actors:** Student · Faculty Evaluator

- **Student:** UC-Request, UC-Respond-Integrity, UC-View-Similarity
- **Faculty Evaluator:** UC-Run-Scan, UC-Open-Case, UC-Generate-Evidence-Pack, UC-Decide-Case, UC-Review-Request, UC-Revise-Score, UC-View-Analytics

Connected via `«include»` (e.g., Open Case includes Generate Evidence Pack) and `«extend»` (e.g., Review Request extends to Revise Score) relationships.

---

## 🔄 Use-Case Flow: UC-08 — Review Regrade Request

| Field | Detail |
|---|---|
| **Primary Actor** | Faculty Evaluator |
| **Secondary Actors** | Student (requester), Notification Service |
| **Trigger** | Student submits a regrade request within 72 hours of publication |
| **Related Requirements** | FR-003, FR-004, FR-005, NFR-001 |
| **Extension** | UC-09 Revise Published Score — invoked only when the request is upheld |

**Main Success Scenario (summary):** Faculty Evaluator reviews the disputed criteria against the original rubric, evidence, and logs → records a per-criterion outcome → system recomputes the total, retains score history, notifies the student, and refreshes analytics/exports.

**Alternate Flow (A1):** If the evaluator discovers the dispute stems from a cohort-wide defect (a broken test case or rubric weight), the request is escalated to a cohort-level correction — all affected submissions are re-evaluated and every affected student is notified.

Full step-by-step flow is in [`PES1UG24AM165_Mohammed_Sinan.pdf`](./PES1UG24AM165_Mohammed_Sinan.pdf).


Mohammed Sinan M T 
PES1UG24AM165
AIML C
