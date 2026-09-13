"""
injury.py

Functions for analysing participants injury data.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)


def load_injury(participant_id: str) -> pd.DataFrame:
    """
    Load injury data for one participant.
    """
    return loader.load_injury(participant_id)


def get_injury_on_date(participant_id: str, date: str) -> dict:
    """
    Return injury information for one date.
    """

    df = load_injury(participant_id)

    df["date"] = df["effective_time_frame"].dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "injuries": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "injuries": selected.iloc[0]["injuries"]
    }


def has_injury(participant_id: str, date: str) -> dict:
    """
    Check whether the participant reported an injury.
    """

    result = get_injury_on_date(participant_id, date)

    injuries = result["injuries"]

    if pd.isna(injuries):
        return {
            "participant": participant_id,
            "date": date,
            "has_injury": False
        }

    return {
        "participant": participant_id,
        "date": date,
        "has_injury": injuries not in [None, "", "{}"]
    }


def get_injury_history(participant_id: str) -> dict:
    """
    Return the complete injury history.
    """

    df = load_injury(participant_id)

    return {
        "participant": participant_id,
        "number_of_reports": len(df),
        "history": df.to_dict("records")
    }


def get_number_of_injury_reports(participant_id: str) -> dict:
    """
    Return the number of injury reports.
    """

    df = load_injury(participant_id)

    return {
        "participant": participant_id,
        "number_of_reports": len(df)
    }


def get_injury_status(participant_id: str, date: str) -> dict:
    """
    Return whether an injury was reported on one day, plus any
    recorded details. Combines has_injury() and get_injury_on_date()
    into a single call, meant to back a single tool.
    """

    flag = has_injury(participant_id, date)
    on_date = get_injury_on_date(participant_id, date)

    details = on_date["injuries"]

    is_empty = (
        details is None
        or (not isinstance(details, str) and pd.isna(details))
        or details in ["", "{}"]
    )

    return {
        "participant": participant_id,
        "date": date,
        "has_injury": flag["has_injury"],
        "details": None if is_empty else details
    }
