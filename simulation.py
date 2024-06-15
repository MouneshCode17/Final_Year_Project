import pandas as pd
import random
import pickle
import points_Calculator as pc


# Team players
players = {
    'MI': ['Rohit Sharma', 'Ishan Kishan', 'Surya Kumar Yadav','Tilak Varma','Hardik Pandya','Mohammad Nabi','Tim David','Gerald Coetzee','Piyush Chawla','Jasprit Bumrah','Dilshan Madhushanka'],
    'CSK': ['Devon Conway','Ruturaj Gaikwad','Daryl Mitchell','Ajinkya Rahane','Rachin Ravindra','Shivam Dube','MS Dhoni','Ravindra Jadeja','Shardul Thakur','Deepak Chahar','Matheesha Pathiraana'],
    'LSG':['KL Rahul','Quinton De Kock','Devdutt Padikkal','Nicolas Pooran','Krunal Pandya','Marcus Stoinis','Deepak Hooda','Shivam Mavi','Mark Wood','Ravi Bishnoi','Mohsin Khan'],
    'GT':['Shubman Gill','Wriddhiman Saha','Sai Sudharshan','Vijay Shankar','David Miller','Azmatullah Omarzai','Shahrukh Khan','Rashid Khan','Mohammed Shami','Umesh Yadav','Noor Ahmad'],
    'DC' : ['Rishab Pant','Prithvi Shaw','David Warner','Mitchell Marsh','Harry Brook','Axar Patel','Lalit Yadav','Kuldeep Yadav','Mukesh Kumar','Anrich Nortej','Khaleel Ahmed'],
    'RCB':['Faf duplessis','Virat Kohli','Rajat Patidar','Glenn Maxwell','Cameron Green','Dinesh Karthik','Mahipal Lomror','Mohhamed siraj','Karan Sharma','Akash Deep','Alzarri Joseph'],
    'RR': ["Yashasvi Jaiswal", "Jos Buttler", "Sanju Samson", "Riyan Parag", "Shimron Hetmyer", "Dhruv Jurel", "Ravichandran Ashwin", "Sandeep Sharma", "Avesh Khan", "Trent Boult", "Yuzvendra Chahal"],
    'KKR': ["Phil Salt", "Venkatesh Iyer", "Shreyas Iyer", "Nitish Rana", "Rinku Singh", "Ramandeep Singh", "Andre Russell", "Sunil Narine", "Mitchell Starc", "Harshit Rana", "Varun Chakaravarthy"],
    'SRH':["Mayank Agarwal", "Rahul Tripathi", "Aiden Markram", "Heinrich Klaasen", "Abdul Samad", "Shahbaz Ahmed", "Marco Jansen", "Pat Cummins", "Bhuvaneshwar Kumar", "Mayank Markande", "T Natarajan"],
    'PBKS':["Shikhar Dhawan", "Jonny Bairstow", "Sam Curran", "Liam Livingstone", "Jitesh Sharma", "Sikandar Raza", "Harpreet Brar", "Harshal Patel", "Kagiso Rabada", "Rahul Chahar", "Arshdeep Singh"]

}

