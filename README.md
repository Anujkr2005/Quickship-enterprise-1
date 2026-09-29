# Quickship AI Lead Generation & Sales CRM — Final MVP

Professional implementation based on the supplied Quickship developer requirement document.

## Included
- React + Vite professional CRM dashboard
- FastAPI backend
- PostgreSQL-ready SQLAlchemy database (SQLite local fallback)
- AI qualification/scoring engine using the specified 100-point model
- HOT/WARM/NORMAL/LOW classification
- Evidence-aware explanation; missing facts remain unknown
- Lead search, filters, status pipeline and CSV export
- Campaign creation foundation (city/area, category, permitted sources, target volume)
- Configurable score weights and thresholds API
- Docker + PostgreSQL deployment setup
- n8n authorized-source ingestion template
- Source connector architecture foundation

## Score model
Website 20; e-commerce platform 15; wholesale 15; manufacturer 10; active social selling 10; WhatsApp ordering 10; Pan-India shipping 10; parcel-friendly category 10.
Thresholds: HOT 80–100, WARM 60–79, NORMAL 40–59, LOW <40.

## Local run
### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\\Scripts\\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```
API: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Set `VITE_API_URL` using `.env.example` if the backend is hosted elsewhere.

## Docker
```bash
docker compose up --build
```
Frontend: http://localhost:3000
Backend docs: http://localhost:8000/docs

## Production data sources
The requirement calls for permitted/authorized APIs, licensed providers or other authorized access. No unauthorized scraping, login/CAPTCHA bypass, private-data harvesting or rate-limit bypass is implemented. Add provider credentials only after Quickship owns/authorizes those accounts and terms.

## Production hardening still required before a real public launch
- SSO/JWT/role-based authentication wired to company identity
- HTTPS, secret manager, backups, audit logging and monitoring
- Provider-specific authorized connectors and rate limits
- Production AI provider key/configuration and prompt governance
- Database migrations and managed PostgreSQL/Supabase
- Queue/worker infrastructure for PAN-India scale
- Formal security/privacy review and applicable telecom/platform compliance

This package is a complete demonstration/MVP foundation, not a claim that third-party provider access or production credentials have been configured.
