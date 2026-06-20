from dataclasses import FrozenInstanceError

import pytest

from web_suffer.contexts.auth.domain.value_objects import PasswordHash


def test_construction_and_value_access() -> None:
    ph = PasswordHash(value="hashed_password_123")
    assert ph.value == "hashed_password_123"


def test_empty_string_allowed() -> None:
    ph = PasswordHash(value="")
    assert ph.value == ""  # noqa: PLC1901


def test_long_hash() -> None:
    long_hash = "a" * 10_000
    ph = PasswordHash(value=long_hash)
    assert ph.value == long_hash


def test_equality_same_value() -> None:
    a = PasswordHash(value="abc123")
    b = PasswordHash(value="abc123")
    assert a == b


def test_equality_different_value() -> None:
    a = PasswordHash(value="abc123")
    b = PasswordHash(value="xyz789")
    assert a != b


def test_equality_different_type() -> None:
    ph = PasswordHash(value="abc123")
    assert ph != "abc123"  # type: ignore[comparison-overlap]
    assert ph != 123  # type: ignore[comparison-overlap]  # noqa: PLR2004
    assert ph != None  # noqa: E711


def test_hashable_in_set() -> None:
    a = PasswordHash(value="hash1")
    b = PasswordHash(value="hash2")
    c = PasswordHash(value="hash1")
    assert len({a, b, c}) == 2  # noqa: PLR2004


def test_hashable_as_dict_key() -> None:
    ph = PasswordHash(value="secret")
    assert {ph: "ok"}[ph] == "ok"


def test_hash_consistent_with_eq() -> None:
    a = PasswordHash(value="same")
    b = PasswordHash(value="same")
    assert hash(a) == hash(b)


def test_immutable_value() -> None:
    ph = PasswordHash(value="original")
    with pytest.raises(FrozenInstanceError):
        ph.value = "tampered"  # type: ignore[misc]


def test_no_dynamic_attributes() -> None:
    ph = PasswordHash(value="hash")
    with pytest.raises((AttributeError, TypeError)):
        ph.salt = "extra"  # type: ignore[attr-defined]


def test_repr_contains_value() -> None:
    ph = PasswordHash(value="myhash")
    repr_str = repr(ph)
    assert "PasswordHash" in repr_str
    assert "myhash" in repr_str
