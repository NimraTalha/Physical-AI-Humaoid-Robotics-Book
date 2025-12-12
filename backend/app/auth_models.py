"""
Database models and utility functions for authentication.
"""
import psycopg2
from app.config import settings
from app.schemas import UserCreate
from app.security import get_password_hash

def get_db_connection():
    return psycopg2.connect(settings.database_url)

def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = get_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password, software_background, hardware_background) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (user.username, user.email, hashed_password, user.software_background, user.hardware_background)
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def get_user_by_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
