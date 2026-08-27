from app.repositories import nav_user_repository


def login(username: str, password: str):
    """导航站登录（账号仅在代码中添加）"""
    return nav_user_repository.verify(username, password)
