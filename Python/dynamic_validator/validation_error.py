"""
utils/dynamic_validator/validation_error.py

This module defines the ValidationError model used to report validation failures.
"""

from typing import Any, Dict

from pydantic import BaseModel


class ValidationError(BaseModel):
    """
    Represents a validation error.

    Attributes:
        rule (str): Name of the rule that failed.
        message (str): Error message explaining the failure.
        context (Dict[str, Any]): Context data available during validation.
    """

    rule: str
    message: str
    context: Dict[str, Any]  # kwargs passed to validator