bowlers = {
 
    'MI':['Tilak Varma','Hardik Pandya','Mohammad Nabi','Tim David','Gerald Coetzee','Piyush Chawla','Jasprit Bumrah','Dilshan Madhushanka'],
    'CSK':['Daryl Mitchell','Rachin Ravindra','Shivam Dube','Ravindra Jadeja','Shardul Thakur','Deepak Chahar','Matheesha Pathiraana'],
    'LSG':['Krunal Pandya','Marcus Stoinis','Deepak Hooda','Shivam Mavi','Mark Wood','Ravi Bishnoi','Mohsin Khan'],
    'GT':['Vijay Shankar','Azmatullah Omarzai','Shahrukh Khan','Rashid Khan','Mohammed Shami','Umesh Yadav','Noor Ahmad'],
    'DC':['Mitchell Marsh','Axar Patel','Lalit Yadav','Kuldeep Yadav','Mukesh Kumar','Anrich Nortej','Khaleel Ahmed'],
    'RCB':['Glenn Maxwell','Cameron Green','Mohhamed siraj','Karan Sharma','Akash Deep','Alzarri Joseph'],
    'RR':["Ravichandran Ashwin", "Sandeep Sharma", "Avesh Khan", "Trent Boult", "Yuzvendra Chahal"],
    'KKR':["Andre Russell", "Sunil Narine", "Mitchell Starc", "Harshit Rana", "Varun Chakaravarthy"],
    'SRH':["Aiden Markram","Shahbaz Ahmed", "Marco Jansen", "Pat Cummins", "Bhuvaneshwar Kumar", "Mayank Markande", "T Natarajan"],
    'PBKS':[ "Sam Curran", "Liam Livingstone","Sikandar Raza", "Harpreet Brar", "Harshal Patel", "Kagiso Rabada", "Rahul Chahar", "Arshdeep Singh"]

}

# Run probabilities
run_probabilities = {'0': 0.4, '1': 0.3, '2': 0.15, '3': 0.05, '4': 0.06, '6': 0.04}

# Wicket probability
wicket_probability = 0.05

# Match parameters
total_balls = 120
num_overs = 20
num_balls_per_over = 6


# Initialize match data DataFrame
match_data = pd.DataFrame(columns=['Ball', 'Bowler', 'Batter', 'Non-Striker', 'Runs_Scored', 'Target', 'Current_Score', 'Balls_Left', 'Wickets_Left', 'CRR', 'RRR', 'isWicket', 'Batting_Team', 'Bowling_Team', 'City'])

# Initialize match variables
current_over = 0
current_balls = 0
current_score = 0
wickets_left = 10
change_strike_next_over = False  # Flag to track if strike should change in the next over
batting_team = input("Enter the batting team: ")
bowling_team = input("Enter the bowling team: ")
city = input("Enter the city: ")
target_score = int(input("Enter the target: "))
current_batsmen = [players[batting_team][0],players[batting_team][1]]
previous_bowler_index = -1


while current_over < num_overs and wickets_left > 0 and current_score < target_score:
    # Select bowler for the current over
    while True:
        current_bowler_index = random.randint(0, len(bowlers[bowling_team]) - 1)
        if current_bowler_index != previous_bowler_index:
            break
    previous_bowler_index = current_bowler_index
    
    # Simulate balls for the current over
    for ball in range(1, num_balls_per_over + 1):
        # Select random runs scored for the ball based on probabilities
        runs_scored = random.choices(list(run_probabilities.keys()), weights=list(run_probabilities.values()))[0]
        
        # Update match details
        current_score += int(runs_scored)
        current_balls += 1
        
        # Check for wicket
        is_wicket = False
        if random.random() < wicket_probability:
            is_wicket = True
            wickets_left -= 1
            if wickets_left == 0:  # All out
                break
            # Replace the current striker with the next batsman who is not out
            current_batsmen[0] = next((player for player in players[batting_team][10 - wickets_left:] if player not in current_batsmen), None)
            if current_batsmen[0] is None:  # If all remaining batsmen are out, get the next one
                current_batsmen[0] = players[batting_team][10 - wickets_left]
            runs_scored = '0'  # Set runs scored to zero for wicket
        
        # Add ball details to DataFrame
        ball_data = {'Ball': current_balls,
                     'Bowler': bowlers[bowling_team][current_bowler_index],
                     'Batter': current_batsmen[0],
                     'Non-Striker': current_batsmen[1],
                     'Runs_Scored': int(runs_scored),
                     'Target': target_score,
                     'Current_Score': current_score,
                     'Balls_Left': total_balls - current_balls,
                     'Wickets_Left': wickets_left,
                     'CRR': current_score / (current_balls / 6) if current_balls > 0 else 0,
                     'RRR': ((target_score - current_score) * 6) / (total_balls - current_balls) if current_balls > 0 and total_balls - current_balls > 0 else 0,
                     'Batting_Team': batting_team,
                     'Bowling_Team': bowling_team,
                     'City': city}
        match_data = pd.concat([match_data, pd.DataFrame([ball_data])], ignore_index=True)
    
    # Check if the runs scored on the last ball of the over are even
    if int(runs_scored) % 2 == 0:
        change_strike_next_over = True
    
    # Change strike for the next over if required
    if change_strike_next_over:
        current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        change_strike_next_over = False
    
    current_over += 1

