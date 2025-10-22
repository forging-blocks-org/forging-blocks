from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from examples.tasker_primitive_obsession.src.domain.errors.task_due_date_errors import (
    DueDateCannotBeInPastError,
    DueDateCannotBeOneYearInFutureError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_id_errors import (
    InvalidTaskIdError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_priority_error import (
    InvalidTaskPriorityError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_progress_error import (
    InvalidTaskProgressError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_status_errors import (
    InvalidTaskStatusError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_tags_errors import (
    InvalidTaskTagError,
)
from examples.tasker_primitive_obsession.src.domain.errors.task_title_errors import (
    OutOfLimitsTaskTitleError,
)
from examples.tasker_primitive_obsession.src.domain.errors.user_email_errors import (
    InvalidEmailFormatError,
)

from building_blocks.abstractions.errors.core import FieldReference
from building_blocks.abstractions.errors.validation_error import (
    CombinedValidationErrors,
    ValidationError,
    ValidationFieldErrors,
)
from building_blocks.foundation.result import Err, Ok, Result
from building_blocks.domain.aggregate_root import AggregateRoot, AggregateVersion
from building_blocks.domain.entity import DraftEntity


class BaseTask:
    TITLE_MIN_LENGTH = 3
    TITLE_MAX_LENGTH = 100

    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_BLOCKED = "blocked"
    STATUS_CANCELLED = "cancelled"
    STATUS_REVIEW = "review"
    STATUS_TESTING = "testing"
    _VALID_STATUSES = [
        STATUS_TODO,
        STATUS_IN_PROGRESS,
        STATUS_DONE,
        STATUS_BLOCKED,
        STATUS_CANCELLED,
        STATUS_REVIEW,
        STATUS_TESTING,
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"
    PRIORITY_CRITICAL = "critical"
    _VALID_PRIORITIES = [
        PRIORITY_LOW,
        PRIORITY_MEDIUM,
        PRIORITY_HIGH,
        PRIORITY_URGENT,
        PRIORITY_CRITICAL,
    ]

    MIN_PROGRESS = 0
    MAX_PROGRESS = 100
    _VALID_PROGRESS_RANGE = range(MIN_PROGRESS, MAX_PROGRESS + 1)

    @classmethod
    def _validate_id(
        cls, id: Optional[int] = None
    ) -> Result[Optional[int], ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if id and isinstance(id, int) and id <= 0:
            errors.append(InvalidTaskIdError())
        if errors:
            return Err(ValidationFieldErrors(field=FieldReference("id"), errors=errors))
        return Ok(id)

    @classmethod
    def _validate_title(cls, title: str) -> Result[str, ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if len(title) < cls.TITLE_MIN_LENGTH or len(title) > cls.TITLE_MAX_LENGTH:
            errors.append(
                OutOfLimitsTaskTitleError(
                    min_length=cls.TITLE_MIN_LENGTH, max_length=cls.TITLE_MAX_LENGTH
                )
            )
        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("title"), errors=errors)
            )

        return Ok(title)

    @classmethod
    def _validate_description(
        cls, description: str
    ) -> Result[str, ValidationFieldErrors]:
        return Ok(description)

    @classmethod
    def _validate_due_date(
        cls, due_date: datetime.date
    ) -> Result[datetime.date, ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if due_date < datetime.date.today():
            errors.append(DueDateCannotBeInPastError())
        if due_date.year > datetime.date.today().year + 1:
            errors.append(DueDateCannotBeOneYearInFutureError())
        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("due_date"), errors=errors)
            )
        return Ok(due_date)

    @classmethod
    def _validate_status(cls, status: str) -> Result[str, ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if status not in cls._VALID_STATUSES:
            errors.append(InvalidTaskStatusError(valid_statuses=cls._VALID_STATUSES))
        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("status"), errors=errors)
            )
        return Ok(status)

    @classmethod
    def _validate_priority(cls, priority: str) -> Result[str, ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if priority not in cls._VALID_PRIORITIES:
            errors.append(
                InvalidTaskPriorityError(valid_priorities=cls._VALID_PRIORITIES)
            )
        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("priority"), errors=errors)
            )
        return Ok(priority)

    @classmethod
    def _validate_tags(
        cls, tags: Optional[List[str]]
    ) -> Result[List[str], ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if tags is not None and not all(
            isinstance(tag, str) and tag.strip() for tag in tags
        ):
            errors.append(InvalidTaskTagError())
        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("tags"), errors=errors)
            )
        return Ok(tags if tags is not None else [])

    @classmethod
    def _validate_progress(cls, progress: int) -> Result[int, ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if progress not in cls._VALID_PROGRESS_RANGE:
            errors.append(
                InvalidTaskProgressError(
                    min_progress=cls.MIN_PROGRESS, max_progress=cls.MAX_PROGRESS
                )
            )

        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("progress"), errors=errors)
            )
        return Ok(progress)

    @classmethod
    def _validate_assignee_email(
        cls, assignee_email: Optional[str]
    ) -> Result[Optional[str], ValidationFieldErrors]:
        errors: List[ValidationError] = []
        if assignee_email is not None and "@" not in assignee_email:
            errors.append(InvalidEmailFormatError())
        if errors:
            return Err(
                ValidationFieldErrors(
                    field=FieldReference("assignee_email"), errors=errors
                )
            )
        return Ok(assignee_email)

    @classmethod
    def _validate_task(
        cls,
        id: Optional[int],
        title: str,
        description: str,
        due_date: datetime.date,
        status: str = STATUS_TODO,
        priority: str = PRIORITY_MEDIUM,
        tags: Optional[List[str]] = None,
        progress: int = 0,
        assignee_email: Optional[str] = None,
    ) -> Result[Dict[str, Any], CombinedValidationErrors]:
        errors: List[ValidationFieldErrors] = []
        id_result = cls._validate_id(id)
        title_result = cls._validate_title(title)
        description_result = cls._validate_description(description)
        due_date_result = cls._validate_due_date(due_date)
        status_result = cls._validate_status(status)
        priority_result = cls._validate_priority(priority)
        tags_result = cls._validate_tags(tags)
        progress_result = cls._validate_progress(progress)
        assignee_email_result = cls._validate_assignee_email(assignee_email)
        for result in [
            id_result,
            title_result,
            description_result,
            due_date_result,
            status_result,
            priority_result,
            tags_result,
            progress_result,
            assignee_email_result,
        ]:
            if isinstance(result, Err):
                errors.append(result.error)
        if errors:
            return Err(CombinedValidationErrors(errors=errors))
        return Ok(
            {
                "id": id_result.value,
                "title": title_result.value,
                "description": description_result.value,
                "due_date": due_date_result.value,
                "status": status_result.value,
                "priority": priority_result.value,
                "tags": tags_result.value,
                "progress": progress_result.value,
                "assignee_email": assignee_email_result.value,
            }
        )


class DraftTask(BaseTask, DraftEntity[int]):
    def __init__(
        self,
        id: Optional[int],
        title: str,
        description: str,
        due_date: datetime.date,
        status: str = BaseTask.STATUS_TODO,
        priority: str = BaseTask.PRIORITY_MEDIUM,
        tags: Optional[List[str]] = None,
        progress: int = 0,
        assignee_email: Optional[str] = None,
    ) -> None:
        super().__init__(id)
        self._title = title
        self._description = description
        self._due_date = due_date
        self._status = status
        self._priority = priority
        self._tags = tags if tags is not None else []
        self._progress = progress
        self._assignee_email = assignee_email

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self._id!r},\n"
            f"    title={self._title!r},\n"
            f"    description={self._description!r},\n"
            f"    due_date={self._due_date!r},\n"
            f"    status={self._status!r},\n"
            f"    priority={self._priority!r},\n"
            f"    tags={self._tags!r},\n"
            f"    progress={self._progress!r},\n"
            f"    assignee_email={self._assignee_email!r}\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DraftTask):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash((self._id, self._description, self._status))

    @classmethod
    def create(
        cls,
        id: Optional[int],
        title: str,
        description: str,
        due_date: datetime.date,
        status: str = BaseTask.STATUS_TODO,
        priority: str = BaseTask.PRIORITY_MEDIUM,
        tags: Optional[List[str]] = None,
        progress: int = 0,
        assignee_email: Optional[str] = None,
    ) -> Result[DraftTask, CombinedValidationErrors]:
        task_result = cls._validate_task(
            id=id,
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
            tags=tags,
            progress=progress,
            assignee_email=assignee_email,
        )
        if isinstance(task_result, Err):
            return Err(task_result.error)

        draft_task = cls(
            id=task_result.value["id"],
            title=task_result.value["title"],
            description=task_result.value["description"],
            due_date=task_result.value["due_date"],
            status=task_result.value["status"],
            priority=task_result.value["priority"],
            tags=task_result.value["tags"],
            progress=task_result.value["progress"],
            assignee_email=task_result.value["assignee_email"],
        )
        return Ok(draft_task)

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> str:
        return self._status

    @property
    def due_date(self) -> datetime.date:
        return self._due_date

    @property
    def priority(self) -> str:
        return self._priority

    @property
    def tags(self) -> List[str]:
        return self._tags.copy()

    @property
    def progress(self) -> int:
        return self._progress

    @property
    def assignee_email(self) -> Optional[str]:
        return self._assignee_email


