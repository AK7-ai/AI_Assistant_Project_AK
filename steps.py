"""
steps.py

Functions for analysing participants step data.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

# Create one loader instance
loader = PMDataLoader(DATA_DIR)


def load_steps(participant_id: str) -> pd.DataFrame:
    """
    Load the step data of one participant.

    Parameters
    ----------
    participant_id : str
        Participant ID (e.g. "p01").

    Returns
    -------
    pd.DataFrame
        Step data.
    """
    return loader.load_steps(participant_id)


def get_daily_steps(participant_id: str, date: str) -> dict:
    """
    Return the total number of steps for a specific day.

    Parameters
    ----------
    participant_id : str
    date : str
        Format: YYYY-MM-DD

    Returns
    -------
    dict
    """

    df = load_steps(participant_id)

    df["date"] = df["dateTime"].dt.date

    selected_date = pd.to_datetime(date).date()

    selected = df[df["date"] == selected_date]

    if selected.empty:
        return {
            "participant": participant_id,
            "date": date,
            "steps": None,
            "message": "No data available for this date."
        }

    total_steps = selected["value"].sum()

    return {
        "participant": participant_id,
        "date": date,
        "steps": int(total_steps)
    }


def get_average_daily_steps(participant_id: str) -> dict:
    """
    Compute the participant's average daily steps.
    """

    df = load_steps(participant_id)

    if df.empty:
        return {
            "participant": participant_id,
            "average_daily_steps": None,
            "message": "No data available for this participant."
        }

    df["date"] = df["dateTime"].dt.date

    daily_steps = (
        df.groupby("date")["value"]
        .sum()
    )

    average = daily_steps.mean()

    return {
        "participant": participant_id,
        "average_daily_steps": round(float(average), 1)
    }


def get_total_steps(participant_id: str) -> dict:
    """
    Return the total number of recorded steps.
    """

    df = load_steps(participant_id)

    total = df["value"].sum()

    return {
        "participant": participant_id,
        "total_steps": int(total)
    }


def get_steps_between_dates(
    participant_id: str,
    start_date: str,
    end_date: str
) -> dict:
    """
    Return the total number of steps between two dates.
    """

    df = load_steps(participant_id)

    mask = (
        (df["dateTime"] >= pd.to_datetime(start_date))
        &
        (df["dateTime"] <= pd.to_datetime(end_date))
    )

    total = df.loc[mask, "value"].sum()

    return {
        "participant": participant_id,
        "start_date": start_date,
        "end_date": end_date,
        "steps": int(total)
    }

def get_step_goal_progress(
    participant_id: str,
    date: str,
    goal: int = 10000
) -> dict:
    """
    Check whether the participant reached the daily step goal.
    """

    result = get_daily_steps(participant_id, date)

    if result["steps"] is None:
        return {
            "participant": participant_id,
            "date": date,
            "steps": None,
            "goal": goal,
            "goal_reached": None
        }

    return {
        "participant": participant_id,
        "date": date,
        "steps": result["steps"],
        "goal": goal,
        "goal_reached": result["steps"] >= goal
    }
