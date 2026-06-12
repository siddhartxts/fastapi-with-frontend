# Finance Backend

A beginner-friendly FastAPI project for saving:

- Watchlist items, such as ticker symbols and notes
- Finance notes, such as notes about a ticker or investment idea

The app has:

- A FastAPI backend
- A simple HTML/CSS/JavaScript dashboard
- PostgreSQL as the database
- SQLAlchemy as the Python database layer
- Docker Compose for running everything together
- Adminer for viewing the database in your browser

This README explains two ways to run the project:

1. Run Python directly using a local `.venv`
2. Run the full project using Docker Compose

If you are a complete beginner, start with the Docker Compose method first. It runs the API, database, and database viewer together.

---

## What This Project Does

When you open the app in your browser, you see a small dashboard.

You can:

- Add a watchlist item
- View all watchlist items
- Add a finance note
- View all finance notes

The dashboard talks to the FastAPI backend using HTTP requests.

For example:

- The browser opens `/`
- FastAPI returns `templates/home.html`
- The browser loads `static/js/app.js`
- JavaScript calls API routes like `/watchlist/` and `/financenotes/`
- FastAPI saves and reads data using SQLAlchemy
- SQLAlchemy talks to PostgreSQL

The basic flow looks like this:

```text
Browser
  -> FastAPI app
  -> SQLAlchemy
  -> PostgreSQL database
```

When running with Docker Compose, the flow looks like this:

```text
Browser
  -> api container
  -> db container
```

Adminer is a separate browser tool that lets you inspect the database:

```text
Browser
  -> adminer container
  -> db container
```

---

## Project Structure

```text
fin_back/
  main.py
  database.py
  models.py
  requirements.txt
  Dockerfile
  docker-compose.yml
  .env
  .env.example
  .gitignore
  .dockerignore

  routers/
    watchlist.py
    financenotes.py

  templates/
    home.html

  static/
    css/
      styles.css
    js/
      app.js

  alembic/
    env.py
    versions/
```

Important files:

| File | Purpose |
| --- | --- |
| `main.py` | Creates the FastAPI app, serves the homepage, loads routers, mounts static files |
| `database.py` | Creates the database connection using SQLAlchemy |
| `models.py` | Defines database tables using SQLAlchemy models |
| `routers/watchlist.py` | API routes for watchlist items |
| `routers/financenotes.py` | API routes for finance notes |
| `templates/home.html` | The browser page |
| `static/js/app.js` | Frontend JavaScript that calls the API |
| `static/css/styles.css` | Frontend styling |
| `requirements.txt` | Python packages needed by the app |
| `Dockerfile` | Instructions for building the FastAPI app container |
| `docker-compose.yml` | Runs the API, PostgreSQL, and Adminer together |
| `.env` | Your real local environment values |
| `.env.example` | Safe template for other people |
| `.gitignore` | Tells git what not to commit |
| `.dockerignore` | Tells Docker what not to copy into the image |

---

## Important Beginner Concepts

### What Is FastAPI?

FastAPI is the Python web framework used by this project.

It lets you create routes like:

```python
@app.get("/")
def home():
    ...
```

That means:

```text
When someone visits GET /, run this Python function.
```

This project also has API routes like:

```text
GET    /watchlist/
POST   /watchlist/
GET    /watchlist/{id}
PUT    /watchlist/{id}
DELETE /watchlist/{id}

GET    /financenotes/
POST   /financenotes/
GET    /financenotes/{id}
PUT    /financenotes/{id}
DELETE /financenotes/{id}
```

You can view the automatic FastAPI API docs here after the app is running:

```text
http://localhost:8000/docs
```

### What Is PostgreSQL?

PostgreSQL is the database.

The app stores watchlist items and finance notes in PostgreSQL tables.

This project uses two main tables:

```text
watchlist
finance_notes
```

The table definitions live in `models.py`.

### What Is SQLAlchemy?

