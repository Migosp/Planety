from app.repositories import tool_repository


def list_tools(user=None) -> list[dict]:
    """游客只返回公共工具；登录导航站后同时返回私人工具"""
    return tool_repository.get_tools(include_private=user is not None)
