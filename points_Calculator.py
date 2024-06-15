import pandas as pd


df = pd.read_csv('static//IPL_Player_Stats.csv')
# print(df.describe())


def calculate_points(row):

    batting_points = (row['batting_avg'] / 20) + (row['batting_strike_rate'] / 20)
    if row['bowling_economy'] == 0 and row['bowling_avg'] == 0 and row['bowling_strike_rate'] == 0:
        bowling_points = 0
    else:
        bowling_points = (10 - (row['bowling_economy'] / 1.0)) + (10 - (row['bowling_avg'] / 5.0)) + (row['bowling_strike_rate'] / 10)
    return min(max(round(batting_points), 1), 10), min(max(round(bowling_points), 1), 10)



df[['batting_points', 'bowling_points']] = df.apply(calculate_points, axis=1, result_type='expand')

print(df)
df.to_csv('points.csv',index=False)

def get_player_bat_points(player_name):
    player_row = df[df['player'] == player_name]
    if not player_row.empty:
        batting_points = player_row['batting_points'].iloc[0]
        return batting_points
    else:
        return None

def get_player_bowl_points(player_name):
    player_row = df[df['player'] == player_name]
    if not player_row.empty:
        bowling_points = player_row['bowling_points'].iloc[0]
        return bowling_points
    else:
        return None

def update_probabilities(win_probability, loss_probability, in_strike_batsman_points, partnership_percentage):

    max_change = 5
    if in_strike_batsman_points < 5:
        change_factor = min(partnership_percentage / 10, max_change)
        updated_win_probability = win_probability + (change_factor / 100)
        updated_loss_probability = max(0, loss_probability - (change_factor / 100))
    else:
        updated_win_probability = win_probability
        updated_loss_probability = loss_probability
    return updated_win_probability, updated_loss_probability

