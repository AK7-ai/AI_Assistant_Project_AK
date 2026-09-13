"""
heart_rate.py

Functions for analysing resting heart rate.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)


def load_resting_heart_rate(participant_id: str) -> pd.DataFrame:
    """
    Load resting heart rate data.
    """
    return loader.load_resting_heart_rate(participant_id)


def get_resting_heart_rate(participant_id: str, date: str) -> dict:
    """
    Return resting heart rate for one day.
    """

    df = load_resting_heart_rate(participant_id)

    selected = df[df["dateTime"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "resting_heart_rate": None
        }

    bpm = float(selected.iloc[0]["restingHeartRate"])

    return {
        "participant": participant_id,
        "date": date,
        "resting_heart_rate": round(bpm, 1)
    }


def get_average_resting_heart_rate(participant_id: str) -> dict:
    """
    Return average resting heart rate.
    """

    df = load_resting_heart_rate(participant_id)

    average = df["restingHeartRate"].mean()

    return {
        "participant": participant_id,
        "average_resting_heart_rate": round(float(average), 1)
    }


def is_resting_heart_rate_low(
    participant_id: str,
    date: str,
    threshold: float = 60
) -> dict:
    """
    Check if resting heart rate is below the threshold.
    """

    result = get_resting_heart_rate(participant_id, date)

    if result["resting_heart_rate"] is None:
        return result

    return {
        "participant": participant_id,
        "date": date,
        "resting_heart_rate": result["resting_heart_rate"],
        "low_resting_heart_rate": bool(
            result["resting_heart_rate"] < threshold
        )
    }


def is_resting_heart_rate_high(
    participant_id: str,
    date: str,
    threshold: float = 100
) -> dict:
    """
    Check if resting heart rate is above the threshold.
    """

    result = get_resting_heart_rate(participant_id, date)

    if result["resting_heart_rate"] is None:
        return result

    return {
        "participant": participant_id,
        "date": date,
        "resting_heart_rate": result["resting_heart_rate"],
        "high_resting_heart_rate": bool(
            result["resting_heart_rate"] > threshold
        )
    }
