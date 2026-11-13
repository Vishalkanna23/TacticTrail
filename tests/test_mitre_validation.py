
from app.mitre_validation import (
    find_unverified_ids,
    validate_stream,
)


def test_detect_unverified_mitre_ids():
    evidence = "ID: T1110\nName: Brute Force"

    answer = (
        "T1110 is Brute Force. "
        "Attackers also use T1078 and T1003."
    )

    result = find_unverified_ids(answer, evidence)

    assert result == ["T1003", "T1078"]

def test_description_ids_are_not_automatically_verified():
    evidence = (
        "ID: T1110\n"
        "Name: Brute Force\n"
        "Description: This technique mentions T1078."
    )

    answer = "T1110 is relevant. T1078 is also involved."

    result = find_unverified_ids(answer, evidence)

    assert result == ["T1078"]

def test_stream_blocks_unverified_id():
    evidence = "ID: T1110\nName: Brute Force"

    chunks = [
        "Attackers use T1110 and T10",
        "78 to gain access.",
    ]

    result = "".join(validate_stream(chunks, evidence))

    assert "T1110" in result
    assert "T1078" not in result
    assert "unsupported MITRE" in result

def test_stream_blocks_unverified_subtechnique():
    evidence = "ID: T1110\nName: Brute Force"

    chunks = [
        "Attackers use T1110 and T1110.",
        "002 for password cracking."
    ]

    result = "".join(validate_stream(chunks, evidence))

    assert "T1110.002" not in result
    assert "unsupported MITRE" in result


def test_stream_allows_verified_id_with_punctuation():
    evidence = "ID: T1110\nName: Brute Force"

    chunks = [
        "The technique is T1110.",
        " It involves password guessing."
    ]

    result = "".join(validate_stream(chunks, evidence))

    assert result == (
        "The technique is T1110. "
        "It involves password guessing."
    )
    assert "unsupported MITRE" not in result
