# Lab 3: Component Modelling & Architectural Pattern Selection

**Student:** Rishyendra M (PES1UG24AM154) – Section C, AIML
**Scenario:** Problem Statement #02 (Automated Rubric Assignment Evaluator), Test Case 3: Rubric Authoring, Test-Suite Binding & Version Control (from Lab 1)
**Chosen architecture:** Layered (Presentation → Business → Data)

## Files

| File | Description |
|------|-------------|
| `PES1UG24AM154_Lab3_Component_Diagram.png` / `.pdf` | UML component diagram |
| `PES1UG24AM154_Lab3_Component_Diagram.drawio` | Editable draw.io source |
| `PES1UG24AM154_Lab3_Architecture_Justification.pdf` | One-page written justification |

## Components (9)

| Layer | Component |
|-------|-----------|
| Presentation | Rubric Editor UI, Student Rubric Viewer |
| Business | Access Control & API Gateway, **Rubric Authoring Manager** (order manager), Test-Suite Binding & Weight Validator, **Dry-Run Executor** (sandboxed runner), Version Control & Audit Manager |
| Data | Rubric Repository (DB), Test-Suite & Reference Solution Store |

## Interfaces (7, ball = provided, socket = required)

| Interface | Provider | Required by | Technology |
|-----------|----------|-------------|------------|
| IRubricAPI | API Gateway | Rubric Editor UI, Student Viewer | HTTPS / REST (JSON) |
| IRubricAuthoring | Rubric Authoring Manager | API Gateway | internal API call |
| IBindingValidation | Binding & Weight Validator | Rubric Authoring Manager | validate weights & test IDs |
| IDryRun | Dry-Run Executor | Rubric Authoring Manager | async job API |
| IVersioning | Version Control & Audit Manager | Rubric Authoring Manager | publish / lock / clone |
| IRubricStore | Rubric Repository | Version Control & Audit Manager | SQL / JDBC |
| ITestCatalog | Test-Suite & Reference Store | Binding Validator, Dry-Run Executor | file read |

## Style comparison (summary)

| Style | Fit for this scenario |
|-------|-----------------------|
| **Layered (chosen)** | A single transactional data layer makes "validate → bind → dry run → freeze version" all-or-nothing. It matches the small scope and gives one security choke point (the gateway). |
| Microservices | Independent scaling is not needed at this load. Publication would become a distributed transaction across service-owned databases. |
| Client-Server | Simple, but validation, dry-run and versioning logic would be mixed in one server, with no internal separation and a single point of failure. |
