"""停机坪导航站独立会话（独立 cookie，与评分工具 session 互不干扰）"""
from typing import Optional

from fastapi import HTTPException, Request

from app.core.session import serializer
from app.repositories import nav_user_repository

NAV_COOKIE = "nav_session"


def get_nav_session(request: Request) -> dict:
    token = request.cookies.get(NAV_COOKIE)
    if not token:
        return {}
    try:
        return serializer.loads(token)
    except Exception:
        return {}


def set_nav_session(response, data: dict) -> None:
    response.set_cookie(
        key=NAV_COOKIE, value=serializer.dumps(data), httponly=True,
        max_age=86400 * 7, samesite="lax",
    )


def clear_nav_session(response) -> None:
    response.delete_cookie(NAV_COOKIE)


def get_current_nav_user(request: Request) -> Optional[dict]:
    user_id = get_nav_session(request).get("user_id")
    return nav_user_repository.get_by_id(user_id) if user_id else None


def require_nav_login(request: Request) -> dict:
    user = get_current_nav_user(request)
    if not user:
        raise HTTPException(status_code=401)
    return user


def require_nav_admin(request: Request) -> dict:
    user = require_nav_login(request)
    if user["role"] != "admin":
        raise HTTPException(status_code=403)
    return user
