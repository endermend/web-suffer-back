import uuid

import pytest

from web_suffer.shared.domain.value_objects.base_id import BaseID


def test_user_id_fields() -> None:
    uuid_4 = uuid.uuid4()
    uid = BaseID(value=uuid_4)

    assert uid.value == uuid_4


def test_generate_different_ids() -> None:
    assert BaseID.new() != BaseID.new()


def test_from_str_valid() -> None:
    uuid_4 = uuid.uuid4()
    uid = BaseID.from_str(uuid_str=str(uuid_4))

    assert uid.value == uuid_4


def test_from_str_invalid() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        BaseID.from_str("not-a-uuid")


def test_eq_same_value() -> None:
    uuid_4 = uuid.uuid4()
    assert BaseID(value=uuid_4) == BaseID(value=uuid_4)


def test_immutable() -> None:
    uid = BaseID.new()
    with pytest.raises(AttributeError):
        uid.value = uuid.uuid4()  # ty:ignore[invalid-assignment] # pyrefly: ignore [read-only]


def test_from_str_roundtrip() -> None:
    uid = BaseID.new()
    assert BaseID.from_str(str(uid.value)) == uid


def test_hashable() -> None:
    uid = BaseID.new()
    assert {uid: "ok"}[uid] == "ok"
