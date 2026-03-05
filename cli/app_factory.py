# cli/app_factory.py

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Literal

from application.services.student_management_system import StudentManagementSystem
from cli.application_api import StudentManagementSystemAPI
from cli.errors import ConfigurationError

from infrastructure.in_memory.in_memory_store import InMemoryStore
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)

@dataclass(frozen=True, slots=True)
class PersistenceConfig:
    """
    Persistence selection configuration.

    Owned strictly by the composition root.

    This object represents a *resolved backend selection* and contains only
    wiring values required to build the object graph.

    It does NOT encode runtime policy or environment defaults. Default backend
    selection is decided by the CLI entry point (see cli/main.py), not by this
    data structure.

    Backends:
        - "sqlite"  → Production-intended backend (selected explicitly)
        - "memory"  → Default fallback for CLI/tests (selected explicitly or by default)

    The config object itself must not cross architectural boundaries; only
    primitives derived from it may be passed downward during wiring.
    """
    backend: Literal["memory", "sqlite"] = "memory"
    sqlite_path: Path | None = None


# ---------------------------------------------------------
# Backend builder typing (wiring-only)
# ---------------------------------------------------------

BackendBuilder = Callable[[PersistenceConfig], StudentManagementSystem]


# ---------------------------------------------------------
# In-memory baseline (unchanged behavior)
# ---------------------------------------------------------

def _build_in_memory_sms(config: PersistenceConfig) -> StudentManagementSystem:
    """
    Build the canonical in-memory StudentManagementSystem.

    Detached semantics require a shared in-memory store across repositories.
    """
    _ = config    # explicit: config is accepted for a uniform builder signature

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
# SQLite backend
# ---------------------------------------------------------

def _build_sqlite_sms(config: PersistenceConfig) -> StudentManagementSystem:
    """
    Build the SQLite-backed StudentManagementSystem.

    Requires:
        config.sqlite_path is provided and absolute.

    Bootstrap ownership:
        Database initialization occurs only at the composition root.
    """
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

    # Bootstrap ownership — composition root only
    initialize_sqlite_database(db_path)

    return SqliteTransactionalStudentManagementSystem(
        sqlite_path=db_path,
    )


# ---------------------------------------------------------
# Backend dispatch table (typed)
# ---------------------------------------------------------

_BACKEND_BUILDERS: Dict[str, BackendBuilder] = {
    "memory": _build_in_memory_sms,
    "sqlite": _build_sqlite_sms,
}


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

    try:
        builder = _BACKEND_BUILDERS[config.backend]
    except KeyError:
        raise ConfigurationError(
            f"Unsupported backend: {config.backend!r}"
        ) from None

    return builder(config)

