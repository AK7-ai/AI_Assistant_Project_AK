"""
tools/

Pydantic-validated wrappers around the PMData analytics functions, ready to be registered as LangGraph tools.

Usage:
    from tools.registry import TOOLS, TOOLS_BY_NAME

    spec = TOOLS_BY_NAME["get_resting_heart_rate"]
    payload = spec.input_model(participant_id="p01", date="2019-11-01")
    result = spec.run(payload)  # returns a validated output_model instance
"""

from tools.registry import TOOLS, TOOLS_BY_NAME

__all__ = ["TOOLS", "TOOLS_BY_NAME"]