class Task(BaseTask, AggregateRoot[int]):
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        due_date: datetime.date,
        status: str,
        priority: str,
        tags: Optional[List[str]],
        progress: int,
        assignee_email: Optional[str],
        version: Optional[AggregateVersion] = None,
    ) -> None:
        super().__init__(id, version)
        self._title = title
        self._description = description
        self._due_date = due_date
        self._status = status
        self._priority = priority
        self._tags = tags if tags is not None else []
        self._progress = progress
        self._assignee_email = assignee_email

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self._id!r},\n"
            f"    title={self._title!r},\n"
            f"    description={self._description!r},\n"
            f"    due_date={self._due_date!r},\n"
            f"    status={self._status!r},\n"
            f"    priority={self._priority!r},\n"
            f"    tags={self._tags!r},\n"
            f"    progress={self._progress!r},\n"
            f"    assignee_email={self._assignee_email!r}\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash((self._id, self._description, self._status, self._version))

    def change_status(self, new_status: str) -> None:
        if new_status not in self._VALID_STATUSES:
            raise InvalidTaskStatusError(valid_statuses=self._VALID_STATUSES)
        self._status = new_status

    def change_priority(self, new_priority: str) -> None:
        if new_priority not in self._VALID_PRIORITIES:
            raise InvalidTaskPriorityError(valid_priorities=self._VALID_PRIORITIES)
        self._priority = new_priority

    def edit_title(self, new_title: str):
        if not (self.TITLE_MIN_LENGTH <= len(new_title) <= self.TITLE_MAX_LENGTH):
            raise OutOfLimitsTaskTitleError(
                min_length=self.TITLE_MIN_LENGTH, max_length=self.TITLE_MAX_LENGTH
            )
        self._title = new_title

    def edit_description(self, new_description: str):
        self._description = new_description

    def edit_due_date(self, new_due_date: datetime.date):
        if new_due_date < datetime.date.today():
            raise DueDateCannotBeInPastError()
        if new_due_date.year > datetime.date.today().year + 1:
            raise DueDateCannotBeOneYearInFutureError()
        self._due_date = new_due_date

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> str:
        return self._status

    @property
    def due_date(self) -> datetime.date:
        return self._due_date

    @property
    def priority(self) -> str:
        return self._priority

    @property
    def tags(self) -> List[str]:
        return self._tags.copy()

    @property
    def progress(self) -> int:
        return self._progress

    @property
    def assignee_email(self) -> Optional[str]:
        return self._assignee_email
