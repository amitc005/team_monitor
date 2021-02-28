import pytest
from django.contrib.auth.models import User

from api.models import Employee
from api.models import Team


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def create_users():
    user_1 = User.objects.create_user(
        "testuser1", "testuser1@thebeatles.com", "test123"
    )
    user_2 = User.objects.create_user(
        "testuser2", "testuser2@thebeatles.com", "test123"
    )
    user_3 = User.objects.create_user(
        "testuser3", "testuser3@thebeatles.com", "test123"
    )
    user_4 = User.objects.create_user(
        "testuser4", "testuser4@thebeatles.com", "test123"
    )
    user_5 = User.objects.create_user(
        "testuser5", "testuser5@thebeatles.com", "test123"
    )
    user_6 = User.objects.create_user(
        "testuser6", "testuser6@thebeatles.com", "test123"
    )

    team_1 = Team(name="Team 1", description="Team 1")
    team_1.save()
    team_2 = Team(name="Team 2", description="Team 2")
    team_2.save()
    team_3 = Team(name="Team 3", description="Team 3")
    team_3.save()

    emp_1 = Employee(user=user_1, team=team_1, name="Test 1")
    emp_1.save()
    emp_2 = Employee(user=user_2, team=team_1, name="Test 2")
    emp_2.save()
    emp_3 = Employee(user=user_3, team=team_2, name="Test 3")
    emp_3.save()
    emp_4 = Employee(user=user_4, team=team_2, name="Test 4")
    emp_4.save()
    emp_5 = Employee(user=user_5, team=team_3, name="Test 5")
    emp_5.save()
    emp_6 = Employee(user=user_6, team=team_3, name="Test 6")
    emp_6.save()
