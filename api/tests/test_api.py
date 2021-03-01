from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from api.constants import TEAM_STATS_TOTAL_FIELDS
from api.models import Employee
from api.models import Level
from api.models import MoodLevel


class TestMonitorAPI:
    @pytest.fixture(autouse=True)
    def set_up(self, create_users):
        self.client = APIClient()

    def test_add_mood_level(self):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"level": Level.SAD.value}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        record = MoodLevel.objects.all()
        assert len(record) == 1
        assert record[0].employee.id == emp_1.id
        assert record[0].level == Level.SAD.value

    @pytest.mark.parametrize(
        "level",
        [
            Level.SAD.value,
            Level.NORMAL.value,
            Level.GOOD.value,
            Level.BETTER.value,
            Level.EXCELLENT.value,
        ],
    )
    def test_add_mood_level_and_update(self, level):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post("/api/mood_levels", {"level": level}, format="json")
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        record = MoodLevel.objects.all()
        assert len(record) == 1
        assert record[0].employee.id == emp_1.id
        assert record[0].level == level

    @pytest.mark.parametrize(
        "level",
        [
            Level.SAD.value,
            Level.NORMAL.value,
            Level.GOOD.value,
            Level.BETTER.value,
            Level.EXCELLENT.value,
        ],
    )
    def test_add_mood_level_and_check_team_stats(self, level):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        data = {"level": level}
        res = self.client.post("/api/mood_levels", data, format="json")
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        res = self.client.get("/api/team_stats", data, format="json")
        assert res.status_code == HTTPStatus.OK
        res_data = res.json()
        assert isinstance(res_data, list)
        assert len(res_data) == 1

        team_data = res_data[0]
        assert "id" in team_data
        team_data.pop("id")

        assert "team" in team_data
        team_id = team_data.pop("team")
        assert team_id == 1

        total_field = TEAM_STATS_TOTAL_FIELDS[level]
        total_no = team_data.pop(total_field)
        assert total_no == 1

        assert "avg_mood" in team_data
        avg_mood = team_data.pop("avg_mood")
        assert avg_mood == level

        for value in team_data.values():
            assert value == 0

    @pytest.mark.parametrize(
        "emp_one_mood, emp_two_mood",
        [
            (Level.SAD.value, Level.GOOD.value),
            (Level.GOOD.value, Level.SAD.value),
            (Level.NORMAL.value, Level.EXCELLENT.value),
            (Level.BETTER.value, Level.GOOD.value),
            (Level.SAD.value, Level.SAD.value),
            (Level.NORMAL.value, Level.NORMAL.value),
            (Level.GOOD.value, Level.GOOD.value),
            (Level.BETTER.value, Level.BETTER.value),
            (Level.EXCELLENT.value, Level.EXCELLENT.value),
        ],
    )
    def test_add_multiple_members_mood_level_and_check_team_stats(
        self, emp_one_mood, emp_two_mood
    ):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"level": emp_one_mood}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        emp_2 = Employee.objects.filter(name="Test 2").first()
        self.client.force_authenticate(user=emp_2.user)
        res = self.client.post(
            "/api/mood_levels", {"level": emp_two_mood}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        res = self.client.get("/api/team_stats")
        assert res.status_code == HTTPStatus.OK
        res_data = res.json()
        assert isinstance(res_data, list)
        assert len(res_data) == 1

        team_data = res_data[0]
        assert "id" in team_data
        team_data.pop("id")

        assert "team" in team_data
        team_id = team_data.pop("team")
        assert team_id == 1

        if emp_one_mood == emp_two_mood:
            total_field = TEAM_STATS_TOTAL_FIELDS[emp_one_mood]
            assert total_field in team_data

            total_no = team_data.pop(total_field)
            assert total_no == 2

        else:
            for field in [emp_one_mood, emp_two_mood]:
                total_field = TEAM_STATS_TOTAL_FIELDS[field]
                assert total_field in team_data
                total_no = team_data.pop(total_field)
                assert total_no == 1

        assert "avg_mood" in team_data
        avg_mood = team_data.pop("avg_mood")
        assert avg_mood == int((emp_one_mood + emp_two_mood) / 2)

        for value in team_data.values():
            assert value == 0

    @pytest.mark.parametrize(
        "team_one_emp, team_two_emp",
        [
            (Level.SAD.value, Level.GOOD.value),
            (Level.GOOD.value, Level.SAD.value),
            (Level.NORMAL.value, Level.EXCELLENT.value),
            (Level.BETTER.value, Level.GOOD.value),
            (Level.SAD.value, Level.SAD.value),
            (Level.NORMAL.value, Level.NORMAL.value),
            (Level.GOOD.value, Level.GOOD.value),
            (Level.BETTER.value, Level.BETTER.value),
            (Level.EXCELLENT.value, Level.EXCELLENT.value),
        ],
    )
    def test_add_mood_level_with_multiple_teams(self, team_one_emp, team_two_emp):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"level": team_one_emp}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        emp_2 = Employee.objects.filter(name="Test 3").first()
        self.client.force_authenticate(user=emp_2.user)
        res = self.client.post(
            "/api/mood_levels", {"level": team_two_emp}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED

        self.client.force_authenticate(user=None)
        res = self.client.get("/api/team_stats")
        assert res.status_code == HTTPStatus.OK
        res_data = res.json()
        assert isinstance(res_data, list)
        assert len(res_data) == 2

        self.client.force_authenticate(user=emp_1.user)
        res = self.client.get("/api/team_stats")
        assert res.status_code == HTTPStatus.OK
        res_data = res.json()
        assert isinstance(res_data, list)
        assert len(res_data) == 1

        team_data = res_data[0]
        assert "team" in team_data
        assert team_data["team"] == 1

        total_field = TEAM_STATS_TOTAL_FIELDS[team_one_emp]
        assert total_field in team_data
        assert team_data[total_field] == 1

        assert "avg_mood" in team_data
        team_data["avg_mood"] == 1

        self.client.force_authenticate(user=emp_2.user)
        res = self.client.get("/api/team_stats")
        assert res.status_code == HTTPStatus.OK
        res_data = res.json()
        assert isinstance(res_data, list)
        assert len(res_data) == 1

        team_data = res_data[0]
        assert "team" in team_data
        assert team_data["team"] == 2

        total_field = TEAM_STATS_TOTAL_FIELDS[team_two_emp]
        assert total_field in team_data
        assert team_data[total_field] == 1
