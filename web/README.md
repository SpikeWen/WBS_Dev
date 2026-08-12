# WBS Dev Web

React + TypeScript + Vite admin frontend for the WBS MVP.

## Run

Start the backend first:

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/backend
../.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then start the frontend:

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm install
npm run dev
```

In restricted environments where Vite cannot bind a port, build the frontend and serve it through the backend:

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm run build
cd ../backend
../.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
