import pytest

from web_suffer.contexts.auth.domain.types import UserStatusType
from web_suffer.shared.domain.exceptions import DomainError
from web_suffer.shared.domain.value_objects.user_status import UserStatus


@pytest.mark.parametrize(
    ("constant", "expected_value"),
    [
        (UserStatus.ACTIVE, 0),
        (UserStatus.BANNED, 1),
        (UserStatus.DELETED, 2),
    ],
)
def test_class_var_constants(constant: UserStatus, expected_value: int) -> None:
    assert constant.value == expected_value


def test_constants_are_instances() -> None:
    assert isinstance(UserStatus.ACTIVE, UserStatus)
    assert isinstance(UserStatus.BANNED, UserStatus)
    assert isinstance(UserStatus.DELETED, UserStatus)


def test_constructor_accepts_arbitrary_int() -> None:
    custom = UserStatus(42)
    assert custom.value == 42  # noqa: PLR2004


def test_is_active_returns_true_for_active() -> None:
    assert UserStatus.ACTIVE.is_active() is True


def test_is_active_returns_false_for_banned() -> None:
    assert UserStatus.BANNED.is_active() is False


def test_is_active_returns_false_for_deleted() -> None:
    assert UserStatus.DELETED.is_active() is False


def test_is_active_returns_false_for_unknown_value() -> None:
    custom = UserStatus(999)
    assert custom.is_active() is False


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("active", UserStatus.ACTIVE),
        ("banned", UserStatus.BANNED),
        ("deleted", UserStatus.DELETED),
    ],
)
def test_from_str_valid(input_str: UserStatusType, expected: UserStatus) -> None:
    result = UserStatus.from_str(input_str)
    assert result == expected
    assert result.value == expected.value


def test_from_str_invalid_raises_domain_error() -> None:
    with pytest.raises(DomainError):
        UserStatus.from_str("unknown")  # type: ignore[arg-type]


def test_from_str_empty_raises_domain_error() -> None:
    with pytest.raises(DomainError):
        UserStatus.from_str("")  # type: ignore[arg-type]


def test_from_str_case_sensitive() -> None:
    with pytest.raises(DomainError):
        UserStatus.from_str("Active")  # type: ignore[arg-type]
    with pytest.raises(DomainError):
        UserStatus.from_str("ACTIVE")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("status", "expected_str"),
    [
        (UserStatus.ACTIVE, "active"),
        (UserStatus.BANNED, "banned"),
        (UserStatus.DELETED, "deleted"),
    ],
)
def test_to_str_valid(status: UserStatus, expected_str: str) -> None:
    assert status.to_str() == expected_str


def test_to_str_unknown_value_raises_domain_error() -> None:
    custom = UserStatus(999)
    with pytest.raises(DomainError):
        custom.to_str()


def test_roundtrip_from_str_to_str() -> None:
    assert UserStatus.from_str("active").to_str() == "active"
    assert UserStatus.from_str("banned").to_str() == "banned"
    assert UserStatus.from_str("deleted").to_str() == "deleted"


def test_roundtrip_to_str_from_str() -> None:
    assert UserStatus.from_str(UserStatus.ACTIVE.to_str()) == UserStatus.ACTIVE
    assert UserStatus.from_str(UserStatus.BANNED.to_str()) == UserStatus.BANNED
    assert UserStatus.from_str(UserStatus.DELETED.to_str()) == UserStatus.DELETED


def test_eq_same_value() -> None:
    assert UserStatus(0) == UserStatus.ACTIVE
    assert UserStatus(1) == UserStatus.BANNED
    assert UserStatus(2) == UserStatus.DELETED


def test_eq_different_value() -> None:
    assert UserStatus.ACTIVE != UserStatus.BANNED
    assert UserStatus.BANNED != UserStatus.DELETED
    assert UserStatus.ACTIVE != UserStatus.DELETED


def test_hashable() -> None:
    assert {UserStatus.ACTIVE: "active"}[UserStatus.ACTIVE] == "active"
    assert {UserStatus.BANNED: "banned"}[UserStatus.BANNED] == "banned"
    assert {UserStatus.DELETED: "deleted"}[UserStatus.DELETED] == "deleted"


def test_hash_consistent_with_eq() -> None:
    assert hash(UserStatus(0)) == hash(UserStatus.ACTIVE)
    assert hash(UserStatus(1)) == hash(UserStatus.BANNED)
    assert hash(UserStatus(2)) == hash(UserStatus.DELETED)


def test_immutable() -> None:
    status = UserStatus.ACTIVE
    with pytest.raises(AttributeError):
        status.value = 999  # ty:ignore[invalid-assignment] # pyrefly: ignore [read-only]
