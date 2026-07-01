from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Post domain class

Package: orm.post
Layer: orm
Related tasks: #159, #160, #161, #162, #167, #169, #170, #171, #172, #178
Requirement coverage:
- User can create a text post and optionally upload images
- User can like and unlike a post
- Add, edit, and delete comments on posts
- Display News Feed Sorted by Time
- Group Post Feed Filter
"""


class PostORM(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    authorId: Mapped[str] = mapped_column(String, nullable=False)
    textContent: Mapped[str] = mapped_column(String, nullable=False)
