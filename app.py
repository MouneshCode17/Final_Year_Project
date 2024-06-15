from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import points_Calculator as pc
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.form.to_dict()
        pipe = pickle.load(open('pipeProject.pkl', 'rb'))
        print("Received data:", data)

        batting_team = data.get("teams_bat")
        bowling_team = data.get("teams_bowl")
        target = int(data.get("target"))
        score = int(data.get("score"))
        overs = int(data.get("overs"))
        selected_city = data.get("venue")
        wickets = int(data.get("wickets"))
        batter = data.get("instrike_batsman")
        nonstriker= data.get("nonstrike_batsman")
        bowler = data.get("instrike_bowler")
        partnership = int(data.get("ship"))

        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({'BattingTeam': [batting_team], 'BowlingTeam': [bowling_team], 'City': [selected_city],
                                 'runs_left': [runs_left], 'current_score':[score],'balls_left': [balls_left], 'wickets': [wickets],
                                 'total_run_x': [target], 'crr': [crr], 'rrr': [rrr]})


        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        # Initial win and loss probabilities
        initial_win_prob = win
        initial_loss_prob = loss

        # Batting points and bowling points

        batting_points = pc.get_player_bat_points(batter)
        bowling_points = pc.get_player_bowl_points(bowler)
        nonstriker_points = pc.get_player_bat_points(nonstriker)
        maxVal = max(batting_points,nonstriker_points)
        print(maxVal)

        points_difference = maxVal - bowling_points

        max_change_limit = 5


        if abs(points_difference) > max_change_limit:
            points_difference = max_change_limit if points_difference > 0 else -max_change_limit

        if points_difference > 0:
            adjustment_factor = points_difference / 100
            adjusted_win_prob = min(0.95, initial_win_prob + adjustment_factor)
            adjusted_loss_prob = max(0.05,initial_loss_prob - adjustment_factor)
        elif points_difference < 0:
            adjustment_factor = abs(points_difference) / 100
            adjusted_win_prob = max(0.05,initial_win_prob - adjustment_factor)
            adjusted_loss_prob = min(0.95,initial_loss_prob + adjustment_factor)
        else:
            adjusted_win_prob = initial_win_prob
            adjusted_loss_prob = initial_loss_prob

        # print("Initial Win Probability from Model:", round(initial_win_prob*100),"%")
        # print("Initial Loss Probability from Model:", round(initial_loss_prob*100),"%")
        # # print("Batting Points:", batting_points)
        # # print("Bowling Points:", bowling_points)
        # # print("Points Difference:", points_difference)
        # print("Points Win Probability:", round(adjusted_win_prob*100),"%")
        # print("Points Loss Probability:", round(adjusted_loss_prob*100),"%")

        partnership_percentage = partnership
        updated_win_probability, updated_loss_probability = pc.update_probabilities(adjusted_win_prob, adjusted_loss_prob,
                                                                                 batting_points,
                                                                                 partnership_percentage)

        if (round(wickets) == 0):
            win = 0
            loss = 100
            print('Win Probability:',win,'%')
            print('Loss Probability',loss,'%')
        elif (target <= score):
            win = 100
            loss = 0
            print('Win Probability:', win,'%')
            print('Loss Probability', loss,'%')
        else:
            print(f"Win Probability: {round(updated_win_probability * 100)}%")
            print(f"Loss Probability: {round(updated_loss_probability * 100)}%")

        return jsonify({'message': 'Data received successfully', 'win_probability': win, 'loss_probability': loss})
    except Exception as e:

        print("Error:", e)
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    app.run(debug=True)