SQLAlchemy is the Python library that lets the app talk to the database.

Instead of writing raw SQL everywhere, the app can use Python classes.

For example, this model:

```python
class WatchlistItem(Base):
    __tablename__ = "watchlist"
```

represents a database table named:

```text
watchlist
```

### What Is `.venv`?

`.venv` is a local Python virtual environment.

Think of it as a private Python package folder for this project.

Without a virtual environment, packages installed for one project can affect other projects on your machine.

With a virtual environment:

```text
This project gets its own isolated Python packages.
```

### What Is Docker?

Docker lets you package an app with the environment it needs.

Instead of saying:

```text
Install Python, install packages, install Postgres, configure everything manually...
```

Docker lets you define that setup in files:

```text
Dockerfile
docker-compose.yml
```

### What Is Docker Compose?

Docker Compose runs multiple containers together.

This project has three services in `docker-compose.yml`:

| Service | What it does |
| --- | --- |
| `api` | Runs the FastAPI app |
| `db` | Runs PostgreSQL |
| `adminer` | Runs a simple database viewer in your browser |

### What Is Adminer?

Adminer is a lightweight web UI for looking inside the database.

It is simpler than pgAdmin.

For a beginner, Adminer is usually easier.

After Docker is running, Adminer is available at:

```text
http://localhost:8080
```

### What Is `.env`?

`.env` stores environment variables.

Environment variables are configuration values that your app needs.

Examples:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=fastapi
```

The real `.env` file should not be committed to git because it can contain passwords.

That is why `.gitignore` ignores `.env`.

### What Is `.env.example`?

`.env.example` is a safe template.

It shows other people what variables they need, without exposing your real password.

The normal workflow is:

```bash
cp .env.example .env
```

Then edit `.env`.

Do not rename `.env.example` to `.env`.

Copy it instead, because `.env.example` should stay in the repo for other people.

### `db` vs `localhost`

This is very important.

Inside Docker Compose, containers talk to each other by service name.

So the FastAPI container connects to Postgres using:

```text
db
```

That is why the Docker database URL looks like this:

```env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:your_password@db:5432/fastapi
```

But if you run Python directly on your computer using `.venv`, your Python process is not inside Docker.

From your normal terminal, the database host is usually:

```text
localhost
```

or:

```text
127.0.0.1
```

So a local `.venv` database URL usually looks like:

```bash
postgresql://postgres:your_password@localhost:5432/fastapi
```

Remember:

| Where the app runs | Database host |
| --- | --- |
| App inside Docker | `db` |
| App directly in `.venv` | `localhost` |

---

## Environment Variables

The example environment file looks like this:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me
POSTGRES_DB=fastapi
POSTGRES_PORT=5432

SQLALCHEMY_DATABASE_URL=postgresql://postgres:change_me@db:5432/fastapi

API_PORT=8000
ADMINER_PORT=8080
```

Meaning:

| Variable | Meaning |
| --- | --- |
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `POSTGRES_PORT` | Port exposed on your machine for Postgres |
| `SQLALCHEMY_DATABASE_URL` | Full database connection string used by FastAPI |
| `API_PORT` | Port for the FastAPI app |
| `ADMINER_PORT` | Port for Adminer |

For Docker Compose, use `db` in `SQLALCHEMY_DATABASE_URL`.

For local `.venv` development, use `localhost` in `SQLALCHEMY_DATABASE_URL` if you export it manually.

Docker Compose automatically reads a file named `.env` from the same folder as `docker-compose.yml`.

Plain Python does not automatically read `.env` in this project.

So when running with `.venv`, either:

- Let `database.py` use its default local database URL
- Or manually export `SQLALCHEMY_DATABASE_URL` before starting Uvicorn

---

## Prerequisites

For the Docker method, install:

- Docker Desktop

For the `.venv` method, install:

- Python 3.10 or newer
- Docker Desktop if you want to run PostgreSQL using Docker

