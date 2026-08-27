from app.core.database import get_conn


def get_tools(include_private: bool = False) -> list[dict]:
    """获取工具列表；include_private 为 True 时同时返回私人（隐藏）工具"""
    conn = get_conn()
    if include_private:
        rows = conn.execute(
            "SELECT * FROM tools WHERE is_active=1 ORDER BY sort_order ASC, id ASC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tools WHERE is_active=1 AND visibility='public' "
            "ORDER BY sort_order ASC, id ASC"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
