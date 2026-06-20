import pytest

from web_suffer.contexts.auth.domain.exceptions import InvalidEmailError
from web_suffer.contexts.auth.domain.value_objects import UserEmail


def test_construction_valid_email() -> None:
    email = UserEmail(value="user@example.com")
    assert email.value == "user@example.com"


def test_normalization_lowercase() -> None:
    email = UserEmail(value="USER@EXAMPLE.COM")
    assert email.value == "user@example.com"


def test_normalization_strip_whitespace() -> None:
    email = UserEmail(value="  user@example.com  ")
    assert email.value == "user@example.com"


def test_normalization_both() -> None:
    email = UserEmail(value="  USER@EXAMPLE.COM  ")
    assert email.value == "user@example.com"


@pytest.mark.parametrize(
    "raw_email",
    [
        "simple@example.com",
        "very.common@example.com",
        "disposable.style.stripe.with+symbol@example.com",
        "other.email-with-hyphen@example.com",
        "user.name+tag+sorting@example.com",
        "xx@example.com",
        "example-indeed@strange-example.com",
        "user.name@example.co.uk",
        "123@example.com",
        "a88@bozo.co",
    ],
)
def test_valid_emails_accepted(raw_email: str) -> None:
    email = UserEmail(value=raw_email)
    assert email.value == raw_email.strip().lower()


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "   ",
        "plainaddress",
        "@missinglocal.com",
        "missing@domain",
        "missing@.com",
        "missing@domain..com",
        "double..dots@example.com",
        "spaces in@example.com",
        "missing@domain.c",  # TLD too short
        "@example.com",
        "user@",
        "user@.com",
        "user@domain,com",
        "user@domain_com",
        "user name@example.com",
        "user@domain .com",
        "user@-domain.com",
        "user@domain-.com",
        "user@domain.com-",
        ".leadingdot@example.com",
        "trailingdot.@example.com",
    ],
)
def test_invalid_emails_rejected(invalid_email: str) -> None:
    with pytest.raises(InvalidEmailError):
        UserEmail(value=invalid_email)


def test_error_preserves_original_value() -> None:
    bad = "not-an-email"
    with pytest.raises(InvalidEmailError) as exc_info:
        UserEmail(value=bad)
    assert bad in str(exc_info.value) or exc_info.value.args[0] == bad


def test_equality_same_normalized_value() -> None:
    a = UserEmail(value="User@Example.COM")
    b = UserEmail(value="  user@example.com  ")
    assert a == b
    assert a.value == b.value


def test_equality_different_value() -> None:
    a = UserEmail(value="a2025@example.com")
    b = UserEmail(value="b200@example.com")
    assert a != b


def test_equality_different_type() -> None:
    email = UserEmail(value="user@example.com")
    assert email != "user@example.com"
    assert email != 42  # noqa: PLR2004


def test_hashable_in_set() -> None:
    a = UserEmail(value="user@example.com")
    b = UserEmail(value="USER@EXAMPLE.COM")
    assert len({a, b}) == 1  # same after normalization


def test_hashable_as_dict_key() -> None:
    email = UserEmail(value="user@example.com")
    assert {email: "ok"}[email] == "ok"


def test_hash_consistent_after_normalization() -> None:
    a = UserEmail(value="ABBA@Bo.COM")
    b = UserEmail(value="  abba@bo.com  ")
    assert hash(a) == hash(b)


def test_immutable_after_construction() -> None:
    email = UserEmail(value="user@example.com")
    with pytest.raises(AttributeError):
        email.value = "other@example.com"  # type: ignore[misc]  # pyrefly: ignore [read-only]


# === Repr ===

def test_repr_does_not_crash() -> None:
    email = UserEmail(value="user@example.com")
    repr_str = repr(email)
    assert isinstance(repr_str, str)
    assert "user@example.com" in repr_str or "UserEmail" in repr_str
