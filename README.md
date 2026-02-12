# Docker Compose + Nginx Load Balancer

A simple project that runs **3 copies** of a FastAPI app behind an **Nginx reverse proxy** that load-balances requests across them.

## Project Structure

```
.
├── app/
│   └── main.py            # FastAPI application
├── nginx/
│   └── nginx.conf         # Nginx config (upstream + proxy)
├── docker-compose.yml     # Orchestrates all containers
├── Dockerfile             # Builds the FastAPI image
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .dockerignore
└── README.md
```

## Setup

### 1. Create your `.env` file

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key (get one at https://ai.google.dev/):

```
GEMINI_API_KEY=your_actual_key
```

### 2. Build and run

```bash
docker compose up --build
```

This builds the FastAPI image once and starts 4 containers (3 app + 1 nginx).

### 3. Stop

```bash
docker compose down
```

## How Load Balancing Works

Nginx uses **round-robin** by default — it sends request 1 to app1, request 2 to app2, request 3 to app3, then back to app1, and so on.

Every API response includes a `"container"` field showing which container handled it. Hit the health endpoint a few times to see it rotate:

```bash
$ for i in {1..10}; do curl http://localhost/health; echo; done
```

You'll see different container IDs:

```json
{"status": "healthy", "container": "a1b2c3d4e5f6"}
{"status": "healthy", "container": "f6e5d4c3b2a1"}
{"status": "healthy", "container": "1a2b3c4d5e6f"}
```

## API Endpoints

| Method | Path        | Description                    |
|--------|-------------|--------------------------------|
| GET    | `/health`   | Health check + container ID    |
| POST   | `/generate` | Generate text with Gemini API  |

### Example: Generate text

```bash
curl -X POST http://localhost/generate \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Hello\"}"
```

## Environment Variables

| Variable        | Description            |
|-----------------|------------------------|
| `GEMINI_API_KEY`| Google Gemini API key  |
