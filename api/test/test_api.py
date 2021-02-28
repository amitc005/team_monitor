from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from api.models import Employee
from api.models import MoodLevel


class TestMonitorAPI:
    @pytest.fixture(autouse=True)
    def set_up(self, create_users):
        self.client = APIClient()

    def test_add_mood_level(self):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        data = {"mood_level": 1}
        res = self.client.post("/api/mood_levels", data, format="json")
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        record = MoodLevel.objects.all()
        assert len(record) == 1
        assert record[0].employee.id == emp_1.id
        assert record[0].mood_level == data["mood_level"]

    @pytest.mark.parametrize("mood_level", [1, 2, 3, 4, 5])
    def test_add_mood_level_and_update(self, mood_level):
        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"mood_level": mood_level}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        record = MoodLevel.objects.all()
        assert len(record) == 1
        assert record[0].employee.id == emp_1.id
        assert record[0].mood_level == mood_level

    @pytest.mark.parametrize("mood_level", [1, 2, 3, 4, 5])
    def test_add_mood_level_and_check_team_stats(self, mood_level):
        field_dict = {
            1: "total_sad",
            2: "total_normal",
            3: "total_good",
            4: "total_better",
            5: "total_excellent",
        }

        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        data = {"mood_level": mood_level}
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

        total_field = field_dict[mood_level]
        total_no = team_data.pop(total_field)
        assert total_no == 1

        assert "avg_mood" in team_data
        avg_mood = team_data.pop("avg_mood")
        assert avg_mood == mood_level

        for value in team_data.values():
            assert value == 0

    @pytest.mark.parametrize(
        "emp_one_mood, emp_two_mood",
        [(1, 3), (3, 1), (2, 5), (4, 3), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    def test_add_multiple_members_mood_level_and_check_team_stats(
        self, emp_one_mood, emp_two_mood
    ):
        field_dict = {
            1: "total_sad",
            2: "total_normal",
            3: "total_good",
            4: "total_better",
            5: "total_excellent",
        }

        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"mood_level": emp_one_mood}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        emp_2 = Employee.objects.filter(name="Test 2").first()
        self.client.force_authenticate(user=emp_2.user)
        res = self.client.post(
            "/api/mood_levels", {"mood_level": emp_two_mood}, format="json"
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
            total_field = field_dict[emp_one_mood]
            assert total_field in team_data

            total_no = team_data.pop(total_field)
            assert total_no == 2

        else:
            for field in [emp_one_mood, emp_two_mood]:
                total_field = field_dict[field]
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
        [(1, 3), (3, 1), (2, 5), (4, 3), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    def test_add_mood_level_with_multiple_teams(self, team_one_emp, team_two_emp):
        field_dict = {
            1: "total_sad",
            2: "total_normal",
            3: "total_good",
            4: "total_better",
            5: "total_excellent",
        }

        emp_1 = Employee.objects.filter(name="Test 1").first()
        self.client.force_authenticate(user=emp_1.user)
        res = self.client.post(
            "/api/mood_levels", {"mood_level": team_one_emp}, format="json"
        )
        assert res.status_code == HTTPStatus.CREATED
        self.client.force_authenticate(user=None)

        emp_2 = Employee.objects.filter(name="Test 3").first()
        self.client.force_authenticate(user=emp_2.user)
        res = self.client.post(
            "/api/mood_levels", {"mood_level": team_two_emp}, format="json"
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

        total_field = field_dict[team_one_emp]
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

        total_field = field_dict[team_two_emp]
        assert total_field in team_data
        assert team_data[total_field] == 1