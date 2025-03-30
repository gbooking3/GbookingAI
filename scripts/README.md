```markdown
# 🧩 Fullstack App Setup Guide

This project contains a fullstack web application with:

- 🌐 **Frontend** built with React (in `/frontend`)
- 🖥️ **Backend** built with Flask + MongoDB (in `/backend`)

---

## 📁 Folder Structure

```bash
project-root/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   ├── .gitignore
│   └── venv/
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│
└── scripts/
    ├── backend_setup.sh
    ├── frontend_setup.sh
    ├── fullstack_setup.sh
    └── README.md
```

---

## 🚀 Step-by-Step: Run the Fullstack App

### ✅ 1. Run the Backend (Flask)

#### Step 1.1: Go to backend folder
```bash
cd backend
```

#### Step 1.2: Activate the virtual environment
```bash
source venv/bin/activate
```

#### Step 1.3: Start the Flask server
```bash
flask run
```

> By default, this runs on [http://localhost:8000](http://localhost:8000)

---

### ✅ 2. Run the Frontend (React)

Open a **new terminal**, then:

#### Step 2.1: Go to frontend folder
```bash
cd frontend
```

#### Step 2.2: Install dependencies
```bash
npm install
```

#### Step 2.3: Start the React app
```bash
npm start
```

> By default, this runs on [http://localhost:3000](http://localhost:3000)

---
