"""
wellness.py

Functions for analysing participants wellness data.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

# Create one loader instance
loader = PMDataLoader(DATA_DIR)


def load_wellness(participant_id: str) -> pd.DataFrame:
    """
    Load the wellness data of one participant.
    """

    return loader.load_wellness(participant_id)


def get_daily_wellness(participant_id: str, date: str) -> dict:
    """
    Return all wellness information for one day.
    """

    df = load_wellness(participant_id)

    df["date"] = pd.to_datetime(df["effective_time_frame"]).dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "message": "No wellness data available."
        }

    row = selected.iloc[0]

    return {
        "participant": participant_id,
        "date": date,
        "fatigue": int(row["fatigue"]),
        "mood": int(row["mood"]),
        "readiness": int(row["readiness"]),
        "sleep_duration_h": int(row["sleep_duration_h"]),
        "sleep_quality": int(row["sleep_quality"]),
        "soreness": int(row["soreness"]),
        "stress": int(row["stress"])
    }


def get_daily_fatigue(participant_id: str, date: str) -> dict:
    """
    Return fatigue level for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "fatigue": result.get("fatigue")
    }


def get_daily_mood(participant_id: str, date: str) -> dict:
    """
    Return mood level for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "mood": result.get("mood")
    }


def get_daily_stress(participant_id: str, date: str) -> dict:
    """
    Return stress level for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "stress": result.get("stress")
    }


def get_daily_readiness(participant_id: str, date: str) -> dict:
    """
    Return readiness level for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "readiness": result.get("readiness")
    }


def get_daily_sleep_quality(participant_id: str, date: str) -> dict:
    """
    Return subjective sleep quality for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "sleep_quality": result.get("sleep_quality")
    }


def get_daily_soreness(participant_id: str, date: str) -> dict:
    """
    Return soreness level for one day.
    """

    result = get_daily_wellness(participant_id, date)

    return {
        "participant": participant_id,
        "date": date,
        "soreness": result.get("soreness")
    }


def get_average_wellness(participant_id: str) -> dict:
    """
    Compute average wellness metrics.
    """

    df = load_wellness(participant_id)

    return {
        "participant": participant_id,
        "average_fatigue": round(float(df["fatigue"].mean()), 2),
        "average_mood": round(float(df["mood"].mean()), 2),
        "average_readiness": round(float(df["readiness"].mean()), 2),
        "average_sleep_duration_h": round(float(df["sleep_duration_h"].mean()), 2),
        "average_sleep_quality": round(float(df["sleep_quality"].mean()), 2),
        "average_soreness": round(float(df["soreness"].mean()), 2),
        "average_stress": round(float(df["stress"].mean()), 2)
    }
