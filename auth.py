import hashlib
import os
import re
import random
import binascii

import database as db
from email_utils import send_email

PBKDF2_ITERATIONS = 260_000
EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def _hash_password(password, salt=None):
    if salt is None:
        salt = binascii.hexlify(os.urandom(16)).decode("utf-8")
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS)
    return binascii.hexlify(pwd_hash).decode("utf-8"), salt


def register_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return False, "All fields are required."
    if not re.match(EMAIL_REGEX, email):
        return False, "Please enter a valid email address."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    if db.get_user_by_username(username):
        return False, "That username is already taken."
    if db.get_user_by_email(email):
        return False, "An account with that email already exists."

    pwd_hash, salt = _hash_password(password)
    db.create_user(username, email, pwd_hash, salt)
    return True, "Account created. Please log in."


def verify_user_by_email(email, password):
    user = db.get_user_by_email(email.strip().lower())
    if not user:
        return None
    pwd_hash, _ = _hash_password(password, salt=user["salt"])
    return user if pwd_hash == user["password_hash"] else None


def change_password(user_id, old_password, new_password):
    conn = db.get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return False, "User not found."

    pwd_hash, _ = _hash_password(old_password, salt=row["salt"])
    if pwd_hash != row["password_hash"]:
        return False, "Current password is incorrect."
    if len(new_password) < 4:
        return False, "New password must be at least 4 characters."

    new_hash, new_salt = _hash_password(new_password)
    db.update_user_password(user_id, new_hash, new_salt)
    return True, "Password updated."


def request_password_reset(email):
    email = email.strip().lower()
    user = db.get_user_by_email(email)
    if not user:
        # don't reveal whether the email exists
        return True, "If that email is registered, a reset code has been sent."

    code = f"{random.randint(0, 999999):06d}"
    db.create_password_reset(email, code)

    try:
        send_email(
            email,
            "GramDoctor AI — Password Reset Code",
            f"Your password reset code is: {code}\nThis code expires in 15 minutes."
        )
    except Exception as e:
        return False, f"Could not send email: {e}"

    return True, "If that email is registered, a reset code has been sent."


def reset_password_with_code(email, code, new_password):
    reset_row = db.get_valid_reset(email, code)
    if not reset_row:
        return False, "Invalid or expired code."
    if len(new_password) < 4:
        return False, "New password must be at least 4 characters."

    user = db.get_user_by_email(email)
    if not user:
        return False, "User not found."

    new_hash, new_salt = _hash_password(new_password)
    db.update_user_password(user["id"], new_hash, new_salt)
    db.mark_reset_used(reset_row["id"])
    return True, "Password reset. Please log in."

def verify_user_by_identifier(identifier, password):
    """Logs in with either username or email in the same field."""
    identifier = identifier.strip()
    user = db.get_user_by_email(identifier.lower()) if "@" in identifier else db.get_user_by_username(identifier)
    if not user:
        # fallback in case the format guess above was wrong
        user = db.get_user_by_username(identifier) or db.get_user_by_email(identifier.lower())
    if not user:
        return None
    pwd_hash, _ = _hash_password(password, salt=user["salt"])
    return user if pwd_hash == user["password_hash"] else None


def check_reset_code(email, code):
    """Validates a code WITHOUT consuming it — used for the intermediate wizard step."""
    return db.get_valid_reset(email, code) is not None

def set_email(user_id, email):
    email = email.strip().lower()
    if not re.match(EMAIL_REGEX, email):
        return False, "Please enter a valid email address."
    existing = db.get_user_by_email(email)
    if existing and existing["id"] != user_id:
        return False, "That email is already used by another account."
    db.update_user_email(user_id, email)
    return True, "Email saved."