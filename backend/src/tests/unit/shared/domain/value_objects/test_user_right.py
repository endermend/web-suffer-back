from dataclasses import FrozenInstanceError

import pytest

from web_suffer.shared.domain.value_objects.user_right import UserRight
from web_suffer.shared.domain.value_objects.user_role import UserRole
from web_suffer.shared.domain.value_objects.user_status import UserStatus


def test_all_constant() -> None:
    assert UserRight.ALL == "*"


def test_construction_all_all() -> None:
    right = UserRight(roles="*", statuses="*")
    assert right.roles == "*"
    assert right.statuses == "*"


def test_construction_specific_roles_all_statuses() -> None:
    right = UserRight(roles={UserRole.ADMIN}, statuses="*")
    assert right.roles == {UserRole.ADMIN}
    assert right.statuses == "*"


def test_construction_all_roles_specific_statuses() -> None:
    right = UserRight(roles="*", statuses={UserStatus.ACTIVE})
    assert right.roles == "*"
    assert right.statuses == {UserStatus.ACTIVE}


def test_construction_specific_both() -> None:
    right = UserRight(
        roles={UserRole.USER, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE, UserStatus.BANNED},
    )
    assert right.roles == {UserRole.USER, UserRole.MODERATOR}
    assert right.statuses == {UserStatus.ACTIVE, UserStatus.BANNED}


def test_invalid_empty_roles_raises() -> None:
    with pytest.raises(ValueError, match="At least one role required"):
        UserRight(roles=set(), statuses={UserStatus.ACTIVE})


def test_invalid_empty_statuses_raises() -> None:
    with pytest.raises(ValueError, match="At least one status required"):
        UserRight(roles={UserRole.USER}, statuses=set())


def test_invalid_both_empty_roles_checked_first() -> None:
    with pytest.raises(ValueError, match="At least one role required"):
        UserRight(roles=set(), statuses=set())


def test_satisfied_all_all() -> None:
    right = UserRight(roles="*", statuses="*")
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is True
    assert right.is_satisfied_by(UserRole.ADMIN, UserStatus.DELETED) is True


def test_satisfied_specific_role_any_status() -> None:
    right = UserRight(roles={UserRole.ADMIN}, statuses="*")
    assert right.is_satisfied_by(UserRole.ADMIN, UserStatus.BANNED) is True
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is False


def test_satisfied_any_role_specific_status() -> None:
    right = UserRight(roles="*", statuses={UserStatus.ACTIVE})
    assert right.is_satisfied_by(UserRole.MODERATOR, UserStatus.ACTIVE) is True
    assert right.is_satisfied_by(UserRole.ADMIN, UserStatus.DELETED) is False


def test_satisfied_specific_both_match() -> None:
    right = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is True


def test_satisfied_role_mismatch() -> None:
    right = UserRight(roles={UserRole.ADMIN}, statuses={UserStatus.ACTIVE})
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is False


def test_satisfied_status_mismatch() -> None:
    right = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    assert right.is_satisfied_by(UserRole.USER, UserStatus.BANNED) is False


def test_satisfied_both_mismatch() -> None:
    right = UserRight(roles={UserRole.ADMIN}, statuses={UserStatus.DELETED})
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is False


def test_satisfied_multiple_roles_and_statuses() -> None:
    right = UserRight(
        roles={UserRole.USER, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE, UserStatus.BANNED},
    )
    assert right.is_satisfied_by(UserRole.USER, UserStatus.ACTIVE) is True
    assert right.is_satisfied_by(UserRole.MODERATOR, UserStatus.BANNED) is True
    assert right.is_satisfied_by(UserRole.ADMIN, UserStatus.ACTIVE) is False
    assert right.is_satisfied_by(UserRole.USER, UserStatus.DELETED) is False


def test_equality_same_components() -> None:
    a = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    b = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    assert a == b
    assert hash(a) == hash(b)


def test_equality_different_roles() -> None:
    a = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    b = UserRight(roles={UserRole.ADMIN}, statuses={UserStatus.ACTIVE})
    assert a != b


def test_equality_different_statuses() -> None:
    a = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    b = UserRight(roles={UserRole.USER}, statuses={UserStatus.BANNED})
    assert a != b


def test_hashable_in_set() -> None:
    right = UserRight(roles="*", statuses="*")
    assert {right} == {right}


def test_hashable_as_dict_key() -> None:
    right = UserRight(roles={UserRole.ADMIN}, statuses={UserStatus.ACTIVE})
    assert {right: "ok"}[right] == "ok"


def test_immutable_roles() -> None:
    right = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    with pytest.raises(FrozenInstanceError):
        right.roles = {UserRole.ADMIN}  # type: ignore[misc]


def test_immutable_statuses() -> None:
    right = UserRight(roles={UserRole.USER}, statuses={UserStatus.ACTIVE})
    with pytest.raises(FrozenInstanceError):
        right.statuses = {UserStatus.BANNED}  # type: ignore[misc]


def test_no_unexpected_attributes() -> None:
    right = UserRight(roles="*", statuses="*")
    with pytest.raises((AttributeError, TypeError)):
        right.unknown_field = 42  # type: ignore[attr-defined]
