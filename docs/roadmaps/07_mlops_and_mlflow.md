# Roadmap: MLOps and MLflow

## Objective

Manage the complete machine-learning lifecycle with reproducibility, traceability, deployment control, and monitoring.

## Prerequisites

- machine-learning development
- Python software engineering
- APIs and Docker
- data pipelines
- testing
- Git

## Part A: MLOps foundations

1. difference between model development and model operations
2. reproducibility
3. lineage
4. environments
5. artifacts
6. validation gates
7. deployment
8. monitoring
9. retraining
10. governance

## Part B: Experiment tracking

1. run
2. parameter
3. metric
4. tag
5. artifact
6. source version
7. dataset reference
8. comparison
9. nested runs
10. search and organization

## Part C: MLflow

1. tracking server
2. backend store
3. artifact store
4. autologging and explicit logging
5. model packaging
6. signatures
7. input examples
8. model registry
9. aliases or lifecycle labels
10. serving and integrations

## Part D: Model validation and promotion

1. candidate generation
2. offline evaluation
3. acceptance criteria
4. data checks
5. fairness and subgroup checks where relevant
6. reproducibility checks
7. approval
8. staging
9. production
10. rollback

## Part E: Inference operations

1. batch inference
2. online inference
3. feature consistency
4. request logging
5. prediction storage
6. latency and throughput
7. failure behavior
8. model version reporting

## Part F: Monitoring

1. service health
2. data quality
3. feature drift
4. prediction drift
5. concept drift
6. delayed labels
7. performance estimation
8. alerts
9. retraining triggers
10. human review

## Part G: Retraining and governance

1. scheduled retraining
2. event-triggered retraining
3. champion and challenger
4. reproducible datasets
5. audit trail
6. approvals
7. rollback
8. retirement
9. retention
10. documentation

## Practical milestones

- track model experiments with MLflow
- store parameters, metrics, and artifacts
- package and register a model
- validate a model before promotion
- serve or batch-score a registered version
- log prediction metadata
- implement basic drift reports
- document retraining and rollback procedures

## Completion criteria

- can explain the ML lifecycle beyond training
- can reproduce a run from recorded evidence
- can manage model versions and promotion
- can monitor operational and statistical behavior
- can design safe retraining and rollback workflows
