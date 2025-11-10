"""This module defines a Protocol/Interface for mapping Result between different layers.

This modules defines a protocol for mapping Result types between different layers or
representations.

You can implement this protocol to create mappers that convert Result types from one
form to another, facilitating data transformation across application layers.

Example:
    ApplicationResult = Result[CreateTaskResponse, CombinedValidationErrors]
    HttpResult = Result[JSONResponse, ErrorResponse]

    class CreateTaskHttpResultMapper(
        ResultMapper[
            CreateTaskResponse,
            CombinedValidationErrors,
            JSONResponse,
            ErrorResponse
        ]
    ):
        def __init__(self, success_mapper: Mapper, error_mapper: Mapper):
            self.success_mapper = success_mapper
            self.error_mapper = error_mapper

        def map(self, result: ApplicationResult) -> HttpResult:
            if result.is_ok():
                data = self.success_mapper.map(result.unwrap())
                return Result.ok(data)
            else:
                error = self.error_mapper.map(result.unwrap_err())
                return Result.err(error)
"""

from typing import Generic, Protocol, TypeVar

from building_blocks.foundation.mapper import Mapper
from building_blocks.foundation.result import Result

SuccessIn = TypeVar("SuccessIn", contravariant=True)
ErrorIn = TypeVar("ErrorIn", contravariant=True)
SuccessOut = TypeVar("SuccessOut", covariant=True)
ErrorOut = TypeVar("ErrorOut", covariant=True)


class ResultMapper(  # type: ignore[misc]
    Generic[SuccessIn, ErrorIn, SuccessOut, ErrorOut],
    Mapper[
        Result[SuccessIn, ErrorIn],
        Result[SuccessOut, ErrorOut],
    ],
    Protocol,
):
    """Specialized Mapper for transforming Result types across layers.

    A ResultMapper is a Mapper that specifically handles Result transformations,
    typically when crossing architectural boundaries (e.g., domain → HTTP).

    This specialization makes the intent clear: we're mapping Results to Results,
    handling both success and error cases appropriately.

    The protocol uses variance annotations to ensure type safety:

    - ``SuccessIn`` and ``ErrorIn`` are **contravariant**: accepts the declared types or supertypes
    - ``SuccessOut`` and ``ErrorOut`` are **covariant**: returns the declared types or subtypes

    ------

    **Type Parameters**
    -------------------
    - SuccessIn: Success type of input Result
    - ErrorIn: Error type of input Result
    - SuccessOut: Success type of output Result
    - ErrorOut: Error type of output Result

    ------
    **Example Usage**
        >>> class TaskResultMapper(
        ...     ResultMapper[TaskDTO, DomainError, JSONResponse, ErrorResponse]
        ... ):
        ...     def map(self, result):
        ...         if result.is_ok():
        ...             return Result.ok(JSONResponse(result.unwrap()))
        ...         return Result.err(ErrorResponse(result.unwrap_err()))
    """

    _success_in: SuccessIn | None = None
    _error_in: ErrorIn | None = None
    _success_out: SuccessOut | None = None
    _error_out: ErrorOut | None = None

    def map(self, result: Result[SuccessIn, ErrorIn]) -> Result[SuccessOut, ErrorOut]:
        """Map a Result from one type representation to another.

        Transforms both success and error types, typically when crossing
        architectural boundaries.

        Args:
            result: The input Result to transform

        Returns:
            A new Result with transformed types
        """
        ...
