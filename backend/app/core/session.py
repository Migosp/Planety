"""导航站会话序列化工具（仅提供签名 serializer，评分工具 session 已在独立项目）"""
from itsdangerous import URLSafeSerializer

from app.core.config import SECRET_KEY


serializer = URLSafeSerializer(SECRET_KEY)
