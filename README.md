# Python Backend Fundamentals

A structured, hands-on backend engineering repository built day by day, covering Python fundamentals, SQL, FastAPI, Django, authentication, API design, and production-style backend patterns.

## Current Coverage

- Core Python and OOP fundamentals
- SQL schema design and query practice
- FastAPI from basics to production-style modules
- Authentication and authorization patterns
- Django fundamentals with DRF
- Side-by-side FastAPI vs Django API implementation and comparison
- Advanced backend patterns: containerization, async programming, caching, task queues
- Production-ready microservices and deployment strategies

## Repository Structure

python-backend-fundamentals/

- Day-1: Python core foundations (OOP, decorators, type hints, exceptions)
- Day-2: Git fundamentals and workflow cheat sheets
- Day-3: SQL schema, joins, normalization, transactions
- Day-4: FastAPI basics and initial API testing
- Day-5: Pydantic validation patterns
- Day-6: SQLAlchemy and advanced CRUD patterns
- Day-7: JWT authentication workflows
- Day-8: OAuth and security-focused API design
- Day-9: FastAPI with MongoDB and async data access
- Day-10: Error handling, logging, and debugging patterns
- Day-11-13: Production-style e-commerce API (FastAPI + PostgreSQL)
- Day-14-17: Django fundamentals and DRF progression
- Day-16: DRF JWT auth and permission system module
- Day-17: Same Task Manager API implemented in both FastAPI and Django with benchmark comparison
- Day-18: Docker containerization and deployment strategies
- Day-19: Redis caching and real-time operations
- Day-20: Celery task queues and async job processing
- Day-21: Asynchronous programming in FastAPI (performance-optimized backends)

## Progress Tracker

| Day/Module | Focus Area | Status |
|---|---|---|
| [Day-1](./Day-1/README.md) | Python OOP, decorators, typing, context managers | Complete |
| [Day-2](./Day-2/README.md) | Git setup, branching, stashing, commit conventions | Complete |
| [Day-3](./Day-3/README.md) | SQL design, joins, advanced queries, transactions | Complete |
| [Day-4](./Day-4/README.md) | FastAPI CRUD and API testing foundations | Complete |
| [Day-5](./Day-5/README.md) | Pydantic v2 validation and model design | Complete |
| [Day-6](./Day-6/README.md) | SQLAlchemy ORM and service-style CRUD | Complete |
| [Day-7](./Day-7/README.md) | JWT auth and protected route design | Complete |
| [Day-8](./Day-8/README.md) | OAuth integration and API security hardening | Complete |
| [Day-9](./Day-9/README.md) | MongoDB integration with FastAPI | Complete |
| [Day-10](./Day-10/README.md) | Logging, error handling, observability basics | Complete |
| [Day-11-13](./Day-11-13/README.md) | E-commerce backend with PostgreSQL and modular architecture | Complete |
| [Day-14-17](./Day-14-17/README.md) | Django fundamentals, MVT, DRF ViewSets, routers | Complete |
| [Day-16](./Day-16/README.md) | DRF JWT identity management and permissions | Complete |
| [Day-17](./Day-17/README.md) | FastAPI vs Django Task Manager API with metrics and recommendations | Complete |
| [Day-18](./Day-18/README.md) | Docker containerization and deployment practices | Complete |
| [Day-19](./Day-19/README.md) | Redis caching and real-time data operations | Complete |
| [Day-20](./Day-20/README.md) | Celery task queues and async job processing | Complete |
| [Day-21](./Day-21/README.md) | Asynchronous programming in FastAPI (4.9x-50x performance improvement) | ✅ Complete |

## Latest Updates

### Day-21 Highlight: Asynchronous Programming in FastAPI ⚡

[Day-21](./Day-21/README.md) is a comprehensive, production-ready async programming implementation:

- **9 async endpoints** demonstrating concurrent patterns
- **4.9x-96x performance improvement** (verified testing)
- **AsyncDatabase class** with proper lifecycle management
- **WebSocket support** for real-time communication
- **Error handling** with `return_exceptions=True` pattern
- **Load testing framework** for performance benchmarking
- **1200+ lines** comprehensive documentation

**Key Achievement**: Building backends that handle 50x more concurrent users through asynchronous programming.

### Day-17-20 Advanced Patterns Track

[Day-17](./Day-17/README.md) through [Day-20](./Day-20/README.md) represent production-ready patterns:

- **Day-17**: FastAPI vs Django framework comparison
- **Day-18**: Docker containerization and deployment
- **Day-19**: Redis caching and real-time operations
- **Day-20**: Celery task queues and async jobs

## Setup Notes

Each day/module may contain its own environment and dependency file.

Recommended approach:

1. Enter the target day directory.
2. Create or activate that day-specific virtual environment.
3. Install dependencies from that day's requirements file when available.
4. Run the module-specific README instructions.

## Quick Access Links

- Main Postman index: [POSTMAN_MASTER_INDEX.md](./POSTMAN_MASTER_INDEX.md)
- E-commerce documentation hub: [Day-11-13/docs/INDEX.md](./Day-11-13/docs/INDEX.md)
- Day-17 framework comparison: [Day-17/README.md](./Day-17/README.md)
- Day-21 async programming guide: [Day-21/README.md](./Day-21/README.md) ⚡ **4.9x-50x performance improvement**

## Contributing

This is a personal learning repository documenting backend progress and architecture decisions. Forking for your own structured practice path is welcome.
