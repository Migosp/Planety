from app.repositories import nav_user_repository


def login(username: str, password: str):
    """导航站登录"""
    return nav_user_repository.verify(username, password)


def register(username: str, password: str) -> tuple:
    """导航站注册"""
    if len(username) < 2:
        return False, "用户名至少2个字符", None
    if len(password) < 6:
        return False, "密码至少6个字符", None
    return nav_user_repository.create(username, password)
