"""
tools/registry.py

A flat list of every tool: name, description (what the LLM sees whendeciding whether to call it), input model, output model, and the run function. 
This is the single source of truth to wire into LangGraph later — each entry maps directly to a LangChain/LangGraph tool spec.
"""

from dataclasses import dataclass
from typing import Any, Callable, Type

from pydantic import BaseModel

from tools import definitions as d


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    run: Callable[[BaseModel], Any]


TOOLS = [
    ToolSpec(
        name="get_resting_heart_rate",
        description="Get resting heart rate (bpm) for one participant on one day.",
        input_model=d.GetRestingHeartRateInput,
        output_model=d.RestingHeartRateOutput,
        run=d.run_get_resting_heart_rate,
    ),
    ToolSpec(
        name="get_sedentary_time",
        description="Get sedentary minutes for one participant on one day.",
        input_model=d.GetSedentaryTimeInput,
        output_model=d.SedentaryTimeOutput,
        run=d.run_get_sedentary_time,
    ),
    ToolSpec(
        name="get_step_goal_progress",
        description=(
            "Get step count for one day and whether a step goal "
            "(default 10000) was reached."
        ),
        input_model=d.GetStepGoalProgressInput,
        output_model=d.StepGoalProgressOutput,
        run=d.run_get_step_goal_progress,
    ),
    ToolSpec(
        name="get_daily_recovery_report",
        description=(
            "Get a recovery snapshot for one day: sleep duration, "
            "sleep efficiency, and self-reported wellness."
        ),
        input_model=d.GetDailyRecoveryReportInput,
        output_model=d.DailyRecoveryReportOutput,
        run=d.run_get_daily_recovery_report,
    ),
    ToolSpec(
        name="get_wake_time",
        description="Get the wake-up time for one participant on one day.",
        input_model=d.GetWakeTimeInput,
        output_model=d.WakeTimeOutput,
        run=d.run_get_wake_time,
    ),
    ToolSpec(
        name="get_daily_fitness_report",
        description=(
            "Get a fitness snapshot for one day: resting heart rate, "
            "steps, and light/moderate/very-active minutes."
        ),
        input_model=d.GetDailyFitnessReportInput,
        output_model=d.DailyFitnessReportOutput,
        run=d.run_get_daily_fitness_report,
    ),
    ToolSpec(
        name="get_wellness_correlation",
        description=(
            "Get the statistical correlation between two self-reported "
            "wellness metrics (fatigue, mood, readiness, sleep_duration_h, "
            "sleep_quality, soreness, stress). Describes an association, "
            "not a cause."
        ),
        input_model=d.GetWellnessCorrelationInput,
        output_model=d.WellnessCorrelationOutput,
        run=d.run_get_wellness_correlation,
    ),
    ToolSpec(
        name="get_activity_vs_stress_correlation",
        description=(
            "Get the statistical correlation between total daily active "
            "minutes and self-reported stress. Describes an association, "
            "not a cause."
        ),
        input_model=d.GetActivityVsStressCorrelationInput,
        output_model=d.ActivityStressCorrelationOutput,
        run=d.run_get_activity_vs_stress_correlation,
    ),
    ToolSpec(
        name="get_injury_status",
        description="Check whether an injury was reported on one day, with details if so.",
        input_model=d.GetInjuryStatusInput,
        output_model=d.InjuryStatusOutput,
        run=d.run_get_injury_status,
    ),
    ToolSpec(
        name="compare_sleep_weeks",
        description="Compare average sleep duration between the two most recent recorded weeks.",
        input_model=d.CompareSleepWeeksInput,
        output_model=d.CompareSleepWeeksOutput,
        run=d.run_compare_sleep_weeks,
    ),
    ToolSpec(
        name="compare_steps_last_month",
        description="Compare total steps between the current and previous recorded month.",
        input_model=d.CompareStepsLastMonthInput,
        output_model=d.CompareStepsLastMonthOutput,
        run=d.run_compare_steps_last_month,
    ),
    ToolSpec(
        name="get_average_sleep_this_month",
        description="Get the average sleep duration for the latest recorded month.",
        input_model=d.GetAverageSleepThisMonthInput,
        output_model=d.AverageSleepThisMonthOutput,
        run=d.run_get_average_sleep_this_month,
    ),
    ToolSpec(
        name="plot_resting_heart_rate_trend",
        description=(
            "Generate a line chart of resting heart rate over a window of "
            "days ending on a given date. Returns a chart file path and "
            "the underlying data points."
        ),
        input_model=d.PlotRestingHeartRateTrendInput,
        output_model=d.ChartOutput,
        run=d.run_plot_resting_heart_rate_trend,
    ),
    ToolSpec(
        name="get_average_wake_up_time",
        description="Get the average wake-up time across all recorded nights.",
        input_model=d.GetAverageWakeUpTimeInput,
        output_model=d.AverageWakeUpTimeOutput,
        run=d.run_get_average_wake_up_time,
    ),
    ToolSpec(
        name="detect_unusual_days",
        description=(
            "Find days where step count is unusually high or low compared "
            "to the participant's own average (z-score based)."
        ),
        input_model=d.DetectUnusualDaysInput,
        output_model=d.DetectUnusualDaysOutput,
        run=d.run_detect_unusual_days,
    ),
    ToolSpec(
        name="get_most_active_day",
        description=(
            "Get the day with the highest step count across the "
            "participant's full recorded history."
        ),
        input_model=d.GetMostActiveDayInput,
        output_model=d.MostActiveDayOutput,
        run=d.run_get_most_active_day,
    ),
    ToolSpec(
        name="get_highest_calorie_day",
        description=(
            "Get the day with the highest calorie expenditure across the "
            "participant's full recorded history."
        ),
        input_model=d.GetHighestCalorieDayInput,
        output_model=d.HighestCalorieDayOutput,
        run=d.run_get_highest_calorie_day,
    ),
    ToolSpec(
        name="get_daily_lifestyle_report",
        description=(
            "Get a general lifestyle snapshot for one day: steps, distance, "
            "calories, sleep duration, and wellness."
        ),
        input_model=d.GetDailyLifestyleReportInput,
        output_model=d.DailyLifestyleReportOutput,
        run=d.run_get_daily_lifestyle_report,
    ),
]


TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}
