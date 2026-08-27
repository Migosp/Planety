import hashlib
import secrets
from typing import Optional

from app.core.database import get_conn


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """返回 (hash, salt)"""
    salt = salt or secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest(), salt


def verify(username: str, password: str) -> Optional[dict]:
    """验证导航站账号登录，成功返回用户dict，失败返回None"""
    conn = get_conn()
    row = conn.execute("SELECT * FROM nav_users WHERE username=?", (username,)).fetchone()
    conn.close()
    if not row:
        return None
    password_hash, _ = hash_password(password, row["salt"])
    return dict(row) if password_hash == row["password_hash"] else None


def get_by_id(user_id: int) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM nav_users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create(username: str, password: str, role: str = "user") -> tuple:
    """创建导航站账号。返回 (success, message, user)"""
    conn = get_conn()
    if conn.execute("SELECT id FROM nav_users WHERE username=?", (username,)).fetchone():
        conn.close()
        return False, "用户名已存在", None
    password_hash, salt = hash_password(password)
    cursor = conn.execute(
        "INSERT INTO nav_users (username, password_hash, salt, role) VALUES (?,?,?,?)",
        (username, password_hash, salt, role),
    )
    conn.commit()
    user = dict(conn.execute("SELECT * FROM nav_users WHERE id=?", (cursor.lastrowid,)).fetchone())
    conn.close()
    return True, "创建成功", user
