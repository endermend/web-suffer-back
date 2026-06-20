from pathlib import Path

import pytest

from web_suffer.contexts.tasks.domain.value_objects.submission_file import SubmissionFile


def test_empty_constant() -> None:
    assert SubmissionFile.EMPTY.value is None
    assert SubmissionFile.EMPTY.does_have_file() is False


def test_empty_is_instance() -> None:
    assert isinstance(SubmissionFile.EMPTY, SubmissionFile)


def test_construction_with_path() -> None:
    p = Path("solutions/main.py")
    sf = SubmissionFile(value=p)
    assert sf.value == p


def test_construction_with_none() -> None:
    sf = SubmissionFile(value=None)
    assert sf.value is None
    assert sf.does_have_file() is False


def test_construction_with_absolute_path() -> None:
    p = Path("/home/user/solution.py")
    sf = SubmissionFile(value=p)
    assert sf.value == p
    assert sf.does_have_file() is True


def test_from_str_simple() -> None:
    sf = SubmissionFile.from_str("solutions/main.py")
    assert isinstance(sf.value, Path)
    assert sf.value == Path("solutions/main.py")


def test_from_str_absolute() -> None:
    sf = SubmissionFile.from_str("/var/data/file.txt")
    assert sf.value == Path("/var/data/file.txt")


def test_from_str_with_dots() -> None:
    sf = SubmissionFile.from_str("../relative/path.py")
    assert sf.value == Path("../relative/path.py")


def test_from_str_with_spaces() -> None:
    sf = SubmissionFile.from_str("my folder/my file.py")
    assert sf.value == Path("my folder/my file.py")


def test_from_str_empty_string() -> None:
    sf = SubmissionFile.from_str("")
    assert sf.value == Path()


def test_from_str_returns_different_instances() -> None:
    a = SubmissionFile.from_str("a.py")
    b = SubmissionFile.from_str("a.py")
    assert a == b
    assert a is not b


def test_does_have_file_true() -> None:
    sf = SubmissionFile(value=Path("file.py"))
    assert sf.does_have_file() is True


def test_does_have_file_false() -> None:
    sf = SubmissionFile(value=None)
    assert sf.does_have_file() is False


def test_does_have_file_empty_constant() -> None:
    assert SubmissionFile.EMPTY.does_have_file() is False


def test_equality_same_path() -> None:
    a = SubmissionFile(value=Path("a.py"))
    b = SubmissionFile(value=Path("a.py"))
    assert a == b


def test_equality_same_none() -> None:
    a = SubmissionFile(value=None)
    b = SubmissionFile(value=None)
    assert a == b


def test_equality_different_paths() -> None:
    a = SubmissionFile(value=Path("a.py"))
    b = SubmissionFile(value=Path("b.py"))
    assert a != b


def test_equality_path_vs_none() -> None:
    a = SubmissionFile(value=Path("a.py"))
    b = SubmissionFile(value=None)
    assert a != b


def test_hashable_with_path() -> None:
    sf = SubmissionFile(value=Path("a.py"))
    assert {sf: "ok"}[sf] == "ok"


def test_hashable_none() -> None:
    sf = SubmissionFile(value=None)
    assert {sf: "ok"}[sf] == "ok"


def test_hash_consistent_with_eq() -> None:
    a = SubmissionFile(value=Path("x.py"))
    b = SubmissionFile(value=Path("x.py"))
    assert hash(a) == hash(b)


def test_immutable_value() -> None:
    sf = SubmissionFile(value=Path("a.py"))
    with pytest.raises(AttributeError):
        sf.value = Path("b.py")  # type: ignore[misc] # pyrefly: ignore [read-only]


def test_path_methods_still_work() -> None:
    sf = SubmissionFile.from_str("folder/file.py")
    assert sf.value is not None
    assert sf.value.name == "file.py"
    assert sf.value.parent == Path("folder")


def test_path_suffix() -> None:
    sf = SubmissionFile.from_str("solution.py")
    assert sf.value is not None
    assert sf.value.suffix == ".py"


def test_path_is_absolute() -> None:
    sf = SubmissionFile.from_str("/absolute/path.py")
    assert sf.value is not None


def test_path_is_relative() -> None:
    sf = SubmissionFile.from_str("relative/path.py")
    assert sf.value is not None
    assert sf.value.is_absolute() is False