The Dockerfile currently uses:

```text
python:3.14-slim
```

Your local Python does not have to be exactly 3.14, but it should be modern enough for this project. Python 3.10 or newer is important because the code uses syntax like:

```python
str | None
```

---

## Method 1: Run Everything With Docker Compose

This is the easiest full setup.

It runs:

- FastAPI
- PostgreSQL
- Adminer

### Step 1: Install Docker

Install Docker Desktop:

```text
https://www.docker.com/products/docker-desktop/
```

After installing, open Docker Desktop and make sure it is running.

Check from the terminal:

```bash
docker --version
docker compose version
```

If Docker is working, both commands should print versions.

### Step 2: Create Your `.env` File

If `.env` does not exist yet:

```bash
cp .env.example .env
```

Open `.env` and change the password:

```env
POSTGRES_PASSWORD=some_password_here
```

Also update the password inside the database URL:

```env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:some_password_here@db:5432/fastapi
```

The password in both places must match.

### Step 3: Build and Start the Containers

Run:

```bash
docker compose up --build
```

This starts Docker in foreground mode.

Foreground mode means logs stay visible in your terminal.

You should see logs from:

```text
finance_backend_api
finance_backend_db
finance_backend_adminer
```

To stop it, press:

```text
Ctrl + C
```

### Step 4: Run Containers in the Background

Usually, after you know it works, run:

```bash
docker compose up -d --build
```

The `-d` means detached mode.

Detached mode means:

```text
Run in the background and give me my terminal back.
```

### Step 5: Open the App

Open:

```text
http://localhost:8000
```

You should see the finance dashboard.

### Step 6: Open FastAPI Docs

Open:

```text
http://localhost:8000/docs
```

This shows interactive API documentation.

You can test API routes from the browser.

### Step 7: Open Adminer

Open:

```text
http://localhost:8080
```

Login using:

```text
System: PostgreSQL
Server: db
Username: postgres
Password: the password from .env
Database: fastapi
```

In Adminer, you should be able to see tables like:

```text
watchlist
finance_notes
```

### Step 8: Useful Docker Commands

See running containers:

```bash
docker compose ps
```

View logs for everything:

```bash
docker compose logs -f
```

View logs only for the API:

```bash
docker compose logs -f api
```

View logs only for the database:

```bash
docker compose logs -f db
```

Stop containers:

```bash
docker compose down
```

Stop containers and delete the database volume:

```bash
docker compose down -v
```

Be careful with `-v`.

It deletes the database data.

Use it only when you are okay losing local database data.

Rebuild the app image:

```bash
docker compose build api
```

Restart only the API:

```bash
docker compose restart api
```

Open a shell inside the API container:

```bash
docker compose exec api bash
```

Open a Postgres shell:

```bash
docker compose exec db psql -U postgres -d fastapi
```

---

## How Docker Works In This Project

### `Dockerfile`

The `Dockerfile` builds the FastAPI app image.

Current Dockerfile:

```dockerfile
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Line by line:

| Line | Meaning |
| --- | --- |
| `FROM python:3.14-slim` | Start from a small Python image |
| `WORKDIR /app` | Use `/app` as the folder inside the container |
| `COPY requirements.txt .` | Copy only requirements first |
| `RUN pip install ...` | Install Python packages |
| `COPY . .` | Copy the rest of the project into the image |
| `EXPOSE 8000` | Document that the app uses port 8000 |
| `CMD [...]` | Start Uvicorn when the container starts |

### Why Copy `requirements.txt` First?

Docker builds in layers.

Python dependencies do not change as often as your code.

By copying `requirements.txt` first, Docker can reuse the dependency install layer when only your app code changes.

That makes rebuilds faster.

### `docker-compose.yml`

Compose runs the project as multiple services.

The important services are:

```yaml
api:
  build: .
```

This builds the FastAPI image using the Dockerfile.

```yaml
db:
  image: postgres:16-alpine
