# Installation Guide

## Prerequisites
- Node.js 20+
- Python 3.12+
- PostgreSQL 16+

## 1. Clone and Configure
- Copy `backend/.env.example` to `backend/.env`
- Copy `frontend/.env.example` to `frontend/.env.local`

## 2. Start PostgreSQL
Use local PostgreSQL or `docker compose up postgres`.

## 3. Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 5. Verify
- Health check: `GET http://localhost:8000/health`
- Open app: `http://localhost:3000/landing`
