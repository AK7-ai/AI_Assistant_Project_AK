"""
correlations.py

Tools for measuring the statistical relationship between two daily metrics for the same participant (e.g. sleep quality vs mood). 
(Return a correlation coefficient, which describes an association, not a cause.)
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader
from wellness import load_wellness

loader = PMDataLoader(DATA_DIR)

VALID_WELLNESS_METRICS = [
    "fatigue",
    "mood",
    "readiness",
    "sleep_duration_h",
    "sleep_quality",
    "soreness",
    "stress",
]


def _interpret_correlation(r: float) -> str:

    abs_r = abs(r)

    if abs_r < 0.2:
        return "very weak or no relationship"
    if abs_r < 0.4:
        return "weak relationship"
    if abs_r < 0.6:
        return "moderate relationship"
    if abs_r < 0.8:
        return "strong relationship"
    return "very strong relationship"


def get_wellness_correlation(
    participant_id: str,
    metric_x: str,
    metric_y: str
) -> dict:
    """
    Return the correlation between two self-reported wellness metrics
    (e.g. 'sleep_quality' and 'mood').
    """

    if metric_x not in VALID_WELLNESS_METRICS:
        raise ValueError(
            f"'{metric_x}' is not a valid wellness metric. "
            f"Choose from: {VALID_WELLNESS_METRICS}"
        )

    if metric_y not in VALID_WELLNESS_METRICS:
        raise ValueError(
            f"'{metric_y}' is not a valid wellness metric. "
            f"Choose from: {VALID_WELLNESS_METRICS}"
        )

    df = load_wellness(participant_id)
    df = df.dropna(subset=[metric_x, metric_y])

    if len(df) < 3:
        return {
            "participant": participant_id,
            "metric_x": metric_x,
            "metric_y": metric_y,
            "correlation": None,
            "n_days": len(df),
            "message": "Not enough overlapping data points to compute a correlation."
        }

    correlation = df[metric_x].corr(df[metric_y])

    return {
        "participant": participant_id,
        "metric_x": metric_x,
        "metric_y": metric_y,
        "correlation": round(float(correlation), 2),
        "n_days": int(len(df)),
        "strength": _interpret_correlation(correlation)
    }


def get_activity_vs_stress_correlation(participant_id: str) -> dict:
    """
    Return the correlation between total daily active minutes (light +
    moderate + very active) and self-reported stress.
    """

    light = loader.load_lightly_active_minutes(participant_id)
    moderate = loader.load_moderately_active_minutes(participant_id)
    very_active = loader.load_very_active_minutes(participant_id)

    for df in (light, moderate, very_active):
        df["date"] = df["dateTime"].dt.date

    activity = (
        light.groupby("date")["value"].sum()
        .add(moderate.groupby("date")["value"].sum(), fill_value=0)
        .add(very_active.groupby("date")["value"].sum(), fill_value=0)
        .rename("active_minutes")
    )

    wellness = load_wellness(participant_id)
    wellness["date"] = wellness["effective_time_frame"].dt.date
    stress = wellness.groupby("date")["stress"].mean()

    merged = pd.concat([activity, stress], axis=1).dropna()

    if len(merged) < 3:
        return {
            "participant": participant_id,
            "correlation": None,
            "n_days": len(merged),
            "message": "Not enough overlapping data points to compute a correlation."
        }

    correlation = merged["active_minutes"].corr(merged["stress"])

    return {
        "participant": participant_id,
        "correlation": round(float(correlation), 2),
        "n_days": int(len(merged)),
        "strength": _interpret_correlation(correlation)
    }