```

This uses the official PostgreSQL image.

```yaml
adminer:
  image: adminer:4.8.1
```

This uses the Adminer image.

### Why `depends_on`?

The API needs the database.

So Compose has:

```yaml
depends_on:
  db:
    condition: service_healthy
```

This tells Compose:

```text
Start the API after the database is healthy.
```

### Why the Healthcheck?

The database container can be running before PostgreSQL is ready to accept connections.

The healthcheck runs:

```bash
pg_isready
```

That checks whether PostgreSQL is ready.

### What Is a Docker Volume?

The Compose file has:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This means database data is stored in a Docker volume named:

```text
postgres_data
```

Without a volume, your database data could disappear when the container is removed.

With a volume, the data survives normal container restarts.

### Why Are Ports Bound to `127.0.0.1`?

The Compose file exposes ports like this:

```yaml
ports:
  - "127.0.0.1:${API_PORT}:8000"
```

This means:

```text
Only expose this service on localhost.
```

That is safer than exposing it publicly.

It is especially important for:

- Adminer
- PostgreSQL

You usually do not want your database viewer or database exposed to the public internet.

---

## Method 2: Run The App With `.venv`

This method runs the FastAPI app directly on your machine.

You still need PostgreSQL running somewhere.

The beginner-friendly option is:

- Run PostgreSQL using Docker Compose
- Run FastAPI locally using `.venv`

That gives you easy Python development while still avoiding manual Postgres installation.

### Step 1: Create the Virtual Environment

From the project folder:

```bash
python3 -m venv .venv
```

This creates a folder named:

```text
.venv
```

### Step 2: Activate the Virtual Environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

After activating, your terminal may show:

```text
(.venv)
```

That means the virtual environment is active.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

With the virtual environment active:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Why use `python -m pip`?

It makes sure pip belongs to the active Python environment.

### Step 4: Start Only The Database With Docker

If you want the app in `.venv`, but the database in Docker:

```bash
cp .env.example .env
```

Edit `.env`, then start only the database and Adminer:

```bash
docker compose up -d db adminer
```

Now Postgres is available from your normal terminal at:

```text
localhost:5432
```

Adminer is available at:

```text
http://localhost:8080
```

### Step 5: Set the Local Database URL

When the app runs inside Docker, it uses host `db`.

When the app runs in `.venv`, use host `localhost`.

On macOS or Linux:

```bash
export SQLALCHEMY_DATABASE_URL='postgresql://postgres:your_password@localhost:5432/fastapi'
```

Replace `your_password` with the password from `.env`.

If your password contains special characters, keep the single quotes around the URL.

### Step 6: Run FastAPI Locally

Run:

```bash
uvicorn main:app --reload
```

Or:

```bash
python -m uvicorn main:app --reload
```

The `--reload` flag means:

```text
Restart the server when code changes.
```

This is useful during development.

Open:

```text
http://localhost:8000
```

Open API docs:

```text
http://localhost:8000/docs
```

### Step 7: Stop Local Development

To stop Uvicorn:

```text
Ctrl + C
```

To deactivate the virtual environment:

```bash
deactivate
```

To stop the Docker database and Adminer:

```bash
docker compose down
```

---

## Which Method Should You Use?

Use Docker Compose when:

- You want the easiest full setup
- You do not want to install Postgres manually
- You want the app, database, and Adminer to run together
- You want something closer to deployment

Use `.venv` when:

- You are actively coding Python
- You want `--reload`
- You want easier debugging
- You want to understand how Python dependencies work

A very common development setup is:

```text
Postgres in Docker
FastAPI in .venv
```

That gives you:

- Easy database setup
- Easy Python development

---

## Running On An SSH Server

If you deploy this project on a remote server over SSH, the safest beginner setup is:

- Run Docker Compose on the server
- Keep ports bound to `127.0.0.1`
- Use SSH port forwarding from your laptop

This project already binds ports to `127.0.0.1`.

That means the app, Adminer, and Postgres are not exposed publicly by default.

### Step 1: SSH Into Server

From your laptop:

```bash
ssh your_user@your_server_ip
```

### Step 2: Clone Or Upload The Project

If using git:

```bash
git clone your_repo_url
cd fin_back
```

If you copied the folder manually, just `cd` into it.

### Step 3: Create `.env`

On the server:

```bash
cp .env.example .env
nano .env
```

Change:

```env
POSTGRES_PASSWORD=change_me
```

Also update:

```env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:change_me@db:5432/fastapi
```

Both passwords must match.

### Step 4: Start Docker Compose

On the server:

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f
```

