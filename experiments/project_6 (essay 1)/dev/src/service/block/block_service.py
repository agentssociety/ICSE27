from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.block.block_dto import BlockCreate, BlockUpdate, BlockResponse

if TYPE_CHECKING:
    from src.infra.block.block_repo_impl import SQLAlchemyBlockRepository


class BlockService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[BlockResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[BlockResponse]: ...
    def create(self, data: BlockCreate) -> BlockResponse: ...
    def update(self, item_id: int, data: BlockUpdate) -> Optional[BlockResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class BlockServiceImpl:
    def __init__(self, repo: SQLAlchemyBlockRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[BlockResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BlockResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: BlockCreate) -> BlockResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: BlockUpdate) -> Optional[BlockResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

