# pragma: no cover
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
    """
    Maps a Result[SuccessInputType, ErrorInputType] from one layer or representation
    to another Result[SuccessOutputType, ErrorOutputType].

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

    def map(
        self, result: Result[SuccessInputType, ErrorInputType]
    ) -> Result[SuccessOutputType, ErrorOutputType]: ...
