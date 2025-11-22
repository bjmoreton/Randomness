"""
utils/dynamic_validator/dynamic_validator.py

This module defines the DynamicValidator class, which orchestrates the validation process.
It allows adding rules, removing rules, and validating values against those rules
using various strategies (all, any, one). It handles both sync and async rules transparently.
"""

import asyncio
import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from utils import logger

from .rule import Rule
from .validation_error import ValidationError

T = TypeVar("T")


class DynamicValidator(Generic[T]):
    """
    Validator supporting mixed sync/async rules and callable in both sync and async contexts.

    This class manages a collection of validation rules and provides methods to
    validate values against them. It supports different validation modes:
    - is_valid: Returns True if all rules pass.
    - all_of: Returns True if all specified rules pass.
    - any_of: Returns True if at least one specified rule passes.
    - one_of: Returns True if exactly one specified rule passes.
    """

    def __init__(self, rules: Optional[List[Rule[T]]] = None):
        self.rules = rules or []

    # --- Rule management ---
    @overload
    def add_rule(self, rule: Rule[T]) -> "DynamicValidator": ...

    @overload
    def add_rule(
        self,
        name: str,
        check: Callable[[T, Dict], Union[bool, Awaitable[bool]]],
        error_message: str,
    ) -> "DynamicValidator": ...

    def add_rule(self, *args):
        """
        Add a validation rule to the validator.

        Can be called with a Rule object or with name, check function, and error message.

        Args:
            *args: Either (Rule) or (name, check, error_message).

        Returns:
            DynamicValidator: Self for method chaining.

        Raises:
            TypeError: If arguments are invalid.
            ValueError: If a rule with the same name already exists.
        """
        if len(args) == 1 and isinstance(args[0], Rule):
            rule = args[0]
        elif len(args) == 3 and isinstance(args[0], str):
            name, check, error_message = args
            rule = Rule(name=name, check=check, error_message=error_message)
        else:
            raise TypeError("Invalid arguments to add_rule")
        if any(r.name == rule.name for r in self.rules):
            raise ValueError(f"Rule '{rule.name}' already exists")
        self.rules.append(rule)
        return self

    def remove_rule(self, rule_name: str):
        """
        Remove a rule by name.

        Args:
            rule_name (str): Name of the rule to remove.

        Returns:
            DynamicValidator: Self for method chaining.
        """
        self.rules = [r for r in self.rules if r.name != rule_name]
        return self

    @property
    def rule_count(self):
        """Return the number of registered rules."""
        return len(self.rules)

    # --- Internal methods ---
    def _resolve_rules(self, names: List[str]) -> List[Rule[T]]:
        """Resolve rule names to Rule objects."""
        resolved = []
        for name in names:
            rule = next((r for r in self.rules if r.name == name), None)
            if rule is None:
                raise ValueError(f"Rule '{name}' not found in validator.")
            resolved.append(rule)
        return resolved

    async def _validate_rule(
        self, rule: Rule[T], value: Any, **kwargs
    ) -> Union[ValidationError, None]:
        """Validate a single rule against a value."""
        result = rule.validate(value, **kwargs)
        if inspect.isawaitable(result):
            result = await result
        if not result:
            return ValidationError(
                rule=rule.name,
                message=rule.error_message,
                value=value,
                context=kwargs,
            )
        return None

    async def _validate_rules(
        self, rules: List[Rule[T]], value: Any, **kwargs
    ) -> Tuple[int, List[ValidationError]]:
        """Validate multiple rules against a value."""
        passed = 0
        errors: List[ValidationError] = []
        for rule in rules:
            error = await self._validate_rule(rule, value, **kwargs)
            if error:
                errors.append(error)
            else:
                passed += 1
        return passed, errors

    # --- Core logic ---

    def _maybe_async(self, rules: List[Rule[T]], value: Any, method: str, **kwargs):
        """
        Execute validation logic, handling async/sync context automatically.

        If called within a running event loop, returns a coroutine.
        If called outside an event loop, runs synchronously via asyncio.run().
        """

        async def runner():
            passed, errors = await self._validate_rules(rules, value, **kwargs)

            if method in ("is_valid", "all"):
                return len(errors) == 0, errors

            elif method == "any":
                return passed > 0, errors

            elif method == "one":
                if passed == 1:
                    return True, errors
                elif passed == 0:
                    return False, errors
                else:
                    return False, [
                        ValidationError(
                            rule="one_of",
                            message=f"Expected exactly one rule to pass, but {passed} passed.",
                            value=value,
                            context={"rules": [r.name for r in rules]},
                        )
                    ]

        # If we are already inside an async event loop → return coroutine
        if asyncio.get_event_loop().is_running():
            return runner()  # caller must await this

        # Sync context (tests, CLIs)
        return asyncio.run(runner())

    # --- Public API ---
    def is_valid(self, value: Any, **kwargs) -> Union[
        Tuple[bool, List[ValidationError]],
        Awaitable[Tuple[bool, List[ValidationError]]],
    ]:
        """Check if all rules pass."""
        return self._maybe_async(self.rules, value, "is_valid", **kwargs)

    def all_of(self, rule_names: List[str], value: Any, **kwargs) -> Union[
        Tuple[bool, List[ValidationError]],
        Awaitable[Tuple[bool, List[ValidationError]]],
    ]:
        """Check if all specified rules pass."""
        rules = self._resolve_rules(rule_names) if rule_names else self.rules
        return self._maybe_async(rules, value, "all", **kwargs)

    def any_of(self, rule_names: List[str], value: Any, **kwargs) -> Union[
        Tuple[bool, List[ValidationError]],
        Awaitable[Tuple[bool, List[ValidationError]]],
    ]:
        """Check if at least one of the specified rules passes."""
        rules = self._resolve_rules(rule_names) if rule_names else self.rules
        return self._maybe_async(rules, value, "any", **kwargs)

    def one_of(self, rule_names: List[str], value: Any, **kwargs) -> Union[
        Tuple[bool, List[ValidationError]],
        Awaitable[Tuple[bool, List[ValidationError]]],
    ]:
        """Check if exactly one of the specified rules passes."""
        rules = self._resolve_rules(rule_names) if rule_names else self.rules
        return self._maybe_async(rules, value, "one", **kwargs)

    def __call__(
        self, value: Any, method: str = "all", rule_names: List[str] = None, **kwargs
    ) -> Union[
        Tuple[bool, List[ValidationError]],
        Awaitable[Tuple[bool, List[ValidationError]]],
    ]:
        """Callable interface for the validator."""
        return self._maybe_async(
            self.rules if not rule_names else self._resolve_rules(rule_names),
            value,
            method,
            **kwargs,
        )
