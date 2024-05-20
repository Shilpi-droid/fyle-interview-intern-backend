import pytest
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs import assertions
from core.libs.exceptions import FyleError
from core.apis.decorators import AuthPrincipal  # Adjust the import based on the actual location


@pytest.fixture
def non_draft_assignment():
    assignment = Assignment(
        id=1,  # Existing ID in your test database
        student_id=1,
        teacher_id=1,
        content="Non-draft content",
        state=AssignmentStateEnum.SUBMITTED  # Not in draft state
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment

@pytest.fixture
def new_assignment():
    assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="Test content",
        state=AssignmentStateEnum.DRAFT
    )
    return assignment

@pytest.fixture
def existing_assignment():
    assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="Initial content",
        state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment

@pytest.fixture
def non_draft_assignment():
    assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="Initial content",
        state=AssignmentStateEnum.SUBMITTED
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment

# Clean up the database after each test
@pytest.fixture(autouse=True)
def cleanup():
    yield
    db.session.rollback()
    db.session.close()

def test_upsert_new_assignment(new_assignment):
    """
    Test inserting a new assignment.
    """
    created_assignment = Assignment.upsert(new_assignment)
    assert created_assignment.id is not None
    assert created_assignment.content == "Test content"

def test_upsert_existing_assignment(existing_assignment):
    """
    Test updating an existing assignment in draft state.
    """
    existing_assignment.content = "Updated content"
    updated_assignment = Assignment.upsert(existing_assignment)
    assert updated_assignment.id == existing_assignment.id
    assert updated_assignment.content == "Updated content"


def test_upsert_assignments_same_state(existing_assignment):
    """
    Test upserting an assignment without changing its state.
    """
    existing_assignment.content = "Updated content again"
    updated_assignment = Assignment.upsert(existing_assignment)
    assert updated_assignment.id == existing_assignment.id
    assert updated_assignment.content == "Updated content again"
    assert updated_assignment.state == AssignmentStateEnum.DRAFT

def test_upsert_assignments_with_null_id():
    """
    Test upserting an assignment with null id.
    """
    new_assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="New Assignment Content",
        state=AssignmentStateEnum.DRAFT
    )
    created_assignment = Assignment.upsert(new_assignment)
    assert created_assignment.id is not None
    assert created_assignment.content == "New Assignment Content"
    assert created_assignment.state == AssignmentStateEnum.DRAFT



# Fixture for creating an assignment for testing
@pytest.fixture
def draft_assignment():
    assignment = Assignment(
        student_id=1,
        teacher_id=None,
        content="Draft content",
        state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment

# Fixture for creating a principal for testing
@pytest.fixture
def auth_principal():
    return AuthPrincipal(student_id=1, user_id=1)  # Include user_id

def test_submit_valid_assignment(draft_assignment, auth_principal):
    """
    Test submitting a valid assignment.
    """
    submitted_assignment = Assignment.submit(draft_assignment.id, teacher_id=1, auth_principal=auth_principal)
    assert submitted_assignment.state == AssignmentStateEnum.SUBMITTED
    assert submitted_assignment.teacher_id == 1

