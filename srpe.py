"""
srpe.py

Functions for analysing participants session RPE data.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)


def load_srpe(participant_id: str) -> pd.DataFrame:
    """
    Load sRPE data.
    """
    return loader.load_srpe(participant_id)


def get_sessions_on_date(participant_id: str, date: str) -> dict:
    """
    Return all sessions for one day.
    """

    df = load_srpe(participant_id)

    df["date"] = df["end_date_time"].dt.date

    selected = df[df["date"] == pd.to_datetime(date).date()]

    sessions = []

    for _, row in selected.iterrows():

        load = row["duration_min"] * row["perceived_exertion"]

        sessions.append(
            {
                "activity": row["activity_names"],
                "duration_min": int(row["duration_min"]),
                "rpe": int(row["perceived_exertion"]),
                "training_load": int(load)
            }
        )

    return {
        "participant": participant_id,
        "date": date,
        "number_of_sessions": len(sessions),
        "sessions": sessions
    }


def get_training_load(participant_id: str, date: str) -> dict:
    """
    Return total training load for one day.
    """

    sessions = get_sessions_on_date(participant_id, date)

    total = sum(
        session["training_load"]
        for session in sessions["sessions"]
    )

    return {
        "participant": participant_id,
        "date": date,
        "training_load": total
    }


def get_average_rpe(participant_id: str) -> dict:
    """
    Return average perceived exertion.
    """

    df = load_srpe(participant_id)

    return {
        "participant": participant_id,
        "average_rpe": round(
            float(df["perceived_exertion"].mean()),
            2
        )
    }


def get_average_training_load(participant_id: str) -> dict:
    """
    Return average training load.
    """

    df = load_srpe(participant_id)

    loads = (
        df["duration_min"] *
        df["perceived_exertion"]
    )

    return {
        "participant": participant_id,
        "average_training_load": round(
            float(loads.mean()),
            2
        )
    }
