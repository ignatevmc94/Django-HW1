import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve(course_factory, student_factory, client):
    course = course_factory(_quantity=1)[0]
    student = student_factory(_quantity=1)[0]
    response = client.get('/api/v1/courses/').json()[0]
    assert course.name == response['name']

@pytest.mark.django_db
def test_list(course_factory, student_factory, client):
    courses = course_factory(_quantity=10)
    students = student_factory(_quantity=10)
    response = client.get('/api/v1/courses/').json()
    resp_list, courses_list = [], []
    print()
    for resp in response:
        resp_list.append(resp['name'])
    print()
    for course in courses:
        courses_list.append(course.name)
    assert resp_list == courses_list

@pytest.mark.django_db
def test_id_filter(course_factory,student_factory, client):
    courses = course_factory(_quantity=10)
    students = student_factory(_quantity=10)
    response = client.get('/api/v1/courses/5/').json()
    for course in courses:
        if course.id == 5:
            assert course.name == response['name']

@pytest.mark.django_db
def test_name_filter(course_factory, student_factory, client):
    courses = course_factory(_quantity=10)
    students = student_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[-2].name}').json()
    assert response[0]['name'] == courses[-2].name

@pytest.mark.django_db
def test_course_creation(client):
    response = client.post('/api/v1/courses/', {'name': 'new created course'})
    assert response.status_code == 201

@pytest.mark.django_db
def test_course_update(course_factory, student_factory, client):
    course = course_factory(_quantity=1)[0]
    student = student_factory(_quantity=1)[0]
    response = client.patch(f'/api/v1/courses/{course.id}/', {'name': 'new name'}).json()
    assert response['name'] == 'new name'

@pytest.mark.django_db
def test_course_delete(course_factory, student_factory, client):
    course = course_factory(_quantity=1)[0]
    student = student_factory(_quantity=1)[0]
    response = client.delete(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204

