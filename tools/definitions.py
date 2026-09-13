"""
tools/definitions.py

One section per tool: an input model, an output model, and a `run` function that validates the input, calls the underlying analytics function, and validates the output before returning it.

Each `run` function is deliberately thin it never recomputes anything, it only validates at the boundary. All the actual logic stays in steps.py / sleep.py / analytics.py / etc.
"""

from typing import List, Literal, Optional

from pydantic import Field

import heart_rate
import activity
import steps
import sleep
import reporting
import injury
import analytics
import charts
import correlations

from tools.base import (
    ParticipantDateInput,
    ParticipantIdInput,
    ParticipantDateRangeInput,
)
from tools.outputs import (
    StrictOutput,
    RestingHeartRateOutput,
    SedentaryTimeOutput,
    StepGoalProgressOutput,
    SleepDurationOutput,
    SleepEfficiencyOutput,
    WakeTimeOutput,
    WellnessOutput,
    LightActivityOutput,
    ModerateActivityOutput,
    VeryActiveOutput,
    StepsOutput,
    DistanceOutput,
    CaloriesOutput,
    RestingHeartRateOutput as _RHROutput,  # reused inside fitness report
    InjuryStatusOutput,
    ChartDataPoint,
)


class GetRestingHeartRateInput(ParticipantDateInput):
    pass


def run_get_resting_heart_rate(payload: GetRestingHeartRateInput) -> RestingHeartRateOutput:
    result = heart_rate.get_resting_heart_rate(payload.participant_id, payload.date)
    return RestingHeartRateOutput(**result)



class GetSedentaryTimeInput(ParticipantDateInput):
    pass


def run_get_sedentary_time(payload: GetSedentaryTimeInput) -> SedentaryTimeOutput:
    result = activity.get_sedentary_time(payload.participant_id, payload.date)
    return SedentaryTimeOutput(**result)



class GetStepGoalProgressInput(ParticipantDateInput):
    goal: int = Field(10000, description="Daily step goal.", gt=0)


def run_get_step_goal_progress(payload: GetStepGoalProgressInput) -> StepGoalProgressOutput:
    result = steps.get_step_goal_progress(payload.participant_id, payload.date, payload.goal)
    return StepGoalProgressOutput(**result)



class GetDailyRecoveryReportInput(ParticipantDateInput):
    pass


class DailyRecoveryReportOutput(StrictOutput):
    sleep: SleepDurationOutput
    sleep_efficiency: SleepEfficiencyOutput
    wellness: WellnessOutput


def run_get_daily_recovery_report(payload: GetDailyRecoveryReportInput) -> DailyRecoveryReportOutput:
    result = reporting.get_daily_recovery_report(payload.participant_id, payload.date)
    return DailyRecoveryReportOutput(**result)



class GetWakeTimeInput(ParticipantDateInput):
    pass


def run_get_wake_time(payload: GetWakeTimeInput) -> WakeTimeOutput:
    result = sleep.get_wake_time(payload.participant_id, payload.date)
    return WakeTimeOutput(**result)



class GetDailyFitnessReportInput(ParticipantDateInput):
    pass


class FitnessActivityOutput(StrictOutput):
    light: LightActivityOutput
    moderate: ModerateActivityOutput
    very_active: VeryActiveOutput


class DailyFitnessReportOutput(StrictOutput):
    heart_rate: _RHROutput
    steps: StepsOutput
    activity: FitnessActivityOutput


def run_get_daily_fitness_report(payload: GetDailyFitnessReportInput) -> DailyFitnessReportOutput:
    result = reporting.get_daily_fitness_report(payload.participant_id, payload.date)
    return DailyFitnessReportOutput(**result)



WellnessMetric = Literal[
    "fatigue", "mood", "readiness", "sleep_duration_h",
    "sleep_quality", "soreness", "stress",
]


class GetWellnessCorrelationInput(ParticipantIdInput):
    metric_x: WellnessMetric = Field(..., description="First wellness metric.")
    metric_y: WellnessMetric = Field(..., description="Second wellness metric.")


class WellnessCorrelationOutput(StrictOutput):
    participant: str
    metric_x: str
    metric_y: str
    correlation: Optional[float] = None
    n_days: int
    strength: Optional[str] = None
    message: Optional[str] = None


def run_get_wellness_correlation(payload: GetWellnessCorrelationInput) -> WellnessCorrelationOutput:
    result = correlations.get_wellness_correlation(
        payload.participant_id, payload.metric_x, payload.metric_y
    )
    return WellnessCorrelationOutput(**result)



class GetActivityVsStressCorrelationInput(ParticipantIdInput):
    pass


class ActivityStressCorrelationOutput(StrictOutput):
    participant: str
    correlation: Optional[float] = None
    n_days: int
    strength: Optional[str] = None
    message: Optional[str] = None


def run_get_activity_vs_stress_correlation(
    payload: GetActivityVsStressCorrelationInput,
) -> ActivityStressCorrelationOutput:
    result = correlations.get_activity_vs_stress_correlation(payload.participant_id)
    return ActivityStressCorrelationOutput(**result)


class GetInjuryStatusInput(ParticipantDateInput):
    pass


