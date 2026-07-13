# Roadmap: Production Infrastructure

## Objective

Learn how production data and ML services are provisioned, secured, scaled, observed, and recovered.

## Prerequisites

- Docker
- cloud foundations
- deployed services
- CI/CD
- monitoring basics

## Part A: Kubernetes

1. cluster
2. control plane
3. node
4. pod
5. deployment
6. replica
7. service
8. ingress
9. configuration
10. secrets
11. requests and limits
12. health probes
13. autoscaling
14. rolling updates
15. rollback

## Part B: Infrastructure as code

1. declarative configuration
2. desired state
3. provider
4. resource
5. variable
6. output
7. plan
8. apply
9. state
10. remote state
11. modules
12. environments
13. drift
14. review and approval

## Part C: Networking and security

1. IP and ports
2. DNS
3. subnets
4. routing
5. firewalls
6. public and private endpoints
7. TLS
8. identity
9. least privilege
10. secret rotation
11. supply-chain security
12. vulnerability management

## Part D: Observability

1. logs
2. metrics
3. traces
4. correlation identifiers
5. dashboards
6. alerting
7. service-level indicators
8. service-level objectives
9. error budgets
10. incident investigation

## Part E: Reliability

1. failure modes
2. redundancy
3. graceful degradation
4. retries and circuit breakers
5. backups
6. restore testing
7. disaster recovery
8. capacity planning
9. scaling
10. runbooks
11. incident response
12. post-incident review

## Part F: Cost and operations

1. resource sizing
2. idle resources
3. storage lifecycle
4. network costs
5. autoscaling trade-offs
6. budgets and alerts
7. tagging
8. ownership
9. environment cleanup
10. operational documentation

## Practical milestones

- deploy a containerized application to a controlled Kubernetes environment
- configure health probes and resource limits
- perform a rolling update and rollback
- define selected infrastructure with Terraform
- configure logs, metrics, and alerts
- simulate a failure and follow a runbook
- restore data from a tested backup
- document security and cost controls

## Completion criteria

- can explain Kubernetes responsibilities
- can provision reproducible infrastructure
- can secure identities, networks, and secrets
- can diagnose systems through observability
- can plan for failure, recovery, and cost
