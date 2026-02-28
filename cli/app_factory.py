# cli/app_factory.py

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from application.services.student_management_system import StudentManagementSystem
from cli.application_api import StudentManagementSystemAPI
from cli.errors import ConfigurationError

from infrastructure.in_memory.in_memory_store import InMemoryStore
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.sqlite_transactional_sms import SqliteTransactionalStudentManagementSystem


@dataclass(frozen=True, slots=True)
class PersistenceConfig:
    """
    Persistence selection configuration.

    Owned by the composition root.

    The config object itself must not cross architectural boundaries;
    only primitive values derived from it may be passed downward
    during wiring.

    It answers one question only: which persistence backend is selected?
    """
    backend: Literal["memory", "sqlite"] = "memory"
    sqlite_path: Path | None = None


# ---------------------------------------------------------
# In-memory baseline (unchanged behavior)
# ---------------------------------------------------------

def _build_in_memory_sms() -> StudentManagementSystem:
    """
    Build the canonical in-memory StudentManagementSystem.

    This preserves the pre-Phase-5 object graph exactly and
    must remain behaviorally identical.
    """
    store = InMemoryStore()

    student_repo = InMemoryStudentRepository(store)
    teacher_repo = InMemoryTeacherRepository(store)
    course_repo = InMemoryCourseRepository(store)

    return StudentManagementSystem(
        student_repo=student_repo,
        teacher_repo=teacher_repo,
        course_repo=course_repo,
    )


# ---------------------------------------------------------
# Composition root
# ---------------------------------------------------------

def create_sms(
        config: PersistenceConfig | None = None,
) -> StudentManagementSystemAPI:
    """
    CLI composition root.

    Returns an object conforming to StudentManagementSystemAPI.

    Backend selection affects wiring only.
    """

    if config is None:
        config = PersistenceConfig()

    if config.backend == "memory":
        return _build_in_memory_sms()

    elif config.backend == "sqlite":
        if config.sqlite_path is None:
            raise ConfigurationError(
                "sqlite_path must be provided when backend='sqlite'."
            )

        db_path = config.sqlite_path

        # Defensive guard - should already be canonical from main()
        if not db_path.is_absolute():
            raise ConfigurationError(
                f"sqlite_path must be an absolute path, got: {str(db_path)!r}"
            )

        # ---------------------------------------------------------
        # Bootstrap ownership — composition root only (ADR-007)
        # ---------------------------------------------------------
        initialize_sqlite_database(db_path)

        return SqliteTransactionalStudentManagementSystem(
            sqlite_path=db_path,
        )

    else:
        # Exhaustive backend guard - enforces composition-root authority
        raise ConfigurationError(f"Unsupported backend: {config.backend!r}")



