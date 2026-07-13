# Documentation Workflow

## Purpose

This document defines the role of each documentation type and the rules for keeping the repository coherent over a long learning programme.

## Document roles

### `README.md`

Public entry point for the repository.

It should explain:

- the repository purpose
- how it differs from other projects
- the learning scope
- the current phase
- how to navigate the documentation
- the final intended result

It should remain concise relative to the detailed documents.

### `00_master_learning_map.md`

Stable strategic map.

It records:

- major phases
- dependency order
- central questions
- high-level topics
- practical result of each phase
- completion expectations

It should change only when the overall programme changes.

### Topic roadmaps

Detailed plan for one subject area.

Each roadmap should contain:

- prerequisites
- lesson sequence
- practical exercises
- project milestones
- completion criteria
- deferred advanced topics
- connections to other phases

Roadmaps define what remains to be learned. They are not substitutes for knowledge notes.

### `01_current_status_and_next_actions.md`

Tactical source of truth.

It records:

- active phase
- active lesson
- completed setup
- immediate next actions
- current implementation boundary
- deferred subjects

It should be updated frequently.

### `02_progress_and_competency_register.md`

Evidence-based status register.

It distinguishes:

- preview
- introduction
- explanation
- guided practice
- independent practice
- application
- review
- portfolio readiness

A status should not be upgraded without evidence.

### `03_integrated_project_architecture.md`

Evolving architecture of the system being built.

It should explain:

- current implemented architecture
- next planned architecture
- responsibilities of components
- data flow
- non-functional requirements
- boundaries and trade-offs

A diagram should never imply that an unimplemented component already exists.

### `04_technology_decision_register.md`

Record of important choices.

Each entry should include:

- decision
- status
- reasoning
- alternatives
- reason alternatives were not selected
- review trigger where relevant

### `05_glossary.md`

Concise terminology reference.

Definitions should be short and precise. Deep explanations belong in knowledge notes.

### Knowledge notes

Standalone technical explanations of learned material.

Planned structure:

```text
docs/knowledge_notes/
    sql/
    data_modelling/
    pipelines/
    storage/
    orchestration/
    software_delivery/
    mlops/
    cloud/
    distributed_processing/
    streaming/
    infrastructure/
```

Each knowledge note should normally include:

1. purpose and motivation
2. precise definitions
3. intuition
4. every new keyword and symbol
5. small input examples
6. step-by-step execution
7. exact outputs
8. row grain before and after
9. common errors
10. comparisons with earlier tools where useful
11. exercises
12. connection to the integrated project

### Exercises

Exercises should be separated into:

- guided exercises
- partially guided exercises
- independent exercises
- review exercises

Solutions should not be placed where they are accidentally visible before attempting the exercise.

### Implementation files

SQL, Python, configuration, tests, infrastructure definitions, and pipeline code are evidence of application. They should contain enough explanation to remain maintainable, but deep reusable theory belongs in knowledge notes.

## Explanation standard

No syntax is assumed to be self-explanatory.

Before using a new item as known material, explain:

- its name
- its purpose
- its inputs
- its output
- its effect on rows
- its interaction with missing values
- its syntax
- at least one small example

For SQL, explicitly explain:

- keywords
- functions
- operators
- punctuation
- aliases
- parentheses
- execution effect
- result grain

## Example standard

A strong example should show:

1. input table
2. query or code
3. meaning of each new component
4. conceptual execution
5. result table
6. row count before and after
7. row grain before and after
8. potential mistake or alternative

## Progress update workflow

After a lesson:

1. create or update the relevant knowledge note
2. add guided exercises
3. record completed evidence
4. update the competency register
5. update current status and next actions
6. apply the concept to the integrated project when ready
7. commit related changes with a descriptive message

## Repository change discipline

Before modifying existing content:

1. inspect the current repository state
2. read the current file
3. preserve valid existing decisions
4. make the requested change explicitly
5. summarize every meaningful modification
6. avoid silent deletion or restructuring

## Writing style

Documentation should be:

- professional
- precise
- standalone
- technically deep where needed
- explicit about assumptions and limitations
- clear about what has and has not been implemented

Documentation should not:

- refer vaguely to unexplained prior conversations
- present planned work as completed
- use unexplained abbreviations
- copy raw tool output without interpretation
- hide uncertainty
- claim mastery without evidence

## Review and maintenance

At regular milestones:

- check links and navigation
- remove contradictions
- confirm active status
- confirm roadmap order
- verify architecture against implementation
- review deferred decisions
- consolidate repeated definitions
- preserve historical decisions through version control rather than cluttering active documents
