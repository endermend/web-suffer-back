import pytest

from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus


@pytest.mark.parametrize(
    ("constant", "expected_value"),
    [
        (SubmissionStatus.PENDING, "pending"),
        (SubmissionStatus.ACCEPTED, "accepted"),
        (SubmissionStatus.REJECTED, "rejected"),
    ],
)
def test_class_var_constants(constant: SubmissionStatus, expected_value: str) -> None:
    assert constant.value == expected_value


def test_constants_are_instances() -> None:
    assert isinstance(SubmissionStatus.PENDING, SubmissionStatus)
    assert isinstance(SubmissionStatus.ACCEPTED, SubmissionStatus)
    assert isinstance(SubmissionStatus.REJECTED, SubmissionStatus)


def test_constructor_accepts_arbitrary_string() -> None:
    custom = SubmissionStatus("custom")  # type: ignore[arg-type]
    assert custom.value == "custom"  # type: ignore[comparison-overlap]


def test_is_pending_true() -> None:
    assert SubmissionStatus.PENDING.is_pending() is True


def test_is_pending_false_for_accepted() -> None:
    assert SubmissionStatus.ACCEPTED.is_pending() is False


def test_is_pending_false_for_rejected() -> None:
    assert SubmissionStatus.REJECTED.is_pending() is False


def test_is_pending_false_for_unknown() -> None:
    custom = SubmissionStatus("unknown")  # type: ignore[arg-type]
    assert custom.is_pending() is False


def test_eq_same_value() -> None:
    assert SubmissionStatus("pending") == SubmissionStatus.PENDING


def test_eq_different_value() -> None:
    assert SubmissionStatus.PENDING != SubmissionStatus.ACCEPTED


def test_hashable_in_set() -> None:
    s = {SubmissionStatus.PENDING, SubmissionStatus.ACCEPTED, SubmissionStatus.PENDING}
    assert len(s) == 2  # noqa: PLR2004


def test_hashable_as_dict_key() -> None:
    assert {SubmissionStatus.PENDING: "ok"}[SubmissionStatus.PENDING] == "ok"


def test_hash_consistent_with_eq() -> None:
    assert hash(SubmissionStatus("pending")) == hash(SubmissionStatus.PENDING)


def test_immutable_value() -> None:
    status = SubmissionStatus.PENDING
    with pytest.raises(AttributeError):
        status.value = "hacked"  # type: ignore[misc, assignment] # pyrefly: ignore [read-only]


def test_repr_does_not_crash() -> None:
    status = SubmissionStatus.PENDING
    repr_str = repr(status)
    assert isinstance(repr_str, str)
    assert "pending" in repr_str or "SubmissionStatus" in repr_str
