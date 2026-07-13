# Technology Decision Register

## Purpose

This register records why a technology or approach is selected, what alternatives were considered, and when the decision should be revisited. The goal is to learn technology selection rather than collect tools without context.

## Decision status

| Status | Meaning |
|---|---|
| Proposed | Candidate decision that has not yet been confirmed |
| Accepted | Current working decision |
| Superseded | Replaced by a later decision |
| Deferred | Intentionally postponed until prerequisites or requirements are clearer |

## TDR-001: Use a separate repository

**Status:** Accepted

**Decision:** Use `production-data-and-ml-systems` as a separate repository from the Telco Customer Churn classification project.

**Reasoning:** The existing churn repository focuses on statistical modelling, model comparison, and evaluation. This repository focuses on databases, data engineering, cloud systems, deployment, and MLOps. Keeping them separate preserves a clear purpose and cleaner portfolio presentation.

## TDR-002: Learn in dependency order

**Status:** Accepted

**Decision:** Follow the phase order defined in the master learning map.

**Reasoning:** Advanced platforms are easier to understand when the simpler problem is already familiar. Airflow should coordinate known tasks, Docker should package a known application, and Azure should provide managed versions of known local capabilities.

## TDR-003: Use PostgreSQL as the primary local relational database

**Status:** Accepted

**Decision:** Use PostgreSQL for the SQL and relational database phase.

**Reasoning:**

- open source
- widely used in professional environments
- supports standard relational concepts and advanced SQL
- provides real client-server database experience
- supports constraints, transactions, indexing, query plans, views, and window functions
- transfers well to other relational systems

**Alternatives considered:**

- SQLite
- MySQL
- Microsoft SQL Server
- DuckDB
- Snowflake

**Why not SQLite as the primary database:** SQLite is valuable, but its embedded architecture does not expose the same client-server, user, connection, and operational concepts.

**Why not Snowflake yet:** Snowflake is primarily an analytical cloud platform. It should be studied after relational and SQL foundations.

**Review trigger:** Revisit when the Azure phase requires a managed database choice.

## TDR-004: Use a telecom-style integrated domain

**Status:** Accepted

**Decision:** Use a simplified telecommunications organization as the consistent domain across phases.

**Reasoning:** The domain naturally includes customers, contracts, invoices, payments, support interactions, usage, and churn. It supports relational modelling, batch pipelines, event streaming, analytical features, and ML use cases.

**Boundary:** Do not copy the existing churn modelling project. Create new operational tables and system-oriented implementations.

## TDR-005: Develop local concepts before cloud equivalents

**Status:** Accepted

**Decision:** Implement storage, pipelines, services, tracking, and monitoring locally before reproducing selected components in Azure.

**Reasoning:** This makes cloud products understandable as managed implementations of known capabilities rather than unexplained interfaces.

## TDR-006: Use Markdown for planning and knowledge notes

**Status:** Accepted

**Decision:** Store roadmaps, coordination documents, glossaries, decisions, and technical knowledge notes as version-controlled Markdown.

**Reasoning:** Markdown is reviewable in Git, readable on GitHub, easy to link, and suitable for code, tables, diagrams, and mathematical notation.

## TDR-007: Explain syntax before relying on it

**Status:** Accepted

**Decision:** Every new keyword, function, operator, symbol, and structural element must be explained before it is used as assumed knowledge.

**Reasoning:** Early SQL discussion showed that examples using `COUNT(*)`, `GROUP BY`, and window functions can become confusing when the individual components have not been established.

## TDR-008: Treat competency as evidence-based

**Status:** Accepted

**Decision:** Track preview, explanation, practice, application, and review separately.

**Reasoning:** Recognition is not mastery. The repository should preserve evidence of independent use and project application.

## TDR-009: Defer the primary database client decision

**Status:** Deferred

**Candidates:**

- DBeaver
- pgAdmin
- a VS Code database extension
- command-line `psql`

**Reason for deferral:** The installation lesson should compare the role of the PostgreSQL server, command-line client, graphical client, and editor integration before selecting the primary workflow.

## TDR-010: Defer cloud service selection details

**Status:** Deferred

**Decision:** Azure is the primary cloud ecosystem to learn, but exact services for deployment and orchestration will be selected after local requirements are known.

**Reasoning:** Choosing services prematurely encourages product memorization and may produce an architecture without a clear workload justification.

## TDR-011: Defer Kubernetes until containers and deployment are understood

**Status:** Accepted

**Decision:** Kubernetes is not an early prerequisite.

**Reasoning:** Kubernetes manages containerized workloads. Docker, APIs, deployment, health checks, and basic cloud operations must be understood first.
