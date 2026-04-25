"""
Why: Defines the building block of our validation system — a single named rule with
     a check function and an error message for when it fails.
How: The Rule class wraps a callable (sync or async) and provides validate() and negate() methods.
"""

import inspect
from typing import Awaitable, Callable, Dict, Generic, TypeVar, Union

T = TypeVar('T')


class Rule(Generic[T]):
    """
    Represents a single validation rule.

    Attributes:
        name (str): Unique name of the rule.
        check (Callable): Function that returns True if valid, False otherwise.
                          Can be sync or async.
        error_message (str): Message to return if validation fails.
    """

    def __init__(
        self,
        name: str,
        check: Callable[[T, Dict], Union[bool, Awaitable[bool]]],
        error_message: str,
    ):
        self.name = name
        self.check = check
        self.error_message = error_message

    def validate(self, value: T, **kwargs) -> Union[bool, Awaitable[bool]]:
        """
        Execute the validation check.

        Args:
            value (T): The value to validate.
            **kwargs: Additional context for the validation check.

        Returns:
            bool | Awaitable[bool]: Validation result.
        """
        # Pass kwargs as a single dict
        return self.check(value, **kwargs)

    def negate(self, message: str = None) -> 'Rule[T]':
        """
        Create a new Rule that is the negation of this rule.

        Args:
            message (str, optional): Custom error message for the negated rule.

        Returns:
            Rule[T]: A new rule with negated logic.
        """
        msg = message or f'NOT({self.name}): {self.error_message}'

        if inspect.iscoroutinefunction(self.check):

            async def negated_check(v, ctx):
                return not await self.check(v, ctx)

        else:

            def negated_check(v, ctx):
                return not self.check(v, ctx)

        return Rule(name=f'not_{self.name}', check=negated_check, error_message=msg)

    def __invert__(self):
        """Allow using the ~ operator to negate a rule."""
        return self.negate()
