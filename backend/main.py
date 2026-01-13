import os
import secrets
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from backend.database import get_db_connection
from backend.models import User, LoginUser, VerifyOTP
from backend.utils import hash_password, verify_password

from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def generate_otp():
    return secrets.token_hex(3).upper()  # 6 char hex code

@app.post("/signup")
async def signup(user: User, background_tasks: BackgroundTasks):
    try:
        db = get_db_connection()
        if db is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        cursor = db.cursor(dictionary=True)
        hashed_password = hash_password(user.password)
        
        # 1. Insert User (inactive)
        cursor.execute(
            "INSERT INTO users (username, email, password, is_active) VALUES (%s, %s, %s, %s)",
            (user.username, user.email, hashed_password, False)
        )
        
        # 2. Generate and store OTP
        otp_code = generate_otp()
        cursor.execute(
            "INSERT INTO otp_codes (email, otp_code) VALUES (%s, %s)",
            (user.email, otp_code)
        )
        
        db.commit()
        
        # 3. Send Email
        message = MessageSchema(
            subject="Verification Code",
            recipients=[user.email],
            body=f"Your verification code is: {otp_code}",
            subtype="html"
        )
        
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        
        return {"message": "User created. Check email for OTP."}
        
    except Exception as e:
        print(f"Signup Error: {e}")
        if 'db' in locals() and db:
            db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db:
            db.close()

@app.post("/verify")
def verify_account(data: VerifyOTP):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        # Check OTP
        cursor.execute(
            "SELECT * FROM otp_codes WHERE email=%s AND otp_code=%s AND expires_at > NOW() ORDER BY id DESC LIMIT 1",
            (data.email, data.otp)
        )
        otp_record = cursor.fetchone()
        
        if not otp_record:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
            
        # Activate User
        cursor.execute("UPDATE users SET is_active=TRUE WHERE email=%s", (data.email,))
        db.commit()
        
        return {"message": "Account verified successfully"}
        
    finally:
        cursor.close()
        db.close()

@app.post("/login")
def login(user: LoginUser):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()
    db.close()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    if not db_user['is_active']:
        raise HTTPException(status_code=400, detail="Account not verified. Please verify your email.")

    return {"message": f"Welcome {db_user['username']}"}
