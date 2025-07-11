# 🚦 Rate Limiter

This **Rate Limiter** is a lightweight, API rate limiting service built with **FastAPI** and **Redis**. It enables developers to define custom rate-limiting policies per route and user role, with secure API-key-based access and real-time enforcement.

---

## ✨ Features

- 🔐 **API Key Authentication** – Secure all operations with unique API keys
- 📊 **Policy-Based Limiting** – Define per-route and per-role rate limits
- 🧠 **Multi-Tenant Support** – Isolate usage per registered client
- 📄 **Structured Logging** – Store the last 1000 requests per client in Redis
- 🛡️ **IP Rate Limiting on Internal Routes** – Prevent abuse of sensitive endpoints
- 📚 **Interactive API Docs** – Swagger UI at `/docs` out of the box

---

## 🛠️ Tech Stack

- **FastAPI** – for building high-performance REST APIs
- **Redis** – used as the backend for rate limiting and logging
- **Pydantic** – for request/response validation
- **Python 3.11+**

---

## 📦 Endpoints Overview

| Method | Path           | Description                                | Auth Required |
|--------|----------------|--------------------------------------------|---------------|
| POST   | `/register`    | Register a new app and get an API key      | ❌ No          |
| POST   | `/policy`      | Define a rate limiting policy              | ✅ Yes         |
| GET    | `/policy`      | Fetch existing policies                    | ✅ Yes         |
| DELETE | `/policy`      | Remove a policy                            | ✅ Yes         |
| POST   | `/check`       | Check if a request is allowed              | ✅ Yes         |
| GET    | `/logs/latest` | Fetch recent rate limit logs               | ✅ Yes         |
| GET    | `/docs`        | Interactive API documentation              | ❌ No          |

---

## 🚀 Quick Start (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/prabhat328/rate_limiter.git
cd rate_limiter
````

### 2. Install Dependencies

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

### 3. Start Redis (Docker or local install)

```bash
docker run -d -p 6379:6379 --name redis redis:7
```
The app uses the following environment variables for Redis configuration:

* `REDIS_HOST` (default: `localhost`)
* `REDIS_PORT` (default: `6379`)

You can optionally define a `.env` file in the root for any other configuration:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
```
### 4. Run the App

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Example Usage

### Register a New App

```bash
curl -X POST http://localhost:8000/register -H "Content-Type: application/json" -d '{"name": "my-app"}'
```

### Define a Policy

```bash
curl -X POST http://localhost:8000/policy \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
        "route_key": "get_users",
        "limit": 10,
        "window_seconds": 60,
        "role": "basic"
      }'
```

### Check a Request

```bash
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
        "user_id": "user_123",
        "route_key": "get_users",
        "role": "basic"
      }'
```

---

## 📂 Project Structure

```
app/
├── api/                 # API route definitions
├── core/                # Core logic (rate limiter, auth, policy, logging)
├── models/              # Pydantic request and response models
redis.py                 # Redis client setup
config.py                # Centralized configuration loader (e.g., environment variables, settings)
main.py                  # FastAPI app entry point
requirements.txt
```

---

## 🧠 Future Enhancements

* Support for advanced rate-limiting strategies like sliding window and token bucket algorithms
* Real-time log streaming via SSE for live request monitoring
* Integration with PostgreSQL for persistent storage of user policies and audit trails
* Development of a usage analytics dashboard to visualize request patterns and blocked events

---
