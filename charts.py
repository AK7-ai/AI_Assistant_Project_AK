"""
charts.py

Chart-generation tools.

Each function computes the underlying data with pandas, renders it with matplotlib, saves the figure to disk, and returns both the file path and the raw data points. The chart itself never contains a number the caller can't trace back to a dataframe.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display backend needed
import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_DIR, PROJECT_ROOT
from loader import PMDataLoader

loader = PMDataLoader(DATA_DIR)

CHARTS_DIR = PROJECT_ROOT / "charts_output"
CHARTS_DIR.mkdir(exist_ok=True)


def _daily_series(participant_id: str, metric: str) -> pd.Series:
    """
    Return a pandas Series indexed by date for a given metric.

    Supported metrics: 'resting_heart_rate', 'steps', 'calories',
    'sleep_hours'.
    """

    if metric == "resting_heart_rate":
        df = loader.load_resting_heart_rate(participant_id)
        df["date"] = df["dateTime"].dt.date
        series = df.set_index("date")["restingHeartRate"]

    elif metric == "steps":
        df = loader.load_steps(participant_id)
        df["date"] = df["dateTime"].dt.date
        series = df.groupby("date")["value"].sum()

    elif metric == "calories":
        df = loader.load_calories(participant_id)
        df["date"] = df["dateTime"].dt.date
        series = df.groupby("date")["value"].sum()

    elif metric == "sleep_hours":
        df = loader.load_sleep(participant_id)
        if "mainSleep" in df.columns:
            main = df[df["mainSleep"] == True]  # noqa: E712
            if not main.empty:
                df = main
        df["date"] = df["dateOfSleep"].dt.date
        series = df.set_index("date")["minutesAsleep"] / 60

    else:
        raise ValueError(
            f"Unsupported metric '{metric}'. Supported metrics: "
            "resting_heart_rate, steps, calories, sleep_hours."
        )

    return series.sort_index()


METRIC_LABELS = {
    "resting_heart_rate": "Resting heart rate (bpm)",
    "steps": "Steps",
    "calories": "Calories burned",
    "sleep_hours": "Sleep duration (hours)",
}


def plot_metric_trend(
    participant_id: str,
    metric: str,
    end_date: str,
    days: int = 7
) -> dict:
    """
    Plot a metric's trend over a window of days ending on end_date.

    Parameters
    ----------
    participant_id : str
    metric : str
        One of: 'resting_heart_rate', 'steps', 'calories', 'sleep_hours'.
    end_date : str
        Last day of the window (YYYY-MM-DD).
    days : int
        Number of days to include (default 7).

    Returns
    -------
    dict with the chart path, the label, and the raw data points used.
    """

    series = _daily_series(participant_id, metric)

    end = pd.to_datetime(end_date).date()
    start = end - pd.Timedelta(days=days - 1)

    window = series[(series.index >= start) & (series.index <= end)]

    if window.empty:
        return {
            "participant": participant_id,
            "metric": metric,
            "start_date": str(start),
            "end_date": str(end),
            "chart_path": None,
            "data": [],
            "message": "No data available for this period."
        }

    label = METRIC_LABELS.get(metric, metric)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(window.index, window.values, marker="o")
    ax.set_title(f"{label} — {participant_id} ({start} to {end})")
    ax.set_xlabel("Date")
    ax.set_ylabel(label)
    fig.autofmt_xdate()
    fig.tight_layout()

    filename = f"{participant_id}_{metric}_{start}_{end}.png"
    chart_path = CHARTS_DIR / filename
    fig.savefig(chart_path)
    plt.close(fig)

    data_points = [
        {"date": str(idx), "value": round(float(val), 2)}
        for idx, val in window.items()
    ]

    return {
        "participant": participant_id,
        "metric": metric,
        "start_date": str(start),
        "end_date": str(end),
        "chart_path": str(chart_path),
        "data": data_points
    }


def plot_resting_heart_rate_trend(
    participant_id: str,
    end_date: str,
    days: int = 7
) -> dict:
    """
    Convenience wrapper: plot resting heart rate over the last N days.
    """
    return plot_metric_trend(participant_id, "resting_heart_rate", end_date, days)
