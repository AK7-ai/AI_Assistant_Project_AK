"""
sleep.py

Functions for analysing participants sleep data.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

# Create one loader instance
loader = PMDataLoader(DATA_DIR)


def load_sleep(participant_id: str) -> pd.DataFrame:
    """
    Load sleep data for one participant.
    """
    return loader.load_sleep(participant_id)


def get_sleep_duration(participant_id: str, date: str) -> dict:
    """
    Return sleep duration (in hours) for one night.
    """

    df = load_sleep(participant_id)

    selected = df[df["dateOfSleep"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "sleep_hours": None,
            "message": "No sleep data available."
        }

    minutes = selected.iloc[0]["minutesAsleep"]

    return {
        "participant": participant_id,
        "date": date,
        "sleep_hours": float(round(minutes / 60, 2))
    }


def get_average_sleep_duration(participant_id: str) -> dict:
    """
    Return average sleep duration.
    """

    df = load_sleep(participant_id)

    average = df["minutesAsleep"].mean()

    return {
        "participant": participant_id,
        "average_sleep_hours": float(round(average / 60, 2))
    }


def get_sleep_efficiency(participant_id: str, date: str) -> dict:
    """
    Return sleep efficiency for one night.
    """

    df = load_sleep(participant_id)

    selected = df[df["dateOfSleep"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "efficiency": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "efficiency": int(selected.iloc[0]["efficiency"])
    }


def slept_enough(
    participant_id: str,
    date: str,
    recommended_hours: float = 8.0
) -> dict:
    """
    Check whether the participant slept enough.
    """

    result = get_sleep_duration(participant_id, date)

    if result["sleep_hours"] is None:
        return result

    return {
        "participant": participant_id,
        "date": date,
        "sleep_hours": result["sleep_hours"],
        "recommended_hours": recommended_hours,
        "enough_sleep": bool(result["sleep_hours"] >= recommended_hours)
    }


def get_average_sleep_efficiency(participant_id: str) -> dict:
    """
    Return average sleep efficiency.
    """

    df = load_sleep(participant_id)

    average = df["efficiency"].mean()

    return {
        "participant": participant_id,
        "average_efficiency": round(float(average), 1)
    }


def _main_sleep_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Restrict to the main sleep period of each day when the column is
    available, so naps don't distort wake-time calculations.
    """

    if "mainSleep" in df.columns:
        main = df[df["mainSleep"] == True]  # noqa: E712
        if not main.empty:
            return main

    return df


def get_wake_time(participant_id: str, date: str) -> dict:
    """
    Return the wake-up time (end of main sleep) for one night.
    """

    df = _main_sleep_only(load_sleep(participant_id))

    selected = df[df["dateOfSleep"] == pd.to_datetime(date)]

    if selected.empty or pd.isna(selected.iloc[0]["endTime"]):
        return {
            "participant": participant_id,
            "date": date,
            "wake_time": None,
            "message": "No sleep data available."
        }

    end_time = selected.iloc[0]["endTime"]

    return {
        "participant": participant_id,
        "date": date,
        "wake_time": end_time.strftime("%H:%M")
    }
