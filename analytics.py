"""
analytics.py

High-level analytics functions built from the PMData modules.
These functions combine several datasets to answer more advanced health questions.
"""

import pandas as pd

from config import DATA_DIR
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)


def get_most_active_day(participant_id: str) -> dict:
    """
    Return the day with the highest number of steps.
    """

    df = loader.load_steps(participant_id)

    df["date"] = df["dateTime"].dt.date

    daily_steps = df.groupby("date")["value"].sum()

    best_day = daily_steps.idxmax()

    return {
        "participant": participant_id,
        "most_active_day": str(best_day),
        "steps": int(daily_steps.max())
    }


def get_average_daily_steps(participant_id: str) -> dict:
    """
    Return the average daily steps.
    """

    df = loader.load_steps(participant_id)

    df["date"] = df["dateTime"].dt.date

    average = (
        df.groupby("date")["value"]
        .sum()
        .mean()
    )

    return {
        "participant": participant_id,
        "average_daily_steps": round(float(average), 1)
    }



def get_highest_calorie_day(participant_id: str) -> dict:
    """
    Return the day with the highest calorie expenditure.
    """

    df = loader.load_calories(participant_id)

    df["date"] = df["dateTime"].dt.date

    daily_calories = (
        df.groupby("date")["value"]
        .sum()
    )

    best_day = daily_calories.idxmax()

    return {
        "participant": participant_id,
        "highest_calorie_day": str(best_day),
        "calories": round(float(daily_calories.max()), 1)
    }


def get_average_sleep_duration(participant_id: str) -> dict:
    """
    Return the average sleep duration.
    """

    df = loader.load_sleep(participant_id)

    average = df["minutesAsleep"].mean() / 60

    return {
        "participant": participant_id,
        "average_sleep_hours": round(float(average), 2)
    }


def get_average_sleep_this_month(participant_id: str) -> dict:
    """
    Return the average sleep duration during the latest month.
    """

    df = loader.load_sleep(participant_id)

    if df.empty:
        return {
            "participant": participant_id,
            "average_sleep_hours": None
        }

    df["month"] = df["dateOfSleep"].dt.to_period("M")

    latest_month = df["month"].max()

    month_df = df[df["month"] == latest_month]

    average = month_df["minutesAsleep"].mean() / 60

    return {
        "participant": participant_id,
        "month": str(latest_month),
        "average_sleep_hours": round(float(average), 2)
    }