def run_get_injury_status(payload: GetInjuryStatusInput) -> InjuryStatusOutput:
    result = injury.get_injury_status(payload.participant_id, payload.date)
    return InjuryStatusOutput(**result)


class CompareSleepWeeksInput(ParticipantIdInput):
    pass


class CompareSleepWeeksOutput(StrictOutput):
    participant: str
    message: Optional[str] = None
    current_week: Optional[str] = None
    previous_week: Optional[str] = None
    current_sleep_hours: Optional[float] = None
    previous_sleep_hours: Optional[float] = None
    difference_hours: Optional[float] = None


def run_compare_sleep_weeks(payload: CompareSleepWeeksInput) -> CompareSleepWeeksOutput:
    result = analytics.compare_sleep_weeks(payload.participant_id)
    return CompareSleepWeeksOutput(**result)


class CompareStepsLastMonthInput(ParticipantIdInput):
    pass


class CompareStepsLastMonthOutput(StrictOutput):
    participant: str
    message: Optional[str] = None
    current_month: Optional[str] = None
    previous_month: Optional[str] = None
    difference: Optional[int] = None
    increased: Optional[bool] = None


def run_compare_steps_last_month(payload: CompareStepsLastMonthInput) -> CompareStepsLastMonthOutput:
    result = analytics.compare_steps_last_month(payload.participant_id)
    return CompareStepsLastMonthOutput(**result)


class GetAverageSleepThisMonthInput(ParticipantIdInput):
    pass


class AverageSleepThisMonthOutput(StrictOutput):
    participant: str
    month: Optional[str] = None
    average_sleep_hours: Optional[float] = None


def run_get_average_sleep_this_month(
    payload: GetAverageSleepThisMonthInput,
) -> AverageSleepThisMonthOutput:
    result = analytics.get_average_sleep_this_month(payload.participant_id)
    return AverageSleepThisMonthOutput(**result)


class PlotRestingHeartRateTrendInput(ParticipantIdInput):
    end_date: str = Field(..., description="Last day of the window, YYYY-MM-DD.")
    days: int = Field(7, description="Number of days to include.", gt=0, le=90)


class ChartOutput(StrictOutput):
    participant: str
    metric: str
    start_date: str
    end_date: str
    chart_path: Optional[str] = None
    data: List[ChartDataPoint] = []
    message: Optional[str] = None


def run_plot_resting_heart_rate_trend(payload: PlotRestingHeartRateTrendInput) -> ChartOutput:
    result = charts.plot_resting_heart_rate_trend(
        payload.participant_id, payload.end_date, payload.days
    )
    return ChartOutput(**result)


class GetAverageWakeUpTimeInput(ParticipantIdInput):
    pass


class AverageWakeUpTimeOutput(StrictOutput):
    participant: str
    average_wake_up_time: str


def run_get_average_wake_up_time(payload: GetAverageWakeUpTimeInput) -> AverageWakeUpTimeOutput:
    result = analytics.get_average_wake_up_time(payload.participant_id)
    return AverageWakeUpTimeOutput(**result)


class DetectUnusualDaysInput(ParticipantIdInput):
    pass


class UnusualStepDay(StrictOutput):
    date: str
    value: float


class DetectUnusualDaysOutput(StrictOutput):
    participant: str
    number_of_unusual_days: int
    days: List[UnusualStepDay]


def run_detect_unusual_days(payload: DetectUnusualDaysInput) -> DetectUnusualDaysOutput:
    result = analytics.detect_unusual_days(payload.participant_id)
    # `date` values come back as datetime.date objects from pandas;
    # normalize to strings so the output model validates cleanly.
    days = [
        {"date": str(day["date"]), "value": float(day["value"])}
        for day in result["days"]
    ]
    return DetectUnusualDaysOutput(
        participant=result["participant"],
        number_of_unusual_days=result["number_of_unusual_days"],
        days=days,
    )


class GetMostActiveDayInput(ParticipantIdInput):
    pass


class MostActiveDayOutput(StrictOutput):
    participant: str
    most_active_day: str
    steps: int


def run_get_most_active_day(payload: GetMostActiveDayInput) -> MostActiveDayOutput:
    result = analytics.get_most_active_day(payload.participant_id)
    return MostActiveDayOutput(**result)


class GetHighestCalorieDayInput(ParticipantIdInput):
    pass


class HighestCalorieDayOutput(StrictOutput):
    participant: str
    highest_calorie_day: str
    calories: float


def run_get_highest_calorie_day(payload: GetHighestCalorieDayInput) -> HighestCalorieDayOutput:
    result = analytics.get_highest_calorie_day(payload.participant_id)
    return HighestCalorieDayOutput(**result)


class GetDailyLifestyleReportInput(ParticipantDateInput):
    pass


class DailyLifestyleReportOutput(StrictOutput):
    steps: StepsOutput
    distance: DistanceOutput
    calories: CaloriesOutput
    sleep: SleepDurationOutput
    wellness: WellnessOutput


def run_get_daily_lifestyle_report(payload: GetDailyLifestyleReportInput) -> DailyLifestyleReportOutput:
    result = reporting.get_daily_lifestyle_report(payload.participant_id, payload.date)
    return DailyLifestyleReportOutput(**result)
