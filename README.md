# Habit Tracker API (FastAPI + DynamoDB)

This project provides a CRUD API layer for managing habits stored in an AWS DynamoDB table.
It is containerized with Docker and can be tested locally before deploying to AWS ECS.

---

## 📂 Project Structure
habit-api/
│── app/
│   ├── app.py              # FastAPI CRUD logic
│   ├── requirements.txt    # Python dependencies
│   └── init.py
│── Dockerfile              # Container build instructions
│── .env                    # Local AWS creds (optional for testing)
│── README.md

---

## 🚀 Running Locally

### 1. Build Docker Image
```bash
docker build -t habit-api .

docker run -p 8000:8000 \
  --env-file .env \
  habit-api


curl -X POST http://localhost:8000/habits \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","habit_id":"h1","status":"active"}'