def get_average_wake_up_time(participant_id: str) -> dict:
    """
    Return the average wake-up time.
    """

    df = loader.load_sleep(participant_id)

    wake_minutes = (
        df["endTime"].dt.hour * 60 +
        df["endTime"].dt.minute
    )

    average = wake_minutes.mean()

    hour = int(average // 60)
    minute = int(average % 60)

    return {
        "participant": participant_id,
        "average_wake_up_time": f"{hour:02d}:{minute:02d}"
    }



def get_average_resting_hr(participant_id: str) -> dict:
    """
    Return the average resting heart rate.
    """

    df = loader.load_resting_heart_rate(participant_id)

    return {
        "participant": participant_id,
        "average_resting_hr": round(
            float(df["restingHeartRate"].mean()),
            1
        )
    }


def get_last_7_days_resting_hr(participant_id: str) -> dict:
    """
    Return resting heart rate for the last seven recorded days.
    """

    df = loader.load_resting_heart_rate(participant_id)

    df = df.sort_values("dateTime").tail(7)

    return {
        "participant": participant_id,
        "heart_rate": df[
            ["dateTime", "restingHeartRate"]
        ].to_dict("records")
    }



def compare_steps_last_month(participant_id: str) -> dict:
    """
    Compare the latest month with the previous month.
    """

    df = loader.load_steps(participant_id)

    df["month"] = df["dateTime"].dt.to_period("M")

    monthly = (
        df.groupby("month")["value"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return {
            "participant": participant_id,
            "message": "Not enough data."
        }

    current = monthly.iloc[-1]
    previous = monthly.iloc[-2]

    difference = current["value"] - previous["value"]

    return {
        "participant": participant_id,
        "current_month": str(current["month"]),
        "previous_month": str(previous["month"]),
        "difference": int(difference),
        "increased": bool(difference > 0)
    }


def compare_sleep_weeks(participant_id: str) -> dict:
    """
    Compare the average sleep duration between the last
    two recorded weeks.
    """

    df = loader.load_sleep(participant_id)

    iso = df["dateOfSleep"].dt.isocalendar()
    df["iso_year"] = iso["year"]
    df["iso_week"] = iso["week"]

    weekly = (
        df.groupby(["iso_year", "iso_week"])["minutesAsleep"]
        .mean()
        .reset_index()
        .sort_values(["iso_year", "iso_week"])
    )

    if len(weekly) < 2:
        return {
            "participant": participant_id,
            "message": "Not enough data."
        }

    current = weekly.iloc[-1]
    previous = weekly.iloc[-2]

    current_hours = current["minutesAsleep"] / 60
    previous_hours = previous["minutesAsleep"] / 60

    return {
        "participant": participant_id,
        "current_week": f"{int(current['iso_year'])}-W{int(current['iso_week']):02d}",
        "previous_week": f"{int(previous['iso_year'])}-W{int(previous['iso_week']):02d}",
        "current_sleep_hours": round(float(current_hours), 2),
        "previous_sleep_hours": round(float(previous_hours), 2),
        "difference_hours": round(
            float(current_hours - previous_hours),
            2
        )
    }


def detect_unusual_days(participant_id: str) -> dict:
    """
    Detect unusually high or low step counts.
    """

    df = loader.load_steps(participant_id)

    df["date"] = df["dateTime"].dt.date

    daily = (
        df.groupby("date")["value"]
        .sum()
        .reset_index()
    )

    mean = daily["value"].mean()
    std = daily["value"].std()

    unusual = daily[
        (daily["value"] > mean + 2 * std) |
        (daily["value"] < mean - 2 * std)
    ]

    return {
        "participant": participant_id,
        "number_of_unusual_days": len(unusual),
        "days": unusual.to_dict("records")
    }


def get_activity_recommendation(participant_id: str) -> dict:
    """
    Give a simple recommendation based on average daily steps.
    """

    average_steps = get_average_daily_steps(
        participant_id
    )["average_daily_steps"]

    if average_steps >= 10000:
        advice = "Excellent activity level. Keep it up!"

    elif average_steps >= 7000:
        advice = "Good activity level. A few more steps would be beneficial."

    else:
        advice = "Try to increase your daily physical activity."

    return {
        "participant": participant_id,
        "average_daily_steps": average_steps,
        "recommendation": advice
    }


def get_sleep_recommendation(participant_id: str) -> dict:
    """
    Give a recommendation based on average sleep duration.
    """

    average_sleep = get_average_sleep_duration(
        participant_id
    )["average_sleep_hours"]

    if average_sleep >= 8:
        advice = "Your sleep duration is excellent."

    elif average_sleep >= 7:
        advice = "Your sleep duration is within the recommended range."

    else:
        advice = (
            "Try to sleep at least 7 hours per night."
        )

    return {
        "participant": participant_id,
        "average_sleep_hours": average_sleep,
        "recommendation": advice
    }


def get_resting_hr_recommendation(participant_id: str) -> dict:
    """
    Give a recommendation based on resting heart rate.
    """

    hr = get_average_resting_hr(
        participant_id
    )["average_resting_hr"]

    if hr < 60:
        advice = "Low resting heart rate. Often observed in trained individuals."

    elif hr <= 80:
        advice = "Resting heart rate is within a healthy range."

    else:
        advice = "Resting heart rate is relatively high. Monitor it regularly."

    return {
        "participant": participant_id,
        "average_resting_hr": hr,
        "recommendation": advice
    }


def get_sedentary_recommendation(participant_id: str) -> dict:
    """
    Give advice based on average sedentary time.
    """

    df = loader.load_sedentary_minutes(participant_id)

    average = df["value"].mean()

    if average < 480:
        advice = "Sedentary time is low."

    elif average < 600:
        advice = "Sedentary time is acceptable."

    else:
        advice = (
            "Try to reduce sedentary time by taking regular breaks."
        )

    return {
        "participant": participant_id,
        "average_sedentary_minutes": round(float(average), 1),
        "recommendation": advice
    }
