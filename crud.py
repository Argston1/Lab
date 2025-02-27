from sqlalchemy.orm import sessionmaker
from orm import setup_database, create_session, Team, Division, Match
from datetime import datetime

# Инициализация базы данных
engine = setup_database("sqlite:///sports_league.sqlite")
session = create_session(engine)

# CREATE (Создание)
def add_team(name, division_id):
    new_team = Team(Name=name, DivisionId=division_id)
    session.add(new_team)
    session.commit()
    print(f"Team '{name}' added with ID: {new_team.TeamId}")
    return new_team.TeamId

def add_division(name):
    new_division = Division(Name=name)
    session.add(new_division)
    session.commit()
    print(f"Division '{name}' added with ID: {new_division.DivisionId}")
    return new_division.DivisionId

def add_match(home_team_id, away_team_id, date, home_score, away_score):
    new_match = Match(
        HomeTeamId=home_team_id,
        AwayTeamId=away_team_id,
        Date=date,
        HomeScore=home_score,
        AwayScore=away_score
    )
    session.add(new_match)
    session.commit()
    print(f"Match added with ID: {new_match.MatchId}")
    return new_match.MatchId

# READ (Чтение)
def get_team_by_id(team_id):
    team = session.query(Team).filter_by(TeamId=team_id).first()
    if team:
        print(f"Team: {team.Name}")
        return team
    else:
        print(f"Team with ID {team_id} not found.")
        return None

def get_all_teams():
    teams = session.query(Team).all()
    for team in teams:
        print(f"Team ID: {team.TeamId}, Name: {team.Name}")
    return teams

def get_matches_by_team(team_id):
    matches = session.query(Match).filter((Match.HomeTeamId == team_id) | (Match.AwayTeamId == team_id)).all()
    print(f"Matches for Team ID {team_id}:")
    for match in matches:
        print(f"- Match {match.MatchId}: {match.HomeScore} - {match.AwayScore}")
    return matches

# UPDATE (Обновление)
def update_team_name(team_id, new_name):
    team = session.query(Team).filter_by(TeamId=team_id).first()
    if team:
        team.Name = new_name
        session.commit()
        print(f"Team ID {team_id} updated to '{new_name}'")
        return team
    else:
        print(f"Team with ID {team_id} not found.")
        return None

def update_match_score(match_id, home_score, away_score):
    match = session.query(Match).filter_by(MatchId=match_id).first()
    if match:
        match.HomeScore = home_score
        match.AwayScore = away_score
        session.commit()
        print(f"Match ID {match_id} score updated to {home_score} - {away_score}")
        return match
    else:
        print(f"Match with ID {match_id} not found.")
        return None

# DELETE (Удаление)
def delete_team(team_id):
    team = session.query(Team).filter_by(TeamId=team_id).first()
    if team:
        session.delete(team)
        session.commit()
        print(f"Team ID {team_id} deleted.")
    else:
        print(f"Team with ID {team_id} not found.")

def delete_match(match_id):
    match = session.query(Match).filter_by(MatchId=match_id).first()
    if match:
        session.delete(match)
        session.commit()
        print(f"Match ID {match_id} deleted.")
    else:
        print(f"Match with ID {match_id} not found.")

# Примеры использования
if __name__ == "__main__":
    print("\n=== Создание данных ===")
    division_id = add_division("Premier League")
    team1_id = add_team("Team A", division_id)
    team2_id = add_team("Team B", division_id)
    match_id = add_match(team1_id, team2_id, datetime.now(), 2, 1)

    print("\n=== Чтение данных ===")
    get_team_by_id(team1_id)
    get_all_teams()
    get_matches_by_team(team1_id)

    print("\n=== Обновление данных ===")
    update_team_name(team1_id, "Updated Team A")
    update_match_score(match_id, 3, 2)

    print("\n=== Удаление данных ===")
    delete_match(match_id)
    delete_team(team1_id)
    delete_team(team2_id)