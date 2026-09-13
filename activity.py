"""
activity.py

Functions for analysing participants physical activity.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)

def get_daily_calories(participant_id: str, date: str) -> dict:
    """
    Return calories burned during one day.
    """

    df = loader.load_calories(participant_id)

    df["date"] = df["dateTime"].dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    total = selected["value"].sum()

    return {
        "participant": participant_id,
        "date": date,
        "calories": float(round(total, 1))
    }

def get_daily_distance(participant_id: str, date: str) -> dict:
    """
    Return total distance travelled during one day.
    """

    df = loader.load_distance(participant_id)

    df["date"] = df["dateTime"].dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    total_cm = selected["value"].sum()

    distance_km = total_cm / 100000

    return {
        "participant": participant_id,
        "date": date,
        "distance_cm": int(total_cm),
        "distance_km": round(float(distance_km), 2)
    }

def get_light_activity(participant_id: str, date: str) -> dict:

    df = loader.load_lightly_active_minutes(participant_id)

    selected = df[df["dateTime"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "light_activity_minutes": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "light_activity_minutes": int(selected.iloc[0]["value"])
    }

def get_moderate_activity(participant_id: str, date: str) -> dict:

    df = loader.load_moderately_active_minutes(participant_id)

    selected = df[df["dateTime"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "moderate_activity_minutes": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "moderate_activity_minutes": int(selected.iloc[0]["value"])
    }

def get_very_active(participant_id: str, date: str) -> dict:

    df = loader.load_very_active_minutes(participant_id)

    selected = df[df["dateTime"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "very_active_minutes": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "very_active_minutes": int(selected.iloc[0]["value"])
    }

def get_sedentary_time(participant_id: str, date: str) -> dict:

    df = loader.load_sedentary_minutes(participant_id)

    selected = df[df["dateTime"] == pd.to_datetime(date)]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "sedentary_minutes": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "sedentary_minutes": int(selected.iloc[0]["value"])
    }

def get_exercise_sessions(participant_id: str, date: str) -> dict:
    """
    Return all exercise sessions performed during one day.
    """

    df = loader.load_exercise(participant_id)

    df["date"] = df["startTime"].dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    sessions = []

    for _, row in selected.iterrows():

        sessions.append(
            {
                "activity": row["activityName"],
                "duration_minutes": round(row["duration"] / 60000, 1),
                "calories": int(row["calories"]),
                "steps": int(row["steps"])
            }
        )

    return {
        "participant": participant_id,
        "date": date,
        "number_of_sessions": len(sessions),
        "sessions": sessions
    }