### Step 5: Create SSH Port Forwarding

On your laptop, not inside the SSH session, run:

```bash
ssh -N \
  -L 8000:127.0.0.1:8000 \
  -L 8080:127.0.0.1:8080 \
  -L 5432:127.0.0.1:5432 \
  your_user@your_server_ip
```

Keep that terminal open.

Now on your laptop browser, open:

```text
http://localhost:8000
http://localhost:8080
```

Even though the app is running on the server, the SSH tunnel makes it feel like it is running on your laptop.

### Adminer Login Through SSH Tunnel

Open:

```text
http://localhost:8080
```

Use:

```text
System: PostgreSQL
Server: db
Username: postgres
Password: password from server .env
Database: fastapi
```

### TablePlus Login Through SSH Tunnel

If you use TablePlus on your laptop, connect to:

```text
Host: 127.0.0.1
Port: 5432
User: postgres
Password: password from server .env
Database: fastapi
```

This works because your laptop port `5432` is forwarded to the server's localhost port `5432`.

### Later: Making The API Public

When you are ready to expose only the API publicly, use a reverse proxy such as:

- Caddy
- Nginx

The public setup usually looks like:

```text
Internet
  -> HTTPS reverse proxy
  -> FastAPI container
```

Keep these private:

- PostgreSQL
- Adminer

Do not expose Adminer or Postgres directly to the internet.

---

## API Endpoints

### Homepage

```text
GET /
```

Shows the dashboard.

### Watchlist

Get all watchlist items:

```text
GET /watchlist/
```

Create a watchlist item:

```text
POST /watchlist/
```

Example JSON body:

```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "notes": "Long-term watchlist idea"
}
```

Get one watchlist item:

```text
GET /watchlist/1
```

Update one watchlist item:

```text
PUT /watchlist/1
```

Delete one watchlist item:

```text
DELETE /watchlist/1
```

### Finance Notes

Get all finance notes:

```text
GET /financenotes/
```

Create a finance note:

```text
POST /financenotes/
```

Example JSON body:

```json
{
  "ticker": "MSFT",
  "title": "Earnings note",
  "content": "Revenue growth looks interesting."
}
```

Get one finance note:

```text
GET /financenotes/1
```

Update one finance note:

```text
PUT /financenotes/1
```

Delete one finance note:

```text
DELETE /financenotes/1
```

---

## Database Tables

The database models live in `models.py`.

### `watchlist`

Columns:

| Column | Meaning |
| --- | --- |
| `id` | Unique ID |
| `ticker` | Stock ticker |
| `company_name` | Optional company name |
| `notes` | Optional notes |
| `created_at` | When the row was created |

### `finance_notes`

Columns:

| Column | Meaning |
| --- | --- |
| `id` | Unique ID |
| `ticker` | Stock ticker |
| `title` | Note title |
| `content` | Note content |
| `created_at` | When the row was created |

The app currently creates tables automatically on startup using:

```python
models.Base.metadata.create_all(bind=engine)
```

That is beginner-friendly because you do not need to manually create tables.

Alembic is also present in the project for migrations, which becomes useful later when the database structure changes over time.

---

## Alembic Basics

Alembic is a database migration tool.

In beginner terms:

