# app/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.connection import create_connection, close_connection

app = FastAPI(title="User Profile Microservice", version="1.0")


# User Models

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    units_id: Optional[int] = 1
    language_id: Optional[int] = 1
    phone_number: Optional[str] = None
    location: Optional[str] = None
    about_me: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    units_id: Optional[int] = None
    language_id: Optional[int] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    about_me: Optional[str] = None


# Root endpoint

@app.get("/")
def root():
    return {"status": "User Profile API is running"}

# Health / DB test

@app.get("/test-db")
def test_db():
    conn = create_connection()
    if conn:
        close_connection(conn)
        return {"status": "✅ Service is running and DB connection works!"}
    raise HTTPException(status_code=500, detail="❌ Database connection failed")


# Get all users

@app.get("/users")
def get_users():
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, first_name, last_name, email FROM CW2.Users")
        return [
            {"user_id": row.user_id, "first_name": row.first_name, "last_name": row.last_name, "email": row.email}
            for row in cursor.fetchall()
        ]
    finally:
        close_connection(conn)


# Get user by ID

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, first_name, last_name, email FROM CW2.Users WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": row.user_id, "first_name": row.first_name, "last_name": row.last_name, "email": row.email}
    finally:
        close_connection(conn)


# Create a new user

@app.post("/users")
def create_user(user: UserCreate):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CW2.Users (first_name, last_name, email, units_id, language_id, phone_number, location, about_me)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, user.first_name, user.last_name, user.email, user.units_id, user.language_id, user.phone_number, user.location, user.about_me)
        conn.commit()
        return {"status": "✅ User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error creating user: {str(e)}")
    finally:
        close_connection(conn)


# Update a user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        # Build dynamic update statement
        fields = []
        values = []
        for key, value in user.dict(exclude_unset=True).items():
            fields.append(f"{key} = ?")
            values.append(value)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        values.append(user_id)
        sql = f"UPDATE CW2.Users SET {', '.join(fields)} WHERE user_id = ?"
        cursor.execute(sql, *values)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "✅ User updated successfully"}
    finally:
        close_connection(conn)


# Delete a user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CW2.Users WHERE user_id = ?", user_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "✅ User deleted successfully"}
    finally:
        close_connection(conn)


# Get full user profile using view

@app.get("/profiles/{user_id}")
def get_user_profile(user_id: int):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.vw_UserProfile WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))
    finally:
        close_connection(conn)


# Activities

@app.get("/activities")
def get_activities():
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.Activity")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        close_connection(conn)

# Languages

@app.get("/languages")
def get_languages():
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.Language")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


# Measurement Units

@app.get("/measurement-units")
def get_units():
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.MeasurementUnits")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        close_connection(conn)
