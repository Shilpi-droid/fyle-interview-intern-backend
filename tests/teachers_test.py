from core import db
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
    db.session.rollback()


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'
    db.session.rollback()


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'
    db.session.rollback()


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
    db.session.rollback()



#----------------------new tests-----------------------------------------


def test_list_teachers_with_data(client, h_principal):
    """
    Test listing teachers when there are teachers in the system.
    """
    # Make the request to list teachers
    response = client.get('/principal_teacher/teachers', headers=h_principal)

    # Check the response status code
    assert response.status_code == 200

    # Check that the response contains the correct structure with data
    assert 'data' in response.json
    assert isinstance(response.json['data'], list)
    assert len(response.json['data']) == 2
    assert response.json['data'][0]['id'] == 1
    assert response.json['data'][1]['id'] == 2

def test_list_teachers_invalid_auth(client):
    """
    Test listing teachers with invalid authentication.
    """
    # Make the request to list teachers without authentication token
    response = client.get('/principal_teacher/teachers')

    # Check the response status code
    assert response.status_code == 401

def test_list_teachers_missing_auth(client):
    """
    Test listing teachers with missing authentication token.
    """
    # Make the request to list teachers with missing authentication token
    response = client.get('/principal_teacher/teachers')

    # Check the response status code
    assert response.status_code == 401


#---------------------------------------------------------------------------------

import json


# def test_list_assignments_empty(client, h_principal):
#     """
#     Test listing assignments when no assignments exist for the teacher.
#     """
#     # Ensure that there are no assignments associated with the teacher
#     # Make the request to list assignments
#     response = client.get('/teacher/assignments', headers=h_principal)

#     # Check the response status code
#     assert response.status_code == 200

#     # Check that the response contains an empty list of assignments
#     data = response.json
#     assert 'data' in data
#     assert isinstance(data['data'], list)
#     assert len(data['data']) == 0
#     # Add more assertions if needed


# def test_grade_assignment_successful(client, h_teacher_1):
#     """
#     Test grading a valid assignment successfully.
#     """
#     # Create a mock assignment associated with the teacher
#     # Make the request to grade the assignment
#     response = client.post(
#         '/teacher/assignments/grade',
#         headers=h_teacher_1,
#         json={'id': 1, 'grade': 'A'}
#     )

#     # Check the response status code
#     assert response.status_code == 200

#     # Check that the response contains the graded assignment data
#     data = response.json
#     assert 'data' in data
#     # Add more assertions if needed


# Add more test functions to cover various error scenarios for grade_assignment route



