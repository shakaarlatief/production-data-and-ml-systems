import csv
from pathlib import Path
from typing import Any

import pytest

from bike_share_etl.validate_citibike_raw import normalize_text, validate_raw_row


FIXTURE_FILE = (
    Path(__file__).parent
    / "fixtures"
    / "citibike_validation_cases.csv"
)

RESOLVED_END_STATION_ID_INDEX = 11
RESOLUTION_METHOD_INDEX = 12
IS_LONG_TRIP_INDEX = 18
HAS_MISSING_END_STATION_INDEX = 19
HAS_MISSING_END_COORDINATES_INDEX = 20


def load_cases() -> dict[str, dict[str, Any]]:
    """Load named synthetic validation cases from the fixture CSV."""
    with FIXTURE_FILE.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as fixture_file:
        reader = csv.DictReader(fixture_file)
        cases: dict[str, dict[str, Any]] = {}

        for row in reader:
            case_name = row.pop("case_name")
            row["file_id"] = int(row["file_id"])
            row["source_row_number"] = int(row["source_row_number"])
            cases[case_name] = row

    return cases


CASES = load_cases()


def validate_case(
    case_name: str,
    station_name_to_ids: dict[str, set[str]] | None = None,
    seen_valid_ride_ids: set[str] | None = None,
) -> tuple[
    tuple[Any, ...] | None,
    tuple[str, ...],
    tuple[str, ...],
]:
    """Validate one named fixture with isolated mutable inputs."""
    return validate_raw_row(
        raw_row=CASES[case_name].copy(),
        station_name_to_ids=station_name_to_ids or {},
        seen_valid_ride_ids=(
            set()
            if seen_valid_ride_ids is None
            else seen_valid_ride_ids.copy()
        ),
    )


def test_normalize_text_strips_whitespace_and_converts_blanks() -> None:
    assert normalize_text("  station  ") == "station"
    assert normalize_text("   ") is None
    assert normalize_text("") is None
    assert normalize_text(None) is None


def test_valid_trip_is_accepted_without_quality_flags() -> None:
    valid_row, rejection_reasons, quality_flags = validate_case(
        "valid_trip"
    )

    assert valid_row is not None
    assert rejection_reasons == ()
    assert quality_flags == ()


def test_soft_conditions_are_accepted_and_flagged() -> None:
    valid_row, rejection_reasons, quality_flags = validate_case(
        "soft_missing_endpoint"
    )

    assert valid_row is not None
    assert rejection_reasons == ()
    assert set(quality_flags) == {
        "LONG_TRIP_OVER_24_HOURS",
        "MISSING_END_STATION",
        "MISSING_END_COORDINATES",
    }
    assert valid_row[IS_LONG_TRIP_INDEX] is True
    assert valid_row[HAS_MISSING_END_STATION_INDEX] is True
    assert valid_row[HAS_MISSING_END_COORDINATES_INDEX] is True
    assert valid_row[RESOLUTION_METHOD_INDEX] == "unavailable"


def test_missing_end_station_id_is_inferred_from_unique_name() -> None:
    valid_row, rejection_reasons, quality_flags = validate_case(
        "inferred_endpoint",
        station_name_to_ids={"Known End": {"END001"}},
    )

    assert valid_row is not None
    assert rejection_reasons == ()
    assert quality_flags == ("END_STATION_ID_INFERRED",)
    assert valid_row[RESOLVED_END_STATION_ID_INDEX] == "END001"
    assert (
        valid_row[RESOLUTION_METHOD_INDEX]
        == "inferred_from_station_name"
    )


def test_ambiguous_station_name_remains_accepted_but_unresolved() -> None:
    valid_row, rejection_reasons, quality_flags = validate_case(
        "ambiguous_endpoint",
        station_name_to_ids={
            "Ambiguous End": {"END001", "END002"},
        },
    )

    assert valid_row is not None
    assert rejection_reasons == ()
    assert set(quality_flags) == {
        "END_STATION_ID_AMBIGUOUS",
        "MISSING_END_STATION",
    }
    assert valid_row[RESOLVED_END_STATION_ID_INDEX] is None
    assert valid_row[RESOLUTION_METHOD_INDEX] == "ambiguous_station_name"


@pytest.mark.parametrize(
    ("case_name", "expected_reasons"),
    [
        ("missing_ride_id", {"MISSING_RIDE_ID"}),
        ("invalid_timestamp", {"INVALID_STARTED_AT"}),
        ("nonpositive_duration", {"NONPOSITIVE_DURATION"}),
        (
            "unknown_categories",
            {"UNKNOWN_RIDEABLE_TYPE", "UNKNOWN_MEMBER_TYPE"},
        ),
        (
            "invalid_coordinates",
            {"OUT_OF_RANGE_START_LAT", "INVALID_START_LNG"},
        ),
        (
            "incomplete_end_coordinates",
            {"INCOMPLETE_END_COORDINATE_PAIR"},
        ),
    ],
)
def test_hard_failures_are_rejected(
    case_name: str,
    expected_reasons: set[str],
) -> None:
    valid_row, rejection_reasons, _ = validate_case(case_name)

    assert valid_row is None
    assert expected_reasons.issubset(set(rejection_reasons))


def test_duplicate_ride_id_is_rejected() -> None:
    valid_row, rejection_reasons, _ = validate_case(
        "duplicate_ride",
        seen_valid_ride_ids={"DUP001"},
    )

    assert valid_row is None
    assert rejection_reasons == ("DUPLICATE_RIDE_ID",)
