from marshmallow import Schema, EXCLUDE, fields, post_load, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_enum import EnumField
from core.models.teachers import Teacher
from core.models.assignments import Assignment, GradeEnum
from core.libs.helpers import GeneralObject


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(dump_only=True)
    user_id = auto_field()
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        return Teacher(**data_dict)


class TeacherCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Integer(required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        if 'user_id' not in data_dict:
            raise ValidationError("user_id is required")
        return GeneralObject(**data_dict)


class TeacherUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Integer(required=False, allow_none=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        return GeneralObject(**data_dict)


class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        unknown = EXCLUDE

    id = auto_field(dump_only=True)
    content = auto_field()
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    teacher_id = auto_field(dump_only=True)
    student_id = auto_field(dump_only=True)
    grade = auto_field(dump_only=True)
    state = auto_field(dump_only=True)


class AssignmentGradeSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    grade = EnumField(GradeEnum, required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        if 'id' not in data_dict or 'grade' not in data_dict:
            raise ValidationError("id and grade are required fields")
        return GeneralObject(**data_dict)