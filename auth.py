"""
auth.py
Registration / login helpers for GramDoctor AI.
Uses Python's built-in hashlib (PBKDF2-HMAC-SHA256) so no extra
dependency needs to be added to requirements.txt.
New file — does not touch any ML/triage backend logic.
"""

import hashlib
import os
import binascii

import database as db

PBKDF2_ITERATIONS = 260_000


def _hash_password(password, salt=None):
    if salt is None:
        salt = binascii.hexlify(os.urandom(16)).decode("utf-8")
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS
    )
    return binascii.hexlify(pwd_hash).decode("utf-8"), salt


def register_user(username, password):
    """Returns (success: bool, message: str)."""
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."

    existing = db.get_user_by_username(username)
    if existing:
        return False, "That username is already taken."

    pwd_hash, salt = _hash_password(password)
    db.create_user(username, pwd_hash, salt)
    return True, "Account created. Please log in."


def verify_user(username, password):
    """Returns the user row if credentials are valid, else None."""
    user = db.get_user_by_username(username.strip())
    if not user:
        return None
    pwd_hash, _ = _hash_password(password, salt=user["salt"])
    if pwd_hash == user["password_hash"]:
        return user
    return None
