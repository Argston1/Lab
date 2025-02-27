from flask import Flask, jsonify, request
from crud import add_team, add_match, get_all_teams, get_matches_by_team, delete_team, delete_match, get_team_by_id

app = Flask(__name__)

# Главная страница API
@app.route('/')
def home():
    return jsonify({"message": "Добро пожаловать в API управления футбольными командами и матчами!"})

# Получение списка всех команд
@app.route('/teams', methods=['GET'])
def list_teams():
    teams = get_all_teams()
    return jsonify([{"TeamId": team.TeamId, "Name": team.Name} for team in teams])

# Получение информации о конкретной команде
@app.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = get_team_by_id(team_id)
    if team:
        return jsonify({"TeamId": team.TeamId, "Name": team.Name})
    return jsonify({"error": "Команда не найдена"}), 404

# Добавление новой команды
@app.route('/teams', methods=['POST'])
def create_team():
    data = request.json
    if 'name' in data and 'division_id' in data:
        team_id = add_team(data['name'], data['division_id'])
        return jsonify({"message": "Команда добавлена!", "TeamId": team_id})
    return jsonify({"error": "Необходимо указать название команды и ID дивизиона"}), 400

# Удаление команды
@app.route('/teams/<int:team_id>', methods=['DELETE'])
def remove_team(team_id):
    delete_team(team_id)
    return jsonify({"message": f"Команда с ID {team_id} удалена."})

# Получение списка всех матчей
@app.route('/matches', methods=['GET'])
def list_all_matches():
    matches = get_matches_by_team(None)  # Получить все матчи
    return jsonify([
        {
            "MatchId": m.MatchId,
            "HomeTeamId": m.HomeTeamId,
            "AwayTeamId": m.AwayTeamId,
            "HomeScore": m.HomeScore,
            "AwayScore": m.AwayScore
        } for m in matches
    ])

# Получение списка матчей для конкретной команды
@app.route('/matches/<int:team_id>', methods=['GET'])
def list_matches_for_team(team_id):
    matches = get_matches_by_team(team_id)
    return jsonify([
        {
            "MatchId": m.MatchId,
            "HomeTeamId": m.HomeTeamId,
            "AwayTeamId": m.AwayTeamId,
            "HomeScore": m.HomeScore,
            "AwayScore": m.AwayScore
        } for m in matches
    ])

# Добавление нового матча
@app.route('/matches', methods=['POST'])
def create_match():
    data = request.json
    if all(k in data for k in ('home_team_id', 'away_team_id', 'home_score', 'away_score')):
        match_id = add_match(data['home_team_id'], data['away_team_id'], None, data['home_score'], data['away_score'])
        return jsonify({"message": "Матч добавлен!", "MatchId": match_id})
    return jsonify({"error": "Необходимо указать ID команд и счет"}), 400

# Удаление матча
@app.route('/matches/<int:match_id>', methods=['DELETE'])
def remove_match(match_id):
    delete_match(match_id)
    return jsonify({"message": f"Матч с ID {match_id} удален."})

if __name__ == '__main__':
    app.run(debug=True)
