# Sandpyth Authentication Project

A full-stack authentication application using **React (Vite)** for the frontend and **FastAPI (Python)** for the backend, with **MySQL** as the database.

## Features
-   User Signup
-   User Login
-   Protected Dashboard Route
-   CORS enabled for local development

## Prerequisites
-   **Python 3.8+**
-   **Node.js 16+**
-   **MySQL Server** running locally

## Setup Instructions

### 1. Database Setup
Create a MySQL database named `user_auth` and a `users` table. You can run the following SQL command in your MySQL client:

```sql
CREATE DATABASE IF NOT EXISTS user_auth;
USE user_auth;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

> **Note**: The backend expects a MySQL user `root` with **no password** by default. To change this, edit `backend/database.py`.

### 2. Backend Setup
Navigate to the `backend` directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Start the server:

```bash
python -m uvicorn backend.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

### 3. Frontend Setup
Navigate to the `frontend` directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend runs at `http://localhost:5173`.

## Troubleshooting

-   **Signup Error (Password too long)**: This project uses a pinned version of `bcrypt` (3.2.2) to ensure compatibility with `passlib`. If you modify `requirements.txt`, ensure you keep this version.
-   **Database Connection Failed**: Ensure your MySQL server is running and the credentials in `backend/database.py` match your local setup.

## Project Structure

-   `backend/main.py`: API Endpoints (`/login`, `/signup`)
-   `frontend/src/App.jsx`: Frontend Routing
