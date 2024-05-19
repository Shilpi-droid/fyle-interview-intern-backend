from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse, APIError
from core.models.teachers import Teacher

principal_teacher_resources = Blueprint('principal_teacher_resources', __name__)

@principal_teacher_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    try:
        teachers = Teacher.query.all()
        teachers_dump = [{'id': teacher.id, 'user_id': teacher.user_id, 'created_at': teacher.created_at, 'updated_at': teacher.updated_at} for teacher in teachers]
        return APIResponse.respond(data=teachers_dump)
    except Exception as e:
        return APIError.respond(message=str(e))


# This file contains the route /teachers (GET) for listing all teachers in the system.