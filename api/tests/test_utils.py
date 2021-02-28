import pytest

from api.constants import TEAM_STATS_TOTAL_FIELDS
from api.models import Employee
from api.models import MoodLevel
from api.models import TeamStatistic
from api.utils import update_team_statistic


class TestMonitorAPI:
    @pytest.fixture(autouse=True)
    def set_up(self, create_users):
        pass

    def test_update_team_statistic_with_one_employee(self):
        mood_level_value = 1
        emp_1 = Employee.objects.filter(name="Test 1").first()
        mood_level = MoodLevel.objects.create(employee=emp_1, level=mood_level_value)
        mood_level.save()

        update_team_statistic(emp_1.team, mood_level)
        team_stats = TeamStatistic.objects.all()
        assert len(team_stats) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[mood_level_value]) == 1

    def test_update_team_statistic_with_one_employee_with_old_value(self):
        mood_level_value = 1
        emp_1 = Employee.objects.filter(name="Test 1").first()
        mood_level = MoodLevel.objects.create(employee=emp_1, level=mood_level_value)
        mood_level.save()

        update_team_statistic(emp_1.team, mood_level)
        team_stats = TeamStatistic.objects.all()
        assert len(team_stats) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[mood_level_value]) == 1

        new_mood_level = 5
        new_mood_record = MoodLevel.objects.get(employee=emp_1)
        assert new_mood_record.level == mood_level_value
        new_mood_record.level = new_mood_level
        new_mood_record.save()
        update_team_statistic(emp_1.team, new_mood_record, mood_level)

        team_stats = TeamStatistic.objects.all()
        assert len(team_stats) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[new_mood_level]) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[mood_level_value]) == 0

    def test_update_team_statistic_with_multiple_employee_with_same_team(self):
        emp_one_mood = 1
        employee_one = Employee.objects.filter(name="Test 1").first()
        team = employee_one.team
        mood_level = MoodLevel.objects.create(employee=employee_one, level=emp_one_mood)
        mood_level.save()
        update_team_statistic(team, mood_level)

        emp_two_mood = 2
        employee_two = Employee.objects.filter(name="Test 2").first()
        mood_level = MoodLevel.objects.create(employee=employee_two, level=emp_two_mood)
        mood_level.save()
        update_team_statistic(employee_two.team, mood_level)

        team_stats = TeamStatistic.objects.all()

        assert team.id == employee_two.team.id
        assert len(team_stats) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[emp_one_mood]) == 1
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[emp_two_mood]) == 1

    def test_update_team_statistic_with_multiple_employee_with_different_team(self):
        team_one_emp_mood = 1
        employee_one = Employee.objects.filter(name="Test 1").first()
        mood_level = MoodLevel.objects.create(
            employee=employee_one, level=team_one_emp_mood
        )
        mood_level.save()
        update_team_statistic(employee_one.team, mood_level)

        team_two_emp_mood = 2
        employee_two = Employee.objects.filter(name="Test 3").first()
        mood_level = MoodLevel.objects.create(
            employee=employee_two, level=team_two_emp_mood
        )
        mood_level.save()
        update_team_statistic(employee_two.team, mood_level)

        team_stats = TeamStatistic.objects.all()

        assert len(team_stats) == 2
        assert getattr(team_stats[0], TEAM_STATS_TOTAL_FIELDS[team_one_emp_mood]) == 1
        assert getattr(team_stats[1], TEAM_STATS_TOTAL_FIELDS[team_two_emp_mood]) == 1
