from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema

# Corrected Blueprint definition
principal_assignment_resources = Blueprint('principal_assignment_resources', __name__)


@principal_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    try:
        assignments = Assignment.query.filter(
            (Assignment.state == 'SUBMITTED') | (Assignment.state == 'GRADED')
        ).all()
        assignments_dump = AssignmentSchema().dump(assignments, many=True)
        return jsonify({'data': assignments_dump}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@principal_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    try:
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
        assignment_id = grade_assignment_payload.id

        # Check the state of the assignment
        assignment = Assignment.get_by_id(assignment_id)
        
        if assignment.state == AssignmentStateEnum.DRAFT:
            return jsonify({'error': 'Bad Request', 'message': 'Assignment is in Draft state and cannot be graded'}), 400

        # Grade the assignment
        graded_assignment = Assignment.mark_grade(
            _id=assignment_id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return jsonify({'data': graded_assignment_dump}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500