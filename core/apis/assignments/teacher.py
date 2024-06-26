from flask import Blueprint,jsonify
from core import db
from core.apis import decorators
from marshmallow import ValidationError
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    # No need to filter again here since the method already filters by state
    teachers_assignments_dump = AssignmentSchema(many=True).dump(teachers_assignments)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    try:
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    except ValidationError as e:
        return jsonify({'error': 'ValidationError', 'message': str(e.messages)}), 400

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if not assignment:
        return jsonify({'error': 'FyleError', 'message': 'No assignment with this id was found'}), 404
    if assignment.teacher_id != p.teacher_id:
        return jsonify({'error': 'FyleError', 'message': 'You are not authorized to grade this assignment'}), 400
    
    