# Decide the winner based on the desired winning team
if (current_score >= target_score):
    print(f"{batting_team} wins!")
else:
    print(f"{batting_team} loses!")

# Convert 'Ball' column to over number
match_data['Over'] = (match_data['Ball'] - 1) // 6 + 1

# Define a custom aggregation function to get the last value
def last_value(series):
    return series.iloc[-1]

# Calculate runs left
match_data['Runs_Left'] = match_data['Target'] - match_data['Current_Score']

# Convert 'Ball' column to over number
match_data['Over'] = (match_data['Ball'] - 1) // 6 + 1

# Define a custom aggregation function to get the last value
def last_value(series):
    return series.iloc[-1]

# Group the DataFrame by 'Over' and aggregate the data
over_data = match_data.groupby('Over').agg({'Batting_Team': 'first',
                                             'Bowling_Team': 'first',
                                             'City': 'first',
                                             'Runs_Left': 'last',
                                             'Balls_Left': 'last',
                                             'Wickets_Left': 'first',
                                             'Target': 'first',
                                             'CRR': 'last',
                                             'RRR': 'last',
                                             'Batter': last_value,
                                             'Non-Striker': last_value,
                                             'Bowler': last_value,
                                             'Runs_Scored': 'sum'
                                             })

# Reset index to make 'Over' a column again
over_data.reset_index(inplace=True)

# Display the aggregated over data

# Save aggregated over data to CSV

pipe = pickle.load(open('D:\Simulation_Match\Project _Final\pipeProject.pkl', 'rb'))

# Iterate through every row in the DataFrame
for index, row in over_data.iterrows():
    # Extract data from the row
    batter = row['Batter']
    bowler = row['Bowler']
    nonstriker = row['Non-Striker']
    batting_team = row['Batting_Team']
    bowling_team = row['Bowling_Team']
    city = row['City']
    runs_left = row['Runs_Left']
    balls_left = row['Balls_Left']
    wickets = row['Wickets_Left']
    target = row['Target']
    crr = row['CRR']
    rrr = row['RRR']
    score = target - runs_left
    # Create input DataFrame for the model
    input_df = pd.DataFrame({
        'BattingTeam': [batting_team],
        'BowlingTeam': [bowling_team],
        'City': [city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets],
        'total_run_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    # Use the model to predict probabilities
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    # Initial win and loss probabilities
    initial_win_prob = win
    initial_loss_prob = loss
    adjusted_win_prob = win
    adjusted_loss_prob = loss

    maxVal = 0

    batting_points = pc.get_player_bat_points(batter)
    bowling_points = pc.get_player_bowl_points(bowler)
    nonstriker_points = pc.get_player_bat_points(nonstriker)
    
    maxVal = max(batting_points, bowling_points)
   


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

    if runs_left<=0:
        over_data.at[index, 'Win_Probability'] = round(1*100)
        over_data.at[index, 'Loss_Probability'] = round(0*100)
    elif wickets == 0 or balls_left==0:
        over_data.at[index, 'Win_Probability'] = round(0*100)
        over_data.at[index, 'Loss_Probability'] = round(1*100)
    else:
        over_data.at[index, 'Win_Probability'] = round(adjusted_win_prob*100)
        over_data.at[index, 'Loss_Probability'] = round(adjusted_loss_prob*100)
        
over_data.to_csv('overs_final.csv', index=False)
match_data.to_csv('new.csv',index=False)
