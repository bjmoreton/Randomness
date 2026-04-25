"""
Why: Gives our validation system a standardized error model so the UI knows
     exactly which rule failed and what the error message is.
How: A Pydantic model containing the rule name, error message, and validation context.
"""

from typing import Any, Dict

from pydantic import BaseModel, Field


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
    context: Dict[str, Any] = Field(exclude=True)  # kwargs passed to validator
