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
    """Interface for mapping between two Result types across application layers.

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

    ...

    def map(
        self, result: Result[SuccessInputType, ErrorInputType]
    ) -> Result[SuccessOutputType, ErrorOutputType]:
        """Map a Result from one representation to another.

        Args:
            result: The input Result to be mapped from one type to another.

        Returns:
            The mapped Result with transformed success and error types.
        """
        ...
