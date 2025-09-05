# Budget Buddy

Budget Buddy is a simple web application that helps users manage debit and cretit

## How to use the app

### in development
```
cp .env.example .env
sudo sh -c 'echo "\n127.0.0.1 budget-buddy.local\n" >> /etc/hosts'
make down build up monitor
open http://localhost:8080/docs for API docs
open http://budget-buddy.local:5173/ for UI
```

### in production
```
gcloud auth login
make deploy-gcp
open https://budget-buddy-692055417597.us-east1.run.app/
```

# How to log in
Just use any username and password,
if such user doesn't exist - it will be created with the provided password,
otherwise - you will have to recall the previous password to log in

# An overview of your choices
- FastAPI for the backend - ample for many use cases
- SQLAlchemy as ORM to provide a higher level of abstraction
- yoyo-migrations for DB migrations - simple but effective
- PostgreSQL for the DB - could be any RDS though
- Makefile for workflow automation (npm scripts - not multiline-friendly)
- containerization to unify environments and simplify local installation
- Docker Compose for the orchestration
- GCP for the prod infrastructure - as a proof of concept
- sass for scss preprocessing - scss is more maintainable than css

# Any assumptions you made
- this is an PoC aimed to show the basic idea
- assuming that the currency is always USD

# Any trade-offs or shortcuts taken to fit the timebox
- ideally to separate backend and frontend containers
- no pytest, no vitest or jest
- ideally to add at least sign up process, email verification etc
- list of transactions is not paginated now
- better to use state management (Redux)
