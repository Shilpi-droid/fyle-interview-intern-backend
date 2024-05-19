from flask import Blueprint,jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    # Validate content is not null
    if 'content' not in incoming_payload or incoming_payload['content'] is None:
        return jsonify({'error': 'Bad Request', 'message': 'Content cannot be null'}), 400
    
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    try:
        submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth_principal=p
        )
        db.session.commit()  # Commit the session after making changes
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
        return APIResponse.respond(data=submitted_assignment_dump)
    except Exception as e:
        db.session.rollback()
        # logging.exception("An error occurred while submitting the assignment")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500



# @student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def submit_assignment(p, incoming_payload):
#     """Submit an assignment"""
#     try:
#         submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
        
#         # Check if the assignment is already submitted or not in a draft state
#         assignment = Assignment.query.filter_by(id=submit_assignment_payload.id).first()
#         if assignment is None:
#             return jsonify({'error': 'FyleError', 'message': 'No assignment with this id was found'}), 400
#         if assignment.teacher_id == submit_assignment_payload.teacher_id:
#             return jsonify({'error': 'FyleError', 'message': 'This assignment has already been submitted to this teacher'}), 400
#         if assignment.state != 'DRAFT':
#             return jsonify({'error': 'FyleError', 'message': 'Only a draft assignment can be submitted'}), 400

#         # Call the submit method if no existing assignment is found
#         submitted_assignment = Assignment.submit(
#             _id=submit_assignment_payload.id,
#             teacher_id=submit_assignment_payload.teacher_id,
#             auth_principal=p
#         )
#         db.session.commit()  # Commit the session after making changes
#         submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
#         return APIResponse.respond(data=submitted_assignment_dump)
#     except AssertionError as e:
#         return jsonify({'error': 'FyleError', 'message': str(e)}), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