```text
Alembic helps you change database tables safely over time.
```

For example, if later you add a new column to `WatchlistItem`, you can create a migration.

Generate a migration:

```bash
alembic revision --autogenerate -m "add new column"
```

Run migrations:

```bash
alembic upgrade head
```

Inside Docker:

```bash
docker compose exec api alembic upgrade head
```

For this current beginner app, automatic table creation is enough to get started.

---

## Common Problems And Fixes

### Docker says it cannot connect to the Docker daemon

Error might look like:

```text
Cannot connect to the Docker daemon
```

Fix:

- Open Docker Desktop
- Wait until Docker is fully running
- Try again

### Port is already in use

Error might mention:

```text
port is already allocated
```

Fix:

Edit `.env` and change ports:

```env
API_PORT=8001
ADMINER_PORT=8081
POSTGRES_PORT=5433
```

Then restart:

```bash
docker compose up -d
```

### App says it cannot connect to host `db`

This usually means you are running the app directly in `.venv` but using the Docker database URL.

Wrong for `.venv`:

```text
postgresql://postgres:password@db:5432/fastapi
```

Correct for `.venv`:

```text
postgresql://postgres:password@localhost:5432/fastapi
```

### App says connection refused

This usually means PostgreSQL is not running.

Check:

```bash
docker compose ps
```

Start the database:

```bash
docker compose up -d db
```

### Password changed but Postgres still rejects login

Postgres stores its initialized data in the Docker volume.

If you changed `POSTGRES_PASSWORD` after the database was already created, the old password may still be stored in the volume.

For a fresh local reset:

```bash
docker compose down -v
docker compose up -d --build
```

Warning:

```text
docker compose down -v deletes local database data.
```

### `ModuleNotFoundError`

You probably did not install requirements in the active virtual environment.

Fix:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Adminer cannot login

For Docker Adminer, use:

```text
Server: db
```

Do not use `localhost` in Adminer when Adminer itself is running inside Docker.

Adminer is a container, so from Adminer's point of view, the database is called `db`.

### TablePlus cannot connect

If using TablePlus from your laptop, use:

```text
Host: 127.0.0.1
Port: 5432
```

If the app is on an SSH server, make sure your SSH tunnel is running.

---

## Git Ignore And Docker Ignore

### `.gitignore`

`.gitignore` tells git what not to commit.

Important ignored files:

```text
.env
.venv/
__pycache__/
.DS_Store
```

Why ignore `.env`?

Because it can contain real passwords.

Why ignore `.venv`?

Because dependencies can be recreated using:

```bash
python -m pip install -r requirements.txt
```

### `.dockerignore`

`.dockerignore` tells Docker what not to copy into the image.

This keeps the image smaller and cleaner.

For example, Docker should not copy:

```text
.venv
__pycache__
.git
.env
```

---

## Daily Cheat Sheet

### Full Docker Start

```bash
docker compose up -d --build
```

### Full Docker Stop

```bash
docker compose down
```

### See Logs

```bash
docker compose logs -f
```

### Open App

```text
http://localhost:8000
```

### Open API Docs

```text
http://localhost:8000/docs
```

### Open Adminer

```text
http://localhost:8080
```

### Local Python Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
docker compose up -d db adminer
export SQLALCHEMY_DATABASE_URL='postgresql://postgres:your_password@localhost:5432/fastapi'
python -m uvicorn main:app --reload
```

---

## Recommended Beginner Workflow

Use this while learning:

1. Use Docker Compose first to confirm the full app works.
2. Use Adminer to look at the database tables.
3. Use `/docs` to understand the API routes.
4. Then try running FastAPI with `.venv`.
5. Keep PostgreSQL in Docker while developing Python locally.
6. When deploying to an SSH server, keep Adminer and Postgres private behind SSH port forwarding.

That gives you a clean learning path:

```text
Docker first -> understand services -> use Adminer -> try .venv -> deploy over SSH
```
