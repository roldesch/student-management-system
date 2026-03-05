ADR-00E — Domain Entity Identity Equality

Status: Accepted
Implemented: Yes
Scope: Domain layer only
Phase Context: Post Phase-4B parity stabilization
Related ADRs: ADR-00C, ADR-00T, ADR-00X, ADR-00Y, ADR-00Z

1️⃣ Context

During SQLite persistence integration (Phase-6), a structural issue was exposed:

Two distinct in-memory entity instances with the same identity could coexist within the same aggregate and bypass duplicate detection invariants.

Example:

course = Course("C1", "Math")

s1 = Student("S1", "Alice")
s2 = Student("S1", "Alice")  # same identity, different instance

course.enroll(s1)
course.enroll(s2)  # ❌ should raise EnrollmentError

Because equality was instance-based, membership checks:

if student in self._students:

failed to detect identity duplication.

This caused:

Domain invariants to be bypassed

Persistence layer UNIQUE constraint violations

Incorrect CLI exit classification (Exit 10 instead of Exit 3)

This behavior violated domain authority boundaries (ADR-00X) and allowed persistence to enforce what should be a domain invariant.

2️⃣ Problem Statement

Entities were using default object identity for equality:

student1 != student2 even if IDs matched

Membership semantics (in) relied on instance identity

Dictionaries keyed by entities treated reconstructed entities as distinct

This breaks DDD identity semantics:

Entities are equal if and only if their identity is equal.

3️⃣ Decision

Implement identity-based equality for all domain entities:

Student

Teacher

Course

Equality semantics are:

Based solely on immutable identity attribute (_id or _code)

Strict type equality (type(self) is type(other))

Hash derived solely from identity

No runtime immutability enforcement

4️⃣ Implementation

Each entity implements:

# ---------- Identity-based equality (ADR-00E) ----------
def __eq__(self, other: object) -> bool:
    if self is other:
        return True

    if type(self) is not type(other):
        return NotImplemented

    return self._id == other._id  # or _code for Course

def __hash__(self) -> int:
    return hash(self._id)  # or _code for Course
Type Discipline

We use:

type(self) is type(other)

instead of isinstance() to:

Prevent subclass equality leakage

Avoid asymmetric equality behavior

Maintain strict entity identity semantics

Hash Discipline

__hash__ matches identity equality to ensure:

Correct set membership

Correct dictionary key behavior

Consistency with Python equality protocol

5️⃣ Identity Immutability Strategy

Two strategies were considered:

Option A — Documented Constraint (Chosen)

Identity must not be reassigned after construction

No runtime guard

No __setattr__ override

Simpler and lower risk

Enforced by convention and discipline

Option B — Runtime Enforcement (Rejected)

Override __setattr__

Block reassignment of _id / _code

Higher complexity

Higher risk

Not necessary at current project maturity

We adopted Option A.

Identity immutability is a documented invariant, not a runtime-enforced one.

6️⃣ Aggregate Integrity Impact

After implementation:

Student Enrollment
if student in self._students:

Now correctly detects identity duplicates across reconstructed instances.

Domain invariant is enforced before persistence layer.

Teacher Assignment

Teacher assignment invariant is cardinality-based:

if self._teacher is not None:

It does not depend on equality semantics.

No change required.

7️⃣ Dictionary Semantics Impact

Student._grades:

self._grades: Dict[Course, float]

After ADR-00E:

Two reconstructed Course("C1") instances are equal and hash-identical.

This enables correct grade lookup across reconstructed instances:

student.assign_grade(course1, 8.0)
student.get_grade(course2)  # now works if identity matches

This is correct DDD behavior.

8️⃣ Accepted Trade-off

If two instances with same identity diverge in state:

s1 = Student("S1", "Alice")
s2 = Student("S1", "Bob")

They collapse under dictionary semantics:

{ s1: "x", s2: "y" }  # one key remains

This is intentional and consistent with DDD:

Identity defines equality, not object state.

Session/repository discipline must prevent divergent instances.

This is an infrastructure responsibility, not a domain equality concern.

9️⃣ Testing Strategy
Added Test (Identity Enforcement)

Only one reconstruction test is required:

test_enrolling_two_distinct_student_instances_with_same_identity_raises_enrollmenterror

This test:

Fails under instance-based equality (RED)

Passes only after identity-based equality implementation (GREEN)

Teacher reconstruction test was removed because:

Teacher invariant is cardinality-based

It does not depend on equality semantics

It already has proper coverage

🔟 Architectural Boundaries Preserved

ADR-00E does NOT:

Introduce StateError

Modify exception taxonomy

Change repository behavior

Change CLI classification

Modify aggregate logic

Introduce identity map

Add runtime immutability guards

Introduce value objects

Modify persistence schema

It strictly defines entity equality semantics.

This preserves:

ADR-00Y repository contract discipline

ADR-00Z taxonomy freeze (Phase-4B)

ADR-00X domain authority boundaries

ADR-00C constructor-safe reconstruction guarantees

1️⃣1️⃣ Outcome

After implementation:

Domain invariants enforce identity duplication correctly

Persistence no longer compensates for domain equality weakness

CLI exit codes correctly classify domain violations

Cross-backend parity preserved

No taxonomy drift introduced

ADR-00E is fully implemented and verified.

1️⃣2️⃣ Enforcement Rules (Post-Adoption)

Violations include:

Manual ID comparisons inside aggregates (s.id == other.id)

Removing or bypassing identity-based equality

Changing equality to include mutable state

Returning False instead of NotImplemented for cross-type comparison

Modifying __hash__ to include non-identity attributes

Introducing subclass-based equality via isinstance

Identity semantics must remain:

Strictly type-based and strictly identity-based.

Final Statement

ADR-00E restores proper DDD identity semantics to the domain layer, ensuring that:

Aggregate invariants rely on equality correctly

Identity duplication is detected at the domain boundary

Persistence remains an implementation detail

Clean Architecture layering is preserved

Status: Implemented and Locked.