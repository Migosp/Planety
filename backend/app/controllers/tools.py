from fastapi import APIRouter, Request

from app.core.nav_session import get_current_nav_user
from app.services import tool_service


router = APIRouter(prefix="/api/tools")


@router.get("")
async def list_tools(request: Request):
    """停机坪工具列表：游客仅见公共工具，登录导航站后含私人工具"""
    user = get_current_nav_user(request)
    tools = tool_service.list_tools(user)
    return {"success": True, "tools": tools, "count": len(tools)}
