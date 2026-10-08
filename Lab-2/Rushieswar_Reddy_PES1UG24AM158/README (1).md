# Automated Rubric Assignment Evaluator
> Lab 1 — Requirements Engineering & UML Use-Case Modelling
> PES University, Dept. of CSE

## Overview
An automated evaluation workflow for academic code submissions — batch-processes 
student project uploads, runs syntax checks and unit test suites, generates 
rubric-based score breakdowns, and handles peer review assignment without manual 
distribution overhead.

**Actors:** Student, Faculty Evaluator

## Contents
| File | Description |
|---|---|
| `requirements.md` | 5 FRs (FR-001–FR-005) + 2 NFRs (NFR-001, NFR-002) |
| `use-case-diagram.png` | UML use-case diagram with actors, use cases, `<<include>>` & `<<extend>>` |
| `use-case-flow.md` | Detailed flow spec for core use case — preconditions, postconditions, main + alternate flow |

## Key Use Cases
- Submit Project (Student)
- Run Test Suite `<<include>>`
- Generate Rubric Score
- Request Manual Re-evaluation `<<extend>>`
- Assign Peer Review (Faculty Evaluator)

## Tech/Modelling Notes
- Requirements follow standard FR/NFR template: ID, Priority/Type, Description, 
  Acceptance Criteria, Rationale
- NFRs cover performance (100 concurrent submissions, <1.5GB memory) and security
