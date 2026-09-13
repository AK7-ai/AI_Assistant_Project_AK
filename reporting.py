"""
reporting.py

High-level reporting functions that combine information from multiple health modules.
"""

from steps import get_daily_steps
from sleep import (
    get_sleep_duration,
    get_sleep_efficiency,
    slept_enough
)
from heart_rate import get_resting_heart_rate
from activity import (
    get_daily_calories,
    get_daily_distance,
    get_light_activity,
    get_moderate_activity,
    get_very_active,
    get_sedentary_time,
    get_exercise_sessions
)
from wellness import get_daily_wellness

def get_daily_health_summary(
    participant_id: str,
    date: str
) -> dict:
    """
    Return a complete summary of one participant for one day.
    """

    summary = {}

    summary["steps"] = get_daily_steps(participant_id, date)

    summary["sleep"] = {
        "duration": get_sleep_duration(participant_id, date),
        "efficiency": get_sleep_efficiency(participant_id, date),
        "recommended": slept_enough(participant_id, date)
    }

    summary["heart_rate"] = get_resting_heart_rate(
        participant_id,
        date
    )

    summary["activity"] = {
        "calories": get_daily_calories(participant_id, date),
        "distance": get_daily_distance(participant_id, date),
        "light_activity": get_light_activity(participant_id, date),
        "moderate_activity": get_moderate_activity(participant_id, date),
        "very_active": get_very_active(participant_id, date),
        "sedentary": get_sedentary_time(participant_id, date),
        "exercise_sessions": get_exercise_sessions(participant_id, date)
    }

    summary["wellness"] = get_daily_wellness(
        participant_id,
        date
    )

    return summary

def get_daily_lifestyle_report(
    participant_id: str,
    date: str
) -> dict:
    """
    Return lifestyle indicators for one day.
    """

    return {

        "steps": get_daily_steps(participant_id, date),

        "distance": get_daily_distance(participant_id, date),

        "calories": get_daily_calories(participant_id, date),

        "sleep": get_sleep_duration(participant_id, date),

        "wellness": get_daily_wellness(participant_id, date)

    }

def get_daily_fitness_report(
    participant_id: str,
    date: str
) -> dict:
    """
    Return fitness-related metrics.
    """

    return {

        "heart_rate": get_resting_heart_rate(
            participant_id,
            date
        ),

        "steps": get_daily_steps(
            participant_id,
            date
        ),

        "activity": {

            "light": get_light_activity(
                participant_id,
                date
            ),

            "moderate": get_moderate_activity(
                participant_id,
                date
            ),

            "very_active": get_very_active(
                participant_id,
                date
            )

        }

    }

def get_daily_recovery_report(
    participant_id: str,
    date: str
) -> dict:
    """
    Return recovery indicators.
    """

    return {

        "sleep": get_sleep_duration(
            participant_id,
            date
        ),

        "sleep_efficiency": get_sleep_efficiency(
            participant_id,
            date
        ),

        "wellness": get_daily_wellness(
            participant_id,
            date
        )

    }
