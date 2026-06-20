import pytest

from web_suffer.shared.domain.exceptions import DomainError
from web_suffer.shared.domain.value_objects.user_role import UserRole


@pytest.mark.parametrize(
    ("constant", "expected_value"),
    [
        (UserRole.USER, "user"),
        (UserRole.ADMIN, "admin"),
        (UserRole.MODERATOR, "moderator"),
    ],
)
def test_class_var_constants(constant: UserRole, expected_value: str) -> None:
    assert constant.value == expected_value


def test_constants_are_instances() -> None:
    assert isinstance(UserRole.USER, UserRole)
    assert isinstance(UserRole.ADMIN, UserRole)
    assert isinstance(UserRole.MODERATOR, UserRole)


def test_constructor_accepts_arbitrary_string() -> None:
    custom = UserRole("superadmin")
    assert custom.value == "superadmin"


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("user", UserRole.USER),
        ("admin", UserRole.ADMIN),
        ("moderator", UserRole.MODERATOR),
    ],
)
def test_from_str_valid(input_str: str, expected: UserRole) -> None:
    result = UserRole.from_str(input_str)  # type: ignore[arg-type]
    assert result == expected
    assert result.value == expected.value


def test_from_str_invalid_raises_domain_error() -> None:
    with pytest.raises(DomainError):
        UserRole.from_str("unknown")  # type: ignore[arg-type]


def test_from_str_empty_raises_domain_error() -> None:
    with pytest.raises(DomainError):
        UserRole.from_str("")  # type: ignore[arg-type]


def test_from_str_case_sensitive() -> None:
    with pytest.raises(DomainError):
        UserRole.from_str("User")  # type: ignore[arg-type]
    with pytest.raises(DomainError):
        UserRole.from_str("ADMIN")  # type: ignore[arg-type]
    with pytest.raises(DomainError):
        UserRole.from_str("Moderator")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("role", "expected_str"),
    [
        (UserRole.USER, "user"),
        (UserRole.ADMIN, "admin"),
        (UserRole.MODERATOR, "moderator"),
    ],
)
def test_to_str_valid(role: UserRole, expected_str: str) -> None:
    assert role.to_str() == expected_str


def test_to_str_unknown_value_raises_domain_error() -> None:
    custom = UserRole("superadmin")
    with pytest.raises(DomainError):
        custom.to_str()


def test_roundtrip_from_str_to_str() -> None:
    assert UserRole.from_str("user").to_str() == "user"
    assert UserRole.from_str("admin").to_str() == "admin"
    assert UserRole.from_str("moderator").to_str() == "moderator"


def test_roundtrip_to_str_from_str() -> None:
    assert UserRole.from_str(UserRole.USER.to_str()) == UserRole.USER
    assert UserRole.from_str(UserRole.ADMIN.to_str()) == UserRole.ADMIN
    assert UserRole.from_str(UserRole.MODERATOR.to_str()) == UserRole.MODERATOR


def test_eq_same_value() -> None:
    assert UserRole("user") == UserRole.USER
    assert UserRole("admin") == UserRole.ADMIN
    assert UserRole("moderator") == UserRole.MODERATOR


def test_eq_different_value() -> None:
    assert UserRole.USER != UserRole.ADMIN
    assert UserRole.ADMIN != UserRole.MODERATOR
    assert UserRole.USER != UserRole.MODERATOR


def test_hashable() -> None:
    assert {UserRole.USER: "user"}[UserRole.USER] == "user"
    assert {UserRole.ADMIN: "admin"}[UserRole.ADMIN] == "admin"
    assert {UserRole.MODERATOR: "moderator"}[UserRole.MODERATOR] == "moderator"


def test_hash_consistent_with_eq() -> None:
    assert hash(UserRole("user")) == hash(UserRole.USER)
    assert hash(UserRole("admin")) == hash(UserRole.ADMIN)
    assert hash(UserRole("moderator")) == hash(UserRole.MODERATOR)


def test_immutable() -> None:
    role = UserRole.USER
    with pytest.raises(AttributeError):
        role.value = "hacker"  # ty:ignore[invalid-assignment] # pyrefly: ignore [read-only]


def test_from_str_whitespace_raises_domain_error() -> None:
    with pytest.raises(DomainError):
        UserRole.from_str(" user")  # type: ignore[arg-type]
    with pytest.raises(DomainError):
        UserRole.from_str("user ")  # type: ignore[arg-type]


def test_from_str_none_raises_type_error() -> None:
    with pytest.raises(DomainError):
        UserRole.from_str(None)  # type: ignore[arg-type]
