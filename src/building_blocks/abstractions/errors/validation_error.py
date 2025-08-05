from building_blocks.abstractions.errors.base import Error, Errors


class ValidationError(Error):
    """
    Base class for validation errors.
    """

    def __str__(self) -> str:
        return f"Validation Error: {super().__str__()}"


class ValidationErrors(Errors):
    """
    A collection of validation errors.
    This class is used to group multiple validation errors together,
    allowing for easier handling and reporting of validation issues.
    """

    def __str__(self) -> str:
        error_messages = "\n".join(f" - {str(error)}" for error in self.errors)
        return f"Validation errors for field '{self.field.value}':\n{error_messages}"
