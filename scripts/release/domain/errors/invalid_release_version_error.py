from forging_blocks.foundation import ErrorMessage, ErrorMetadata, ValidationError


class InvalidReleaseVersionError(ValidationError):
    def __init__(self, release_version: str) -> None:
        message = ErrorMessage(f"'{release_version}' should be bigger than v0.0.0")
        metadata = ErrorMetadata(context={"release_version": release_version})
        super().__init__(message, metadata)
