from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse

from app.core.nav_session import (
    clear_nav_session, get_current_nav_user, set_nav_session,
)
from app.services import nav_auth_service


router = APIRouter(prefix="/api/nav")


@router.post("/login")
async def nav_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """导航站登录（独立账号体系）"""
    user = nav_auth_service.login(username, password)
    if not user:
        return JSONResponse({"success": False, "message": "用户名或密码错误"}, 401)
    response = JSONResponse({"success": True, "user": {
        "id": user["id"], "username": user["username"], "role": user["role"],
    }})
    set_nav_session(response, {"user_id": user["id"], "username": user["username"]})
    return response


@router.post("/register")
async def nav_register(username: str = Form(...), password: str = Form(...)):
    """导航站注册（独立账号体系）"""
    success, message, user = nav_auth_service.register(username, password)
    if not success:
        return JSONResponse({"success": False, "message": message}, 400)
    response = JSONResponse({"success": True, "message": message, "user": {
        "id": user["id"], "username": user["username"], "role": user["role"],
    }})
    set_nav_session(response, {"user_id": user["id"], "username": user["username"]})
    return response


@router.post("/logout")
async def nav_logout():
    response = JSONResponse({"success": True})
    clear_nav_session(response)
    return response


@router.get("/me")
async def nav_me(request: Request):
    """当前导航站登录态"""
    user = get_current_nav_user(request)
    if not user:
        return JSONResponse({"success": False}, 401)
    return {"success": True, "user": {
        "id": user["id"], "username": user["username"], "role": user["role"],
    }}
