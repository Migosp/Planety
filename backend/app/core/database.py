import hashlib
import secrets
import sqlite3

from app.core.config import DB_PATH


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """PLANETY 导航站数据库：独立账号 nav_users + 工具清单 tools"""
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS nav_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            url TEXT NOT NULL,
            icon TEXT DEFAULT '',
            visibility TEXT NOT NULL DEFAULT 'public',
            sort_order INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );
        """
    )
    # 导航站账号：仅通过代码添加（无注册功能）
    for username, password in (("migosp", "cptbtptp123"), ("liunbplus", "liunb0807")):
        if not cur.execute("SELECT id FROM nav_users WHERE username=?", (username,)).fetchone():
            salt = secrets.token_hex(16)
            pw_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            cur.execute(
                "INSERT INTO nav_users (username, password_hash, salt, role) VALUES (?,?,?,?)",
                (username, pw_hash, salt, "admin"),
            )
    cur.execute("DELETE FROM nav_users WHERE username NOT IN ('migosp','liunbplus')")
    # 工具清单种子：已有则改名，没有则插入
    tool_name = "“大众创享”作品展示"
    tool_desc = "大众创享作品浏览与评分"
    tool_icon = "🎨"
    tool_row = cur.execute("SELECT id FROM tools WHERE url='/art'").fetchone()
    if tool_row:
        cur.execute(
            "UPDATE tools SET name=?, description=?, icon=? WHERE id=?",
            (tool_name, tool_desc, tool_icon, tool_row["id"]),
        )
    else:
        cur.execute(
            "INSERT INTO tools (name, description, url, icon, visibility, sort_order) VALUES (?,?,?,?,?,?)",
            (tool_name, tool_desc, "/art", tool_icon, "public", 1),
        )
    # 私人工具：AstrBot 控制台（登录导航站后可见）
    astrbot_name = "AstrBot 控制台"
    astrbot_desc = "AstrBot 机器人管理后台（洛茜 QQ 机器人）"
    astrbot_url = "http://111.231.98.33/astrbot/"
    astrbot_icon = "🤖"
    astrbot_row = cur.execute(
        "SELECT id FROM tools WHERE url=?", (astrbot_url,)
    ).fetchone()
    if astrbot_row:
        cur.execute(
            "UPDATE tools SET name=?, description=?, icon=?, visibility=?, sort_order=? WHERE id=?",
            (astrbot_name, astrbot_desc, astrbot_icon, "private", 2, astrbot_row["id"]),
        )
    else:
        cur.execute(
            "INSERT INTO tools (name, description, url, icon, visibility, sort_order) VALUES (?,?,?,?,?,?)",
            (astrbot_name, astrbot_desc, astrbot_url, astrbot_icon, "private", 2),
        )

    conn.commit()
    conn.close()
