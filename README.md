# Sandpyth Authentication System with OTP

A full-stack authentication application featuring **Signup**, **Email Verification (OTP)**, and **Login**.
Built with **React (Vite)**, **FastAPI (Python)**, and **MySQL**.

## Features
-   **User Registration**: Sign up with username, email, and password.
-   **Email Verification**: Real-time 6-digit OTP sent via SMTP (Gmail etc.).
-   **Secure Login**: Access validation based on password and account activation status.
-   **Protected Routes**: Dashboard accessible only after login.

## Prerequisites
-   **Python 3.8+**
-   **Node.js 16+**
-   **MySQL Server**

## Setup Instructions

### 1. Database Setup
Create a MySQL database named `user_auth`. The application will generally expect the following schema, but you can create the database and the backend will handle queries (ensure the database exists).

```sql
CREATE DATABASE IF NOT EXISTS user_auth;
```

### 2. Backend Setup
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a Virtual Environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration (.env)**:
    Create a `.env` file in the `backend/` directory with your SMTP credentials:
    ```ini
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_app_password
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_FROM=your_email@gmail.com
    ```
5.  **Database Config**:
    Check `backend/database.py` to ensure the MySQL user/password matches your local setup (default is `root` with empty password).

6.  Start the Server:
    ```bash
    python -m uvicorn backend.main:app --reload
    ```
    Runs at: `http://127.0.0.1:8000`

### 3. Frontend Setup
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install Dependencies:
    ```bash
    npm install
    ```
3.  Start the Development Server:
    ```bash
    npm run dev
    ```
    Runs at: `http://localhost:5173`

## Usage Flow
1.  Go to `http://localhost:5173/signup`.
2.  Register a new account.
3.  Check your email for the **Verification Code**.
4.  Enter the code on the Verify page.
5.  Login with your credentials.

## Troubleshooting
-   **Email not sending**: Check your `.env` file credentials. If using Gmail, ensure 2FA is on and you are using an **App Password**, not your login password.
-   **Database Error**: Ensure MySQL server is running and `user_auth` database exists.
-   **Password too long**: If you see this backend error, ensure `bcrypt==3.2.2` is installed (check `requirements.txt`).
