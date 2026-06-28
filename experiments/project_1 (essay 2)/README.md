# project_2

## Running the project

```bash
bash start.sh
```

This starts:
- **Backend** at http://localhost:8000
- **Frontend** at http://localhost:3000

## Manual start

**Backend**
```bash
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_2/dev
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_2/frontend
npm install
npm run dev
```
