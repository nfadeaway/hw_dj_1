import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
from django_testing.settings import MAX_STUDENTS_PER_COURSE

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 200
    assert response.json()['id'] == courses[0].id

@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name

# Предполагается, что ID уникальные
@pytest.mark.django_db
def test_get_filtered_course_for_id(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/?id={courses[3].id}')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == courses[3].id

# Предполагается, что имена курсов уникальные
@pytest.mark.django_db
def test_get_filtered_course_for_name(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/?name={courses[3].name}')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == courses[3].name

@pytest.mark.django_db
def test_create_course(client, course_factory):
    count = Course.objects.count()
    response = client.post(f'/api/v1/courses/', data={'name': 'test name'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.patch(f'/api/v1/courses/{courses[3].id}/', data={'name': 'new test name'})
    assert response.status_code == 200
    response = client.get(f'/api/v1/courses/{courses[3].id}/')
    assert response.json()['name'] == 'new test name'

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=5)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{courses[3].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1

@pytest.mark.parametrize(
    'wrong_settings',
    [
        1, 5, 7, 20,
        pytest.param(21, marks=pytest.mark.xfail(reason='Максимальное число студентов на курсе не может быть больше 20')),
        pytest.param(-1, marks=pytest.mark.xfail(reason='Максимальное число студентов на курсе не может быть меньше 0'))
    ]
)
def test_max_students_per_course_settings(wrong_settings, settings):
    default_settings = 20
    settings.MAX_STUDENTS_PER_COURSE = wrong_settings
    assert 0 <= settings.MAX_STUDENTS_PER_COURSE <= default_settings
