import tkinter as tk
from tkinter import messagebox
from crud import add_team, add_match, get_all_teams, get_matches_by_team, delete_team, delete_match

def create_team():
    name = team_name_entry.get()
    division_id = division_id_entry.get()
    if name and division_id:
        try:
            team_id = add_team(name, int(division_id))
            messagebox.showinfo("Успех", f"Команда '{name}' добавлена с ID {team_id}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showwarning("Внимание", "Заполните все поля!")

def create_match():
    home_team_id = home_team_entry.get()
    away_team_id = away_team_entry.get()
    home_score = home_score_entry.get()
    away_score = away_score_entry.get()
    if home_team_id and away_team_id and home_score and away_score:
        try:
            match_id = add_match(int(home_team_id), int(away_team_id), None, int(home_score), int(away_score))
            messagebox.showinfo("Успех", f"Матч добавлен с ID {match_id}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showwarning("Внимание", "Заполните все поля!")

def list_teams():
    teams = get_all_teams()
    team_list.delete(0, tk.END)
    for team in teams:
        team_list.insert(tk.END, f"ID {team.TeamId}: {team.Name}")

def remove_team():
    selected = team_list.curselection()
    if selected:
        team_id = team_list.get(selected[0]).split(': ', 1)[0].replace('ID ', '').strip()
        delete_team(int(team_id))
        list_teams()
        messagebox.showinfo("Успех", f"Команда с ID {team_id} удалена.")
    else:
        messagebox.showwarning("Внимание", "Выберите команду для удаления!")

def remove_match():
    match_id = match_id_entry.get()
    if match_id:
        try:
            delete_match(int(match_id))
            messagebox.showinfo("Успех", f"Матч с ID {match_id} удален.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showwarning("Внимание", "Введите ID матча!")

def view_match_results():
    team_id = team_id_entry.get()
    if team_id:
        try:
            matches = get_matches_by_team(int(team_id))
            result_text = "\n".join([
                f"Матч {m.MatchId}: {m.HomeTeamId} ({m.HomeScore}) - ({m.AwayScore}) {m.AwayTeamId}"
                for m in matches
            ])
            messagebox.showinfo("Результаты матчей", result_text if result_text else "Нет матчей для данной команды.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showwarning("Внимание", "Введите ID команды!")

root = tk.Tk()
root.title("Управление командами и матчами")
root.geometry("420x650")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#d9d9d9", padx=10, pady=10)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Раздел: Добавление команды
tk.Label(frame, text="Название команды:", bg="#d9d9d9").pack(fill=tk.X)
team_name_entry = tk.Entry(frame)
team_name_entry.pack(fill=tk.X)

tk.Label(frame, text="ID дивизиона:", bg="#d9d9d9").pack(fill=tk.X)
division_id_entry = tk.Entry(frame)
division_id_entry.pack(fill=tk.X)

tk.Button(frame, text="Добавить команду", command=create_team, bg="#4caf50", fg="white").pack(pady=5, fill=tk.X)
tk.Button(frame, text="Обновить список", command=list_teams, bg="#2196f3", fg="white").pack(fill=tk.X)

team_list = tk.Listbox(frame, bg="white", height=7)
team_list.pack(pady=5, fill=tk.BOTH, expand=True)

tk.Button(frame, text="Удалить команду", command=remove_team, bg="#f44336", fg="white").pack(fill=tk.X)

# Раздел: Добавление матча
tk.Label(frame, text="ID домашней команды:", bg="#d9d9d9").pack(fill=tk.X)
home_team_entry = tk.Entry(frame)
home_team_entry.pack(fill=tk.X)

tk.Label(frame, text="ID гостевой команды:", bg="#d9d9d9").pack(fill=tk.X)
away_team_entry = tk.Entry(frame)
away_team_entry.pack(fill=tk.X)

tk.Label(frame, text="Счет домашней команды:", bg="#d9d9d9").pack(fill=tk.X)
home_score_entry = tk.Entry(frame)
home_score_entry.pack(fill=tk.X)

tk.Label(frame, text="Счет гостевой команды:", bg="#d9d9d9").pack(fill=tk.X)
away_score_entry = tk.Entry(frame)
away_score_entry.pack(fill=tk.X)

tk.Button(frame, text="Добавить матч", command=create_match, bg="#ff9800", fg="white").pack(pady=5, fill=tk.X)

# Раздел: Просмотр матчей
tk.Label(frame, text="ID команды для просмотра матчей:", bg="#d9d9d9").pack(fill=tk.X)
team_id_entry = tk.Entry(frame)
team_id_entry.pack(fill=tk.X)

tk.Button(frame, text="Просмотреть результаты матчей", command=view_match_results, bg="#673ab7", fg="white").pack(pady=5, fill=tk.X)

# Раздел: Удаление матча
tk.Label(frame, text="ID матча для удаления:", bg="#d9d9d9").pack(fill=tk.X)
match_id_entry = tk.Entry(frame)
match_id_entry.pack(fill=tk.X)

tk.Button(frame, text="Удалить матч", command=remove_match, bg="#e91e63", fg="white").pack(pady=5, fill=tk.X)

root.mainloop()