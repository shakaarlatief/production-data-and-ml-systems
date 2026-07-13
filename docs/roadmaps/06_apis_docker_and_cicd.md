# Roadmap: APIs, Docker, and CI/CD

## Objective

Turn local Python logic into tested, reproducible, deployable batch applications and online services.

## Prerequisites

- modular Python
- Git
- basic command line
- working data or ML application

## Part A: Software engineering foundations

1. package structure
2. modules and imports
3. configuration
4. environment variables
5. logging
6. exceptions
7. type hints
8. dependency management
9. command-line interfaces
10. testing strategy

## Part B: APIs

1. client and server
2. HTTP
3. methods
4. URL and route
5. headers
6. request body
7. response body
8. status codes
9. JSON
10. REST concepts
11. FastAPI
12. request validation
13. response schemas
14. errors
15. API documentation

## Part C: Inference patterns

1. batch job
2. synchronous online request
3. asynchronous processing
4. latency
5. throughput
6. concurrency
7. input validation
8. model loading
9. health checks
10. versioning

## Part D: Docker

1. image
2. container
3. Dockerfile
4. build context
5. layers
6. base image
7. working directory
8. copying files
9. installing dependencies
10. command and entrypoint
11. ports
12. volumes
13. networks
14. Docker Compose
15. security and image size

## Part E: Continuous integration

1. trigger
2. job
3. step
4. runner
5. test automation
6. linting
7. type checking
8. build checks
9. secrets
10. artifacts
11. GitHub Actions

## Part F: Delivery and deployment

1. versioned artifacts
2. container registry
3. staging and production
4. deployment gates
5. smoke tests
6. rollback
7. continuous delivery versus continuous deployment

## Practical milestones

- convert pipeline code into an installable package
- build a FastAPI prediction service
- add unit and integration tests
- containerize the API
- run PostgreSQL and the API with Docker Compose
- create GitHub Actions checks
- build a versioned Docker image

## Completion criteria

- can explain HTTP and API behavior
- can build and test a FastAPI service
- can create and debug Docker images
- can automate validation in CI
- can describe a safe delivery and rollback process
