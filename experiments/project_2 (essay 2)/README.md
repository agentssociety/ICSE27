# project_5 — Blood Bank Inventory Manager

## Docker (recommended)

```bash
docker compose up --build
```

- **Frontend** → http://localhost:1081
- **Backend API** → http://localhost:9001

## Local dev (start.sh)

```bash
bash start.sh
```

- **Backend** at http://localhost:8765
- **Frontend** at http://localhost:3000

## Manual local start

**Backend**
```bash
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_5/dev
pip install -r requirements.txt
uvicorn main:app --reload --port 8765
```

**Frontend**
```bash
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_5/frontend
npm install
npm run dev
```
