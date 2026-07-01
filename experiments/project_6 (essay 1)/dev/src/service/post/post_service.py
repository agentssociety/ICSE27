from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infra.post.post_repo_impl import SQLAlchemyPostRepository


class PostService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[Any]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Any]: ...
    def create(self, data: Any) -> Any: ...
    def update(self, item_id: int, data: Any) -> Optional[Any]: ...
    def delete(self, item_id: int) -> bool: ...

    def create_with_images(self, author_id: str, text_content: str, image_urls: list[str]) -> None: ...


class PostServiceImpl:
    def __init__(self, repo: SQLAlchemyPostRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[Any]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Any]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: Any) -> Any:
        return self._repo.create(data)

    def update(self, item_id: int, data: Any) -> Optional[Any]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)