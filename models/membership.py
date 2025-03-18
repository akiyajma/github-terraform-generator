from pydantic import BaseModel, Field


class Membership(BaseModel):
    """
    GitHub Membership のモデル

    Attributes:
        username (str): ユーザー名。
        role (str): メンバーシップの役割 ("member" または "admin")。
        allow_delete (bool): 削除可能かどうかのフラグ。デフォルトは False。
    """
    username: str
    role: str = Field(..., pattern="^(member|admin)$")
    allow_delete: bool = False
