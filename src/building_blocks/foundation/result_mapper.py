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

SuccessInputType = TypeVar("SuccessInputType", contravariant=True)
ErrorInputType = TypeVar("ErrorInputType", contravariant=True)
SuccessOutputType = TypeVar("SuccessOutputType", covariant=True)
ErrorOutputType = TypeVar("ErrorOutputType", covariant=True)


class ResultMapper(
    Mapper[
        Result[SuccessInputType, ErrorInputType],
        Result[SuccessOutputType, ErrorOutputType],
    ],
    Protocol,
    Generic[SuccessInputType, ErrorInputType, SuccessOutputType, ErrorOutputType],
):
    """Specialized Mapper for transforming Result types across layers.

    A ResultMapper is a Mapper that specifically handles Result transformations,
    typically when crossing architectural boundaries (e.g., domain → HTTP).

    This specialization makes the intent clear: we're mapping Results to Results,
    handling both success and error cases appropriately.

    Type Parameters:
        SuccessIn: Success type of input Result
        ErrorIn: Error type of input Result
        SuccessOut: Success type of output Result
        ErrorOut: Error type of output Result

    Example:
        >>> class TaskResultMapper(
        ...     ResultMapper[TaskDTO, DomainError, JSONResponse, ErrorResponse]
        ... ):
        ...     def map(self, result):
        ...         if result.is_ok():
        ...             return Result.ok(JSONResponse(result.unwrap()))
        ...         return Result.err(ErrorResponse(result.unwrap_err()))
    """

    def map(
        self, result: Result[SuccessInputType, ErrorInputType]
    ) -> Result[SuccessOutputType, ErrorOutputType]:
        """Map a Result from one type representation to another.

        Transforms both success and error types, typically when crossing
        architectural boundaries.

        Args:
            result: The input Result to transform

        Returns:
            A new Result with transformed types
        """
        ...
