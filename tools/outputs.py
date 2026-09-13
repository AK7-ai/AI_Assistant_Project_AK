"""
tools/outputs.py

Output models that mirror the exact dict shapes returned by the underlying functions across every branch (data found / no data / not enough data). 
`extra="forbid"` is intentional: if a function's return shape ever drifts from what's modeled here, validation fails loudly instead of silently passing an unexpected field to the LLM.
"""

import datetime
from typing import List, Optional

from pydantic import BaseModel


class StrictOutput(BaseModel):
    model_config = {"extra": "forbid"}


class RestingHeartRateOutput(StrictOutput):
    participant: str
    date: str
    resting_heart_rate: Optional[float] = None


class SedentaryTimeOutput(StrictOutput):
    participant: str
    date: str
    sedentary_minutes: Optional[int] = None


class StepsOutput(StrictOutput):
    participant: str
    date: str
    steps: Optional[int] = None
    message: Optional[str] = None


class StepGoalProgressOutput(StrictOutput):
    participant: str
    date: str
    steps: Optional[int] = None
    goal: int
    goal_reached: Optional[bool] = None


class SleepDurationOutput(StrictOutput):
    participant: str
    date: str
    sleep_hours: Optional[float] = None
    message: Optional[str] = None


class SleepEfficiencyOutput(StrictOutput):
    participant: str
    date: str
    efficiency: Optional[int] = None


class WakeTimeOutput(StrictOutput):
    participant: str
    date: str
    wake_time: Optional[str] = None
    message: Optional[str] = None


class WellnessOutput(StrictOutput):
    participant: str
    date: str
    message: Optional[str] = None
    fatigue: Optional[int] = None
    mood: Optional[int] = None
    readiness: Optional[int] = None
    sleep_duration_h: Optional[int] = None
    sleep_quality: Optional[int] = None
    soreness: Optional[int] = None
    stress: Optional[int] = None


class LightActivityOutput(StrictOutput):
    participant: str
    date: str
    light_activity_minutes: Optional[int] = None


class ModerateActivityOutput(StrictOutput):
    participant: str
    date: str
    moderate_activity_minutes: Optional[int] = None


class VeryActiveOutput(StrictOutput):
    participant: str
    date: str
    very_active_minutes: Optional[int] = None


class DistanceOutput(StrictOutput):
    participant: str
    date: str
    distance_cm: int
    distance_km: float


class CaloriesOutput(StrictOutput):
    participant: str
    date: str
    calories: float


class InjuryStatusOutput(StrictOutput):
    participant: str
    date: str
    has_injury: bool
    details: Optional[str] = None


class ChartDataPoint(StrictOutput):
    date: str
    value: float
