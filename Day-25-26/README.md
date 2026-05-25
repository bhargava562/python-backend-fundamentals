# Days 25–26: Research & Advanced Backend Topics

This README is a **structured, ordered** version of my Days 25–26 learnings.

The key mindset shift:

- Beginners learn **technology-first** (“What is GraphQL/Kubernetes/gRPC?”)
- Senior engineers learn **problem-first** (“What pain exists? What scale exists? What breaks? What slows teams down? What costs money? What hurts users?”)

Technology choices come **after** understanding business pain, scale, and tradeoffs.

---

## Table of Contents

- [Day 25 — Microservices Architecture & API Design](#day-25--microservices-architecture--api-design)
- [Day 26 — Advanced Topics: Alternative API Styles, Trends, Observability, Security](#day-26--advanced-topics-alternative-api-styles-trends-observability-security)
- [Industry Case Studies (Proof of Real-World Research)](#industry-case-studies-proof-of-real-world-research)
- [The 6-Questions Framework (How to Learn Like a Senior Engineer)](#the-6-questions-framework-how-to-learn-like-a-senior-engineer)
- [Comparison Matrices (Templates)](#comparison-matrices-templates)
- [System Design Exercise: Food Delivery (Microservices Breakdown)](#system-design-exercise-food-delivery-microservices-breakdown)
- [Deliverables Checklist](#deliverables-checklist)
- [Sources Mentioned in Notes](#sources-mentioned-in-notes)


## 1) Microservices vs Monolith (Problem-First)

### What is a monolith?

A monolith is:

- **One backend application**
- Usually **one database**
- **One deployment**

Analogy: one restaurant kitchen handling billing, cooking, packing, delivery coordination, and customer support.

### Why monoliths exist (and why they’re often correct early)

Monoliths are often the right starting point because they are:

- Simple
- Fast to build
- Easy to debug
- Cheap to operate
- Great for small teams

If you have “500 users, 2 developers, 1 product”, microservices are usually **complexity bigger than the business**.

### What pain appears as a product grows?

When many teams modify one codebase:

- One deployment can break everything
- Codebase becomes huge
- Deployments slow down
- Scaling the whole app becomes expensive
- Teams collide (organizational friction)

That pain (team + scaling + deployment risk) is what motivates microservices.

### What are microservices?

Instead of one giant app, split into independent services:

- Auth
- Payments
- Notifications
- Search
- AI processing

Each service tends to have:

- Its own deployment
- Its own scaling
- Its own (often dedicated) data storage
- Its own owning team

### What microservices solve (business framing)

| Business pain | Microservices help by |
|---|---|
| Teams collide | making services independently owned |
| Slow deployments | enabling independent deploys |
| Scaling everything is expensive | scaling only hot paths/services |
| One bug kills the app | isolating failure domains |
| Different tech needs | letting teams choose fit-for-purpose tech |

### What microservices *create* (the non-negotiable cost)

Microservices don’t remove complexity; they **move** it.

- Monolith complexity: mostly **code complexity**
- Microservice complexity: **network + distributed systems complexity**

Instead of a function call you get:

- Network latency
- Timeouts
- Partial failures
- Retries + duplicate requests
- Serialization overhead
- Observability requirements (tracing becomes mandatory)

### Senior engineer rule

Never choose microservices because they sound modern.

Choose them only when **monolith pain becomes bigger than distributed-system pain**.

### Practical middle-ground: modular monolith

A pattern that shows up in real startups:

- One deployable app
- Internally organized by strong modules/domains
- Later, extract the modules that truly need independent scaling

Example modular monolith for an AI job platform:

| Module | Responsibility |
|---|---|
| Auth Module | login/JWT |
| Resume Module | resume storage/parsing |
| AI Module | resume analysis |
| Job Tracking Module | applications |
| Scheduler Module | interviews |
| Notification Module | reminders |

---

## 2) Service Decomposition (Split by Business Capability)

### Biggest beginner mistake

Splitting “randomly” into tiny services like `UserService`, `UserProfileService`, `UserPreferenceService`, `UserImageService` creates chaos.

### Correct thinking

Split by **business capability**.

Example: Food delivery domains

| Service | Responsibility |
|---|---|
| User Service | authentication/profile |
| Restaurant Service | menus/restaurants |
| Order Service | order lifecycle |
| Payment Service | payment handling |
| Delivery Service | rider tracking |
| Notification Service | SMS/email/push |

Each service should own **one domain** and have clear boundaries.

---

## 3) Inter-Service Communication

When services are split, they must communicate.

### Option A — REST (HTTP + JSON)

Good for:

- Simplicity
- Public APIs
- Frontend-to-backend communication

Tradeoffs:

- Larger payloads
- Repeated requests
- Slower for high-throughput internal calls

### Option B — gRPC (binary + strongly typed)

Good for:

- Internal service-to-service communication at scale
- High request volume (e.g., 10,000 calls/sec)
- Lower latency and smaller payloads

Tradeoffs:

- Harder to debug manually
- Browser usage is not as straightforward as REST
- Requires IDL/tooling discipline (protobuf)

### Option C — Message queues / event streaming (Kafka/RabbitMQ/SQS)

Use when “do this now” becomes “publish an event, process later”.

Why it matters (order placement example): you shouldn’t block the user response while waiting for payment, email, analytics, inventory, delivery allocation.

Instead:

- Create order (fast)
- Publish `OrderCreated`
- Other services react asynchronously

Tradeoffs:

- Eventual consistency
- Duplicate events (retries)
- Dead-letter queues
- Ordering guarantees are hard

---

## 4) API Gateway Pattern

### Problem

Frontend should not call 20 internal services directly.

### Solution

Frontend calls **one** API gateway. The gateway routes internally.

Common gateway responsibilities:

| Responsibility | Why |
|---|---|
| Authentication | centralized |
| Rate limiting | prevent abuse |
| Routing | simplify client |
| Logging/metrics | observability |
| Caching | performance |

Gateway is not “magic”; it’s a coordination tool that reduces frontend-backend integration chaos.

---

## 5) Service Discovery (Research Topic)

### Problem

In microservices, instances scale up/down. Hardcoding hostnames breaks quickly.

### Goal

Service discovery answers: **“How does service A find service B right now?”**

Common approaches:

- DNS-based discovery (simple)
- Registry-based discovery (services register themselves)
- Platform-provided discovery (Kubernetes service abstraction)

Key tradeoff: more dynamic systems reduce manual config but increase operational complexity.

---

## 6) Database-per-Service Pattern

### Beginner thought

“One giant database shared by all services.”

### Problem

- Tight coupling
- Schema conflicts
- Coordinated deployments
- One schema change breaks multiple teams

### Correct pattern

Each service owns its database or schema boundary.

| Service | Database |
|---|---|
| Auth | users DB |
| Orders | orders DB |
| Payments | payments DB |

Reason: independent evolution and scaling, and better ownership.

---

## 7) REST API Design Best Practices

### Resource naming

Avoid verb-based endpoints:

- Bad: `GET /getUsers`, `POST /createUser`
- Good: `GET /users`, `POST /users`, `DELETE /users/{id}`

HTTP method already encodes the action.

### Proper HTTP methods

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

### Filtering + sorting (query params)

Common patterns:

- `GET /jobs?status=open&location=blr`
- `GET /jobs?sort=-createdAt` (descending) or `sort=createdAt`

Keep filters consistent, well-documented, and predictable.

### Pagination

Offset pagination:

- Example: `GET /applications?page=2&limit=20`
- Pros: easy
- Cons: slow/unstable for very large datasets

Cursor pagination:

- Example: `GET /applications?after=job_9281&limit=20`
- Pros: faster at scale, stable for infinite scroll
- Cons: requires cursor design and careful ordering

### API versioning (URL vs header)

- URL versioning: `/v1/users`
  - Pros: explicit, easy to debug
  - Cons: can create version sprawl
- Header-based versioning (e.g., `Accept: application/vnd.company.v2+json`)
  - Pros: cleaner URLs
  - Cons: harder to inspect/debug, tooling-dependent

Main rule: version when you must break clients; avoid unnecessary churn.

### HATEOAS (concept)

HATEOAS is the idea that API responses include links/actions that describe valid next steps.

In practice:

- It can improve discoverability
- Many teams do not implement it fully due to complexity

---

# Industry Case Studies (Proof of Real-World Research)

This section highlights **industry examples** to show the “senior engineer” learning approach:

- What problem existed?
- Why did the older approach fail at scale?
- What did the new solution solve?
- What new problems did it introduce?
- Who uses it and under what conditions?

These examples are intentionally chosen from companies that publish engineering learnings publicly.

## Uber — Monolith → Microservices → “Microservices Chaos” → Domains (DOMA)

- Problem: rapid growth (more cities, more traffic, more engineers) made a single codebase risky and slow
- Why monolith struggled: deploy risk + scaling waste + team collisions
- What microservices solved: service ownership + independent deploys + domain scaling
- New problems created: service sprawl, dependency complexity, debugging difficulty without tracing
- Industry takeaway: microservices are as much about **organizational scaling** as technical scaling

## Meta (Facebook) — Why GraphQL exists

- Problem: REST often caused overfetching/underfetching, especially painful for mobile clients and fast-evolving UIs
- What GraphQL solved: client requests exactly the fields it needs, reducing waste and improving developer velocity for frontend teams
- New problems created: caching becomes harder, query cost control is required, backend complexity increases (resolvers, tracing)
- Industry takeaway: GraphQL is often a **frontend productivity** solution, not a “REST replacement” for all systems

## Google — Why gRPC and reliability discipline matter

- Problem: high-throughput internal service-to-service communication needs strong contracts and efficiency
- What gRPC solved: smaller payloads, lower latency, typed contracts for internal APIs
- New problems created: more tooling, harder human-debuggability, contract/versioning discipline becomes mandatory
- Reliability lens: large-scale systems require systematic reliability practices (SLIs/SLOs, incident response, automation)

## Netflix — Observability becomes mandatory in distributed systems

- Problem: when a single user request crosses many services, “where did it fail?” becomes hard
- What observability solved: logs + metrics + tracing make failures diagnosable and performance measurable
- New problems created: data volume/cost, instrumentation effort, alert fatigue if done poorly
- Industry takeaway: microservices without observability is a production failure waiting to happen

## Amazon — Service-oriented thinking and gateway patterns

- Problem: many teams + many capabilities → clients cannot coordinate dozens of internal services directly
- What gateway layers solve: one entry point, centralized auth/rate limits, consistent policies, simplified client integration
- New problems created: gateways can become bottlenecks and need careful scalability and governance
- Organizational angle: “two-pizza team” style ownership reinforces domain boundaries and API contracts

## Instagram — “Start simple, then evolve” (startup reality)

- Problem: early-stage product needs speed; perfect architecture is less valuable than shipping
- Common evolution: start with a monolith/modular monolith, then optimize hotspots (caching, async processing, read scaling)
- Industry takeaway: early correctness is often “simple + maintainable,” not “distributed + modern”

## Swiggy / Zomato — ETA and realtime logistics are business-critical

- Problem: ETA accuracy affects trust, cancellations, and support load
- Why the naive model fails: ETA is not `distance / speed`; real-world factors dominate
- What modern systems use: realtime tracking, historical data, event streams, prediction models
- New problems created: partial failures, noisy data, non-determinism, user perception when ETAs jump

---

# Day 26 — Advanced Topics: Alternative API Styles, Trends, Observability, Security

## 1) Alternative API Styles (When to use each)

### REST

Best default for:

- Public APIs
- Simple CRUD
- Broad client compatibility

### GraphQL

Why it exists:

- REST can cause overfetching/underfetching
- Mobile/frontends often need field-level flexibility

Benefits:

- Client can request exactly the fields needed

Costs:

- Caching becomes harder
- Backend complexity grows (resolvers, query planning)
- Dangerous queries are possible (needs query depth/complexity controls)

### gRPC

Best for:

- High-throughput internal calls
- Strong typing + contracts between services

### WebSockets vs SSE

Normal HTTP is request → response → closed.

When you need realtime:

- WebSockets: two-way realtime (chat, multiplayer games, collaborative tools)
- SSE (Server-Sent Events): one-way server push (notifications, dashboards, streaming responses)

WebSockets tradeoffs:

- Millions of open connections cost memory
- Reconnect handling is hard on mobile networks
- Load balancing often needs sticky sessions/connection affinity

SSE tradeoffs:

- One-way only
- Still requires connection management, but simpler than WebSockets

---

## 2) Emerging Backend Trends (Research Topics)

### Serverless architecture

- Why it exists: infrastructure management is painful; teams want faster deployment and autoscaling
- Tradeoffs: cold starts, vendor lock-in, observability and debugging complexity

### Edge computing

- Why it exists: reduce latency by running code closer to users
- Tradeoffs: distributed runtime limitations, state/data consistency challenges

### JAMstack

- Why it exists: push work to CDN/static + call APIs for dynamic pieces
- Tradeoffs: backend still exists (APIs), auth and dynamic workflows require careful design

### Backend-as-a-Service (BaaS)

- Why it exists: speed for prototypes/teams that don’t want to build everything
- Tradeoffs: platform constraints, lock-in, cost at scale

### Low-code / no-code backends

- Why it exists: faster internal tools
- Tradeoffs: limited control, performance constraints, security/governance risks

---

## 3) Observability (Logging vs Monitoring vs Tracing)

Observability becomes mandatory as systems distribute.

### Logging

Records events:

- “User login failed”
- “Payment timeout”

### Monitoring

Tracks system health:

- CPU/memory
- request rate
- error rate
- latency

### Tracing (distributed tracing)

Tracks a single request across services:

Frontend → Gateway → Order → Payment → Notification

### APM + metrics + alerting (research targets)

- APM (Application Performance Monitoring): helps detect slow transactions, errors, bottlenecks
- Metrics collection: consistent measurements for SLO/SLA thinking
- Alerting strategies:
  - alert on symptoms (error rate/latency) not just on CPU
  - avoid noisy alerts; route to the right owner

Without observability, production failures become “system failing, nobody knows where”.

---

## 4) Security Deep Dive

### OWASP Top 10 (high-level)

OWASP publishes the most common web app risk categories. A practical “memorize the names” list (keep it high-level; the real skill is applying it):

- Broken access control
- Cryptographic failures (sensitive data exposure, weak encryption)
- Injection (SQL/NoSQL/command injection, etc.)
- Insecure design
- Security misconfiguration
- Vulnerable and outdated components
- Identification and authentication failures
- Software and data integrity failures (supply chain, unsafe deserialization patterns)
- Security logging and monitoring failures
- Server-Side Request Forgery (SSRF)

### API security best practices (practical checklist)

- Strong authentication and authorization (principle of least privilege)
- Input validation + safe query practices
- Rate limiting + abuse detection
- Use TLS everywhere
- Secure defaults; don’t leak internal errors
- Audit logs for security events

### Zero Trust architecture

Assumption: trust nobody automatically; verify everything.

Even internal services should authenticate/authorize calls.

### Secret management

- Bad: hardcoding secrets in source code
- Better: environment variables
- Best at scale: secret managers / vault systems

### Penetration testing basics (research goal)

- Understand how attackers think (threat modeling)
- Test auth boundaries, input validation, and common misconfigurations
- Learn safe tooling and responsible testing practices

---

## 5) Caching & Redis (Why it exists + what makes it hard)

### Why caching becomes necessary

At scale, databases become bottlenecks.

Example scenario:

- Homepage loads millions of times/day
- Hitting PostgreSQL on every request becomes expensive and increases latency

### Redis (typical uses)

Redis is commonly used for:

- Sessions
- Caching hot data
- Rate limiting counters
- Temporary state / coordination

### The hardest part: cache invalidation

Caching is easy.

Keeping cache correct is hard.

Classic failure mode:

- Job/application status changes
- Cache still serves old data
- Users see stale information (real business bug)

This is why “cache invalidation” is considered one of the hardest practical problems in backend engineering.

---

## 6) Realtime at Scale: Polling vs WebSockets (WhatsApp-style lens)

Most tutorials stop at: “WebSockets are realtime.”

The more useful question is: **why polling fails at scale**.

If a chat app used polling ("Any new message?") every few seconds:

- bandwidth waste (requests even when nothing changed)
- server overload (infrastructure cost)
- battery drain (bad mobile UX)
- delayed messages (poor realtime feel)

WebSockets solve this with a persistent connection, but introduce new pain:

- millions of open connections (memory pressure)
- reconnect handling (mobile networks are unstable)
- load balancing complexity (often needs connection affinity)

---

## 7) ETA Systems (Swiggy/Uber-style delivery thinking)

ETA is not just engineering; it’s business-critical.

### Why ETA matters

Accurate ETA impacts:

- user trust
- cancellations
- support tickets
- retention

### Why ETA is hard

ETA is not simply `distance / speed`.

Real factors include:

- restaurant preparation time
- rider availability / assignment delay
- traffic congestion
- rain/weather
- apartment security/waiting time
- batching (one rider delivering multiple orders)
- festivals/high demand periods

### What real systems use

- realtime GPS
- historical delivery data
- traffic APIs
- ML prediction models
- event streams for live updates

---

## 8) Microservices at Extreme Scale: Uber → “Microservices Chaos” → DOMA

Architecture evolves; it doesn’t appear magically.

### Phase 1: monolith (early Uber)

When the team and user base are small, a monolith is effective:

- one deployable app
- one primary database
- faster iteration

### Phase 2: microservices (growth)

As Uber scaled globally (more engineers, more traffic, more product surface area), the monolith pain increased:

- deployment risk (one change can break unrelated flows)
- team collisions (many teams editing shared systems)
- scaling waste (scale everything even if only one domain is hot)

So services were split by business domains (trip, pricing, matching, payments, notifications, maps, fraud, ETA, etc.).

### Phase 3: thousands of services create new pain

At very high service counts, new distributed-systems chaos appears:

- unclear ownership (“who owns what?”)
- dependency explosion (“who calls whom?”)
- debugging failures without tracing becomes a nightmare
- operational overhead increases significantly

### DOMA (Domain-Oriented Microservice Architecture)

Uber describes grouping services into domains to reduce chaos and improve clarity/ownership.

Key lesson:

- microservices solve **organizational scaling** as much as technical scaling
- no architecture is final—each solves one pain while creating another

---

## 9) How Senior Engineers Estimate Systems (before choosing architecture)

Before tools, ask scale questions:

- How many users?
- Peak requests/sec? (not average)
- Realtime needed?
- Latency requirements?
- Storage growth over time?
- Failure tolerance? (what must never fail?)
- Cost constraints? (especially for AI workloads)

Simple rule-of-thumb framing:

- Small startup: modular monolith + PostgreSQL + Redis + REST can be “enough”
- Large scale: microservices + queues/streams + gRPC + distributed tracing + multi-database patterns become more reasonable

Interview maturity signal:

- not “Explain Kubernetes deeply”
- but “What tradeoffs exist, and at what scale do they matter?”

---

# The 6-Questions Framework (How to Learn Like a Senior Engineer)

For every backend concept, ask:

| Question | What it forces you to learn |
|---|---|
| What problem existed before this? | origin pain |
| Why did the older solution fail? | limitation |
| What does this solve? | benefit |
| What new problems does it create? | tradeoff |
| Which companies use this and why? | practical reality |
| At what scale does it become necessary? | engineering judgment |

This converts “definitions” into real-world engineering thinking.

---

# Comparison Matrices (Templates)

These were part of the original deliverables; templates below make it easier to fill in.

## 1) Monolith vs Microservices

| Dimension | Monolith | Microservices |
|---|---|---|
| Team size fit | small | medium/large |
| Deployment risk | one deploy affects all | isolated deploys |
| Scaling | scale whole app | scale per service |
| Complexity location | inside codebase | in the network + ops |
| Debuggability | simpler | harder without tracing |

## 2) REST vs GraphQL vs gRPC

| Dimension | REST | GraphQL | gRPC |
|---|---|---|---|
| Best for | public APIs, CRUD | frontend flexibility | internal high-throughput |
| Human debuggable | yes | medium | low |
| Caching | straightforward | harder | depends on tooling |
| Contract strictness | medium | schema-based | strong (proto) |
| Common risks | overfetching | expensive queries | tooling complexity |

## 3) SQL vs NoSQL (scenario-based)

| Need | Often fits |
|---|---|
| Strong consistency + relational queries | SQL |
| Flexible schema + horizontal scaling patterns | NoSQL |

## 4) Authentication methods

| Method | Typical use |
|---|---|
| Sessions | web apps with server-side session state |
| JWT | stateless APIs, mobile apps |
| OAuth2/OIDC | third-party login + delegated access |

---

# System Design Exercise: Food Delivery (Microservices Breakdown)

This exercise was explicitly part of the original task. The goal is not drawing boxes—it’s defining **boundaries, data, and contracts**.

## 1) Choose service boundaries (business capabilities)

Suggested starting set:

- User Service
- Restaurant Service
- Order Service
- Payment Service
- Delivery Service
- Notification Service

## 2) Data strategy (database-per-service)

- Each service owns its data
- Cross-service reads happen via APIs or events (not direct DB access)

## 3) API contracts (examples)

### Order service (REST)

- `POST /orders` (create order)
- `GET /orders/{id}` (retrieve)

### Event flow (async)

- Order Service publishes `OrderCreated`
- Payment Service consumes → publishes `PaymentAuthorized` or `PaymentFailed`
- Notification Service consumes and sends updates

## 4) Operational requirements

- API Gateway in front
- Observability (logs + metrics + tracing) from day 1 if it’s distributed
- Security (auth, rate limits, secrets) as a design constraint, not an afterthought

---

# Deliverables Checklist

From the original Days 25–26 deliverables list:

- Research presentation on microservices
- API design best practices document
- System architecture design for a complex application (e.g., food delivery)
- Comparison matrices for different technologies
- Trend analysis report
- Security checklist for APIs
- README summarizing learnings (this file)

---

# Sources Mentioned in Notes

These links were referenced in the original notes (kept here as a bibliography). Some include community discussion threads.

- Uber engineering blog on microservice architecture / DOMA:
  - https://www.uber.com/blog/microservice-architecture/
  - https://www.uber.com/en-GB/blog/microservice-architecture/
  - https://www.uber.com/en-NG/blog/microservice-architecture/
- GraphQL (origin + concepts):
  - https://graphql.org/
- gRPC (concepts + tooling):
  - https://grpc.io/
- Google SRE (reliability mindset + practices):
  - https://sre.google/books/
- Netflix engineering (distributed systems + observability patterns):
  - https://netflixtechblog.com/
- AWS API Gateway (gateway pattern reference):
  - https://docs.aws.amazon.com/apigateway/
- Community discussions (used as “what people observe in the wild”):
  - https://www.reddit.com/r/SoftwareEngineering/comments/1t57wzy/microservices_for_everything_trend_almost_killed/
  - https://www.reddit.com/r/developersIndia/comments/189xz1d/
  - https://www.reddit.com/r/swiggy/comments/1puo49o/swiggys_eta_calculation_is_laughable/
- Observability talk referenced:
  - https://www.youtube.com/watch?v=uYDciwTJJiI
