from web_suffer.contexts.auth.domain.entities import User
from web_suffer.contexts.auth.domain.value_objects import PasswordHash, UserEmail
from web_suffer.shared.domain.value_objects import UserID
from web_suffer.shared.domain.value_objects.user_role import UserRole


def test_user_fields() -> None:
    uid = UserID.new()
    email = UserEmail("user@example.com")
    password_hash = PasswordHash("ph")

    user = User.register(
        id=uid,
        email=email,
        password_hash=password_hash,
        role=UserRole.USER,
    )

    assert user.id == uid
    assert user.email == email
    assert user.password_hash == password_hash


def test_eq_same_id() -> None:
    uid = UserID.new()
    u1 = User.register(
        id=uid,
        email=UserEmail("u1@example.com"),
        password_hash=PasswordHash("u1"),
        role=UserRole.USER,
    )
    u2 = User.register(
        id=uid,
        email=UserEmail("u2@example.com"),
        password_hash=PasswordHash("u2"),
        role=UserRole.USER,
    )
    assert u1 == u2


def test_eq_different_id() -> None:
    u1 = User.register(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
        role=UserRole.USER,
    )
    u2 = User.register(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
        role=UserRole.USER,
    )
    assert u1 != u2


def test_eq_not_implemented_for_other_types() -> None:
    u = User.register(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
        role=UserRole.USER,
    )
    result = u.__eq__("not a user")  # noqa: PLC2801
    assert result is NotImplemented


def test_hash_same_id() -> None:
    uid = UserID.new()
    u1 = User.register(
        id=uid,
        email=UserEmail("u1@example.com"),
        password_hash=PasswordHash("ph1"),
        role=UserRole.USER,
    )
    u2 = User.register(
        id=uid,
        email=UserEmail("u2@example.com"),
        password_hash=PasswordHash("ph1"),
        role=UserRole.USER,
    )
    assert hash(u1) == hash(u2)


def test_hash_different_id() -> None:
    u1 = User.register(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
        role=UserRole.USER,
    )
    u2 = User.register(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
        role=UserRole.USER,
    )
    assert hash(u1) != hash(u2)
