# Day 25 — Microservices Architecture & API Design (Research Notes)

This document contains **only Day 25** research.

Day 26 content is kept separately in [README.md](README.md).

---

## The Senior-Engineer Lens (How this research is framed)

For each topic, I studied it as:

- What problem existed before this?
- Why did the older solution fail at scale?
- What does this solve?
- What new problems does it create?
- Who uses it and why?
- At what scale does it become necessary?

This avoids “tutorial knowledge” and forces practical tradeoff thinking.

---

## 1) Monolith vs Microservices (Problem-First)

### What is a monolith?

A monolith is:

- One backend application
- Usually one database
- One deployment

Analogy: one restaurant kitchen handling billing, cooking, packing, delivery coordination, and support.

### Why monoliths exist (and are often correct early)

Monoliths are usually right for small teams because they are:

- Simple
- Fast to build
- Easy to debug
- Cheap to operate

Premature microservices often create complexity bigger than the business.

### What microservices solve

Microservices help when monolith pain becomes real:

- teams collide in one codebase
- deployments are risky and slow
- scaling everything is expensive

They solve organizational scaling as much as technical scaling.

### What microservices create

Microservices move complexity into distributed systems:

- network latency + timeouts
- partial failures
- retries + idempotency
- distributed tracing becomes mandatory

**Rule:** choose microservices only when monolith pain is bigger than distributed-system pain.

### Practical middle ground: modular monolith

Start with one deployable app, but strong internal modules.

Example modular monolith modules:

| Module | Responsibility |
|---|---|
| Auth Module | login/JWT |
| Resume Module | resume storage/parsing |
| AI Module | resume analysis |
| Job Tracking Module | applications |
| Scheduler Module | interviews |
| Notification Module | reminders |

Later, extract only the modules that truly need independent scaling.

---

## 2) Service Decomposition (Split by Business Capability)

### Biggest beginner mistake

Splitting randomly into tiny services (profile/preferences/images/etc.) creates chaos.

### Correct decomposition

Split by business capability.

Example (food delivery):

| Service | Responsibility |
|---|---|
| User Service | authentication/profile |
| Restaurant Service | menus/restaurants |
| Order Service | order lifecycle |
| Payment Service | payment handling |
| Delivery Service | rider tracking |
| Notification Service | SMS/email/push |

---

## 3) Inter-Service Communication

### REST

- Best for: simplicity, public APIs, frontend communication
- Cost: payload overhead, more requests, slower for high internal throughput

### gRPC

- Best for: internal service-to-service efficiency and typed contracts
- Cost: tooling + harder human debugging

### Message queues / event streaming (Kafka/RabbitMQ/SQS)

Use when workflows should be asynchronous.

Example: order placed should not block on email/analytics/inventory.

Tradeoffs:

- eventual consistency
- duplicate events
- dead-letter queues
- ordering problems

---

## 4) API Gateway Pattern

### Problem

Frontend calling many internal services directly creates coordination and security chaos.

### Solution

Use one gateway as the entry point.

Typical gateway responsibilities:

| Responsibility | Why |
|---|---|
| Authentication | centralized |
| Rate limiting | prevent abuse |
| Routing | simplify clients |
| Logging/metrics | observability |
| Caching | performance |

---

## 5) Service Discovery

In microservices, instances come/go. Hardcoding hostnames breaks.

Service discovery answers: “How does service A find service B right now?”

Common approaches:

- DNS-based discovery
- registry-based discovery
- platform-provided discovery (e.g., Kubernetes service abstraction)

---

## 6) Database-per-Service Pattern

### Problem with a shared database

- tight coupling
- schema conflicts
- coordinated deployments

### Pattern

Each service owns its data boundary.

| Service | Database |
|---|---|
| Auth | users DB |
| Orders | orders DB |
| Payments | payments DB |

---

## 7) REST API Design Best Practices

### Resource naming

- Bad: `/getUsers`, `/createUser`
- Good: `GET /users`, `POST /users`, `DELETE /users/{id}`

### HTTP methods

| Method | Meaning |
|---|---|
| GET | read |
| POST | create |
| PUT | replace |
| PATCH | partial update |
| DELETE | remove |

### Status codes (predictability matters)

| Code | Meaning |
|---|---|
| 200 | success |
| 201 | created |
| 400 | bad request |
| 401 | unauthorized |
| 403 | forbidden |
| 404 | not found |
| 500 | server error |

### Pagination

- Offset: easy, but slow for large datasets
- Cursor: stable and scalable for feeds/infinite scroll

### Versioning

- URL versioning: `/v1/users`
- Header versioning: `Accept: application/vnd.company.v2+json`

---

## Industry Example (Microservices Evolution): Uber

- Early stage: monolith works (speed and coordination)
- Growth: microservices reduce team collision and deployment risk
- Extreme scale: service sprawl creates new pain → domain grouping (DOMA) to reduce chaos

---

## Sources

- Uber microservice architecture / DOMA:
  - https://www.uber.com/blog/microservice-architecture/
  - https://www.uber.com/en-GB/blog/microservice-architecture/
  - https://www.uber.com/en-NG/blog/microservice-architecture/
- AWS API Gateway docs (gateway pattern reference):
  - https://docs.aws.amazon.com/apigateway/
