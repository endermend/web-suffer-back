from dataclasses import FrozenInstanceError

import pytest

from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair


def test_construction_and_field_access() -> None:
    access = Token(value="access_123")
    refresh = Token(value="refresh_456")
    pair = TokenPair(access_token=access, refresh_token=refresh)

    assert pair.access_token == access
    assert pair.refresh_token == refresh


def test_same_access_and_refresh_allowed() -> None:
    same = Token(value="same")
    pair = TokenPair(access_token=same, refresh_token=same)
    assert pair.access_token is pair.refresh_token


def test_empty_tokens_allowed() -> None:
    empty = Token(value="")
    pair = TokenPair(access_token=empty, refresh_token=empty)
    assert pair.access_token.value == ""  # noqa: PLC1901
    assert pair.refresh_token.value == ""  # noqa: PLC1901


# === _get_equality_components ===

def test_equality_components() -> None:
    access = Token(value="a")
    refresh = Token(value="b")
    pair = TokenPair(access_token=access, refresh_token=refresh)
    assert pair._get_equality_components() == (access, refresh)  # noqa: SLF001


def test_equality_same_tokens() -> None:
    a = TokenPair(access_token=Token("acc"), refresh_token=Token("ref"))
    b = TokenPair(access_token=Token("acc"), refresh_token=Token("ref"))
    assert a == b
    assert a is not b


def test_equality_different_access() -> None:
    a = TokenPair(access_token=Token("a1"), refresh_token=Token("ref"))
    b = TokenPair(access_token=Token("a2"), refresh_token=Token("ref"))
    assert a != b


def test_equality_different_refresh() -> None:
    a = TokenPair(access_token=Token("acc"), refresh_token=Token("r1"))
    b = TokenPair(access_token=Token("acc"), refresh_token=Token("r2"))
    assert a != b


def test_hashable_in_set() -> None:
    a = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    b = TokenPair(access_token=Token("c"), refresh_token=Token("d"))
    c = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    assert len({a, b, c}) == 2  # noqa: PLR2004


def test_hashable_as_dict_key() -> None:
    pair = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    assert {pair: "ok"}[pair] == "ok"


def test_hash_consistent_with_eq() -> None:
    a = TokenPair(access_token=Token("x"), refresh_token=Token("y"))
    b = TokenPair(access_token=Token("x"), refresh_token=Token("y"))
    assert hash(a) == hash(b)


def test_immutable_access_token() -> None:
    pair = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    with pytest.raises(FrozenInstanceError):
        pair.access_token = Token("tampered")  # type: ignore[misc]


def test_immutable_refresh_token() -> None:
    pair = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    with pytest.raises(FrozenInstanceError):
        pair.refresh_token = Token("tampered")  # type: ignore[misc]


def test_no_dynamic_attributes() -> None:
    pair = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    with pytest.raises((AttributeError, TypeError)):
        pair.extra = "nope"  # type: ignore[attr-defined]


def test_repr_contains_class_name() -> None:
    pair = TokenPair(access_token=Token("a"), refresh_token=Token("b"))
    repr_str = repr(pair)
    assert "TokenPair" in repr_str
