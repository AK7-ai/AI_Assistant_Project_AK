"""
tools/base.py

Shared pydantic input models. Most tools take a participant_id and a date, or a participant_id and a date range, these base classes avoid
repeating the same fields (and the same date-format validation) in every single tool's input schema.
"""

import datetime

from pydantic import BaseModel, Field, field_validator


def _validate_iso_date(value: str) -> str:
    try:
        datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"'{value}' is not a valid date. Use YYYY-MM-DD format."
        ) from exc
    return value


class ParticipantIdInput(BaseModel):
    """Base input for tools that only need to know which participant."""

    model_config = {"extra": "forbid"}

    participant_id: str = Field(
        ...,
        description="Participant identifier, e.g. 'p01'.",
        min_length=1,
    )


class ParticipantDateInput(ParticipantIdInput):
    """Base input for tools scoped to one participant on one day."""

    date: str = Field(
        ...,
        description="Date in YYYY-MM-DD format.",
    )

    @field_validator("date")
    @classmethod
    def _check_date(cls, value: str) -> str:
        return _validate_iso_date(value)


class ParticipantDateRangeInput(ParticipantIdInput):
    """Base input for tools scoped to a date range."""

    start_date: str = Field(..., description="Start date, YYYY-MM-DD.")
    end_date: str = Field(..., description="End date, YYYY-MM-DD.")

    @field_validator("start_date", "end_date")
    @classmethod
    def _check_date(cls, value: str) -> str:
        return _validate_iso_date(value)

    @field_validator("end_date")
    @classmethod
    def _check_end_after_start(cls, end_date: str, info) -> str:
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must not be before start_date.")
        return end_date
