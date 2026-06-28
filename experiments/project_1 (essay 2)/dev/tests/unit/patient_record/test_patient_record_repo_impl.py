from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.database import Base
from src.dto.patient_record.patient_record_dto import PatientRecordCreate, PatientRecordUpdate, PatientRecordResponse
from src.orm.patient_record.patient_record_orm import PatientRecordORM
from src.infra.patient_record.patient_record_repo_impl import SQLAlchemyPatientRecordRepository


@pytest.fixture(scope="module")
def engine():
    e = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=e)
    yield e
    Base.metadata.drop_all(bind=e)


@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    s = SessionLocal()
    yield s
    s.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def repo(session: Session):
    return SQLAlchemyPatientRecordRepository(session)


class TestSQLAlchemyPatientRecordRepository:
    def test_create_and_get_by_id(self, repo, session):
        data = PatientRecordCreate(owner_id=1)
        created = repo.create(data)
        assert created.id is not None
        assert created.owner_id == 1

        fetched = repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.owner_id == 1

    def test_get_by_id_not_found(self, repo):
        assert repo.get_by_id(999) is None

    def test_get_all_empty(self, repo):
        assert repo.get_all(skip=0, limit=100) == []

    def test_get_all(self, repo):
        repo.create(PatientRecordCreate(owner_id=10))
        repo.create(PatientRecordCreate(owner_id=20))
        all_records = repo.get_all()
        assert len(all_records) == 2

    def test_update(self, repo):
        created = repo.create(PatientRecordCreate(owner_id=1))
        updated = repo.update(created.id, PatientRecordUpdate(owner_id=2))
        assert updated is not None
        assert updated.owner_id == 2

    def test_update_returns_none_for_missing(self, repo):
        result = repo.update(999, PatientRecordUpdate(owner_id=2))
        assert result is None

    def test_delete(self, repo):
        created = repo.create(PatientRecordCreate(owner_id=1))
        assert repo.delete(created.id) is True
        assert repo.get_by_id(created.id) is None

    def test_delete_returns_false_for_missing(self, repo):
        assert repo.delete(999) is False

    def test_get_all_pagination(self, repo):
        for i in range(5):
            repo.create(PatientRecordCreate(owner_id=i))
        page1 = repo.get_all(skip=0, limit=2)
        assert len(page1) == 2
        page2 = repo.get_all(skip=2, limit=2)
        assert len(page2) == 2
