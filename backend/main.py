from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_db_connection
from backend.models import User, LoginUser
from backend.utils import hash_password, verify_password

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Signup endpoint
@app.post("/signup")
def signup(user: User):
    try:
        db = get_db_connection()
        if db is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        cursor = db.cursor(dictionary=True)
        hashed_password = hash_password(user.password)
        
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (user.username, user.email, hashed_password)
        )
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        print(f"Signup Error: {e}")
        if 'db' in locals() and db:
            db.rollback()
        raise HTTPException(status_code=400, detail="User already exists or DB error")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db:
            db.close()

# Login endpoint
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

    return {"message": f"Welcome {db_user['username']}"}
