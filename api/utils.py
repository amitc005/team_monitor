from api.models import TeamStatistic


def update_team_statistic(team, mood_level, old_model=None):
    team_stats = TeamStatistic.objects.filter(team=team).first()
    if not team_stats:
        team_stats = TeamStatistic(team=team)
        team_stats.save()

    old_value = old_model.level if old_model else None
    team_stats.update_stats(mood_level, old_value)
    team_stats.save()
