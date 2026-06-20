import pytest

from web_suffer.contexts.auth.domain.value_objects.token import Token


def test_construction_and_value_access() -> None:
    token = Token(value="abc123.def456.ghi789")
    assert token.value == "abc123.def456.ghi789"


def test_empty_string_allowed() -> None:
    token = Token(value="")
    assert token.value == ""  # noqa: PLC1901


def test_long_token() -> None:
    long_token = "x" * 10_000
    token = Token(value=long_token)
    assert token.value == long_token


# === Equality ===


def test_equality_same_value() -> None:
    a = Token(value="same")
    b = Token(value="same")
    assert a == b


def test_equality_different_value() -> None:
    a = Token(value="aaa")
    b = Token(value="bbb")
    assert a != b


def test_hashable_in_set() -> None:
    a = Token(value="t1")
    b = Token(value="t2")
    c = Token(value="t1")
    assert len({a, b, c}) == 2  # noqa: PLR2004


def test_hashable_as_dict_key() -> None:
    token = Token(value="key")
    assert {token: "ok"}[token] == "ok"


def test_hash_consistent_with_eq() -> None:
    a = Token(value="consistent")
    b = Token(value="consistent")
    assert hash(a) == hash(b)


def test_immutable_value() -> None:
    token = Token(value="original")
    with pytest.raises(AttributeError):
        token.value = "tampered"  # pyrefly: ignore [read-only]


def test_repr_does_not_crash() -> None:
    token = Token(value="mytoken")
    repr_str = repr(token)
    assert isinstance(repr_str, str)
    assert "mytoken" in repr_str or "Token" in repr_str


def test_copy_via_constructor() -> None:
    original = Token(value="secret")
    copy = Token(value=original.value)
    assert original == copy
    assert original is not copy
