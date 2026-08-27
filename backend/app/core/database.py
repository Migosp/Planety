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
    """创建表并执行轻量迁移；账号创建由业务流程负责。"""
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'judge',
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            is_used INTEGER NOT NULL DEFAULT 0,
            used_by INTEGER,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (used_by) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_name TEXT NOT NULL,
            contact TEXT DEFAULT '',
            description TEXT DEFAULT '',
            category TEXT NOT NULL,
            file_path TEXT NOT NULL,
            thumbnail_path TEXT DEFAULT '',
            text_content TEXT DEFAULT '',
            is_hidden INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            scores_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            UNIQUE(work_id, user_id),
            FOREIGN KEY (work_id) REFERENCES works(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- PLANETY 导航站：独立账号体系（与评分工具 users 表互不干扰）
        CREATE TABLE IF NOT EXISTS nav_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );

        -- PLANETY 导航站：工具清单（public=游客可见，private=登录后可见）
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
    columns = [row[1] for row in cur.execute("PRAGMA table_info(works)").fetchall()]
    if "images_json" not in columns:
        cur.execute("ALTER TABLE works ADD COLUMN images_json TEXT DEFAULT ''")

    # 导航站账号：仅通过代码添加（无注册功能），删除遗留的 admin
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

    conn.commit()
    conn.close()
