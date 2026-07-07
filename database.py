

import sqlite3
import json
import os
import secrets
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't already exist. Safe to call every run."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            language TEXT DEFAULT 'English',
            theme TEXT DEFAULT 'light',
            font_size TEXT DEFAULT 'normal',
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            language TEXT,
            symptoms_json TEXT,
            active_symptoms_json TEXT,
            triage_color TEXT,
            confidence REAL,
            decision_source TEXT,
            message TEXT,
            referral TEXT,
            alternate_referral TEXT,
            followup_answers_json TEXT,
            ai_response TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            used INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn = get_connection()
    try:
      conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
      conn.commit()
    except Exception:
      pass
    conn.close()


def create_session(user_id, days_valid=30):
    """Creates a long-lived session token for 'remember me across refresh'."""
    token = secrets.token_hex(32)
    now = datetime.now()
    expires = now + timedelta(days=days_valid)
    conn = get_connection()
    conn.execute(
        "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (token, user_id, now.isoformat(), expires.isoformat())
    )
    conn.commit()
    conn.close()
    return token


def get_user_by_session_token(token):
    """Returns the user row if the token exists and hasn't expired, else None."""
    if not token:
        return None
    conn = get_connection()
    row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token,)).fetchone()
    if not row:
        conn.close()
        return None
    if datetime.fromisoformat(row["expires_at"]) < datetime.now():
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        return None
    user = conn.execute("SELECT * FROM users WHERE id = ?", (row["user_id"],)).fetchone()
    conn.close()
    return user


def delete_session(token):
    if not token:
        return
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,)
    ).fetchone()
    conn.close()
    return row


def create_user(username, password_hash, salt):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (username, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
        (username, password_hash, salt, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()
    return row


def create_user(username, email, password_hash, salt):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (username, email, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, email.strip().lower(), password_hash, salt, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def update_user_password(user_id, password_hash, salt):
    conn = get_connection()
    conn.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (password_hash, salt, user_id))
    conn.commit()
    conn.close()


def create_password_reset(email, code, minutes_valid=15):
    conn = get_connection()
    expires = (datetime.now() + timedelta(minutes=minutes_valid)).isoformat()
    conn.execute(
        "INSERT INTO password_resets (email, code, expires_at, used) VALUES (?, ?, ?, 0)",
        (email.strip().lower(), code, expires)
    )
    conn.commit()
    conn.close()


def get_valid_reset(email, code):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM password_resets WHERE email = ? AND code = ? AND used = 0 ORDER BY id DESC LIMIT 1",
        (email.strip().lower(), code)
    ).fetchone()
    conn.close()
    if not row:
        return None
    if datetime.fromisoformat(row["expires_at"]) < datetime.now():
        return None
    return row


def mark_reset_used(reset_id):
    conn = get_connection()
    conn.execute("UPDATE password_resets SET used = 1 WHERE id = ?", (reset_id,))
    conn.commit()
    conn.close()

def update_user_preferences(user_id, language=None, theme=None, font_size=None):
    conn = get_connection()
    if language is not None:
        conn.execute("UPDATE users SET language = ? WHERE id = ?", (language, user_id))
    if theme is not None:
        conn.execute("UPDATE users SET theme = ? WHERE id = ?", (theme, user_id))
    if font_size is not None:
        conn.execute("UPDATE users SET font_size = ? WHERE id = ?", (font_size, user_id))
    conn.commit()
    conn.close()


# ------------------------- History helpers -------------------------

def save_history_entry(user_id, language, symptoms, active_symptoms, triage_result,
                        referral=None, alternate_referral=None, followup_answers=None,
                        ai_response=None):
    """Logs one completed triage session. Does not alter what was computed —
    purely records the already-produced result for the History page."""
    conn = get_connection()
    conn.execute("""
        INSERT INTO history (
            user_id, created_at, language, symptoms_json, active_symptoms_json,
            triage_color, confidence, decision_source, message,
            referral, alternate_referral, followup_answers_json, ai_response
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        datetime.now().isoformat(),
        language,
        json.dumps(symptoms, ensure_ascii=False),
        json.dumps(active_symptoms, ensure_ascii=False),
        triage_result.get("color"),
        triage_result.get("confidence"),
        triage_result.get("source"),
        triage_result.get("message"),
        referral,
        alternate_referral,
        json.dumps(followup_answers or {}, ensure_ascii=False),
        ai_response,
    ))
    conn.commit()
    conn.close()


def get_history_for_user(user_id, limit=50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return rows


def delete_history_entry(entry_id, user_id):
    conn = get_connection()
    conn.execute("DELETE FROM history WHERE id = ? AND user_id = ?", (entry_id, user_id))
    conn.commit()
    conn.close()

def update_user_email(user_id, email):
    conn = get_connection()
    conn.execute("UPDATE users SET email = ? WHERE id = ?", (email.strip().lower(), user_id))
    conn.commit()
    conn.close()