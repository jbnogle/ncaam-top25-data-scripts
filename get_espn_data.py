import urllib.request, json, pandas, os

# Final Schema Reference (can calculate additional cols like win pct, point differential from these)
# Location|Team Name|Color|Ranking|Wins|Losses|Points For|Points Against|Avg Points For|Avg Points Against|Conference|Logo URL

########### PHASE ONE: Get ESPN Ranking and Record Statistics (Top 25 Teams), parse into Pandas DF ###########
rankings_response = json.loads(urllib.request.urlopen("https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/rankings").read())
rankings_list = rankings_response["rankings"][0]["ranks"]

# container for rows (arrays) of data to be converted to csv
final_arr = []
# append first row (array) of column names, in order of schema
final_arr.append(["Location","Team Name","Color","Ranking","Wins","Losses","Points For","Points Against","Avg Points For","Avg Points Against", "Conference", "Logo URL"])

for ranking in rankings_list:
    # array representing single row of data, array objects will be ordered according to schema
    row_arr = []

    # object (dictionary) representing current team in the rankings_list iteration
    curr_team = ranking["team"]
    curr_team_id = curr_team["id"]

    # Add data values from rankings API response, in order of schema
    row_arr.extend([curr_team["location"], curr_team["name"], curr_team["color"], ranking["current"]])

    # Make subsequent API call to get data on this specific team's record
    team_response = json.loads(urllib.request.urlopen(f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{curr_team_id}").read())
    team_record = team_response["team"]["record"]["items"][0]["stats"] # items[0] is the array object representing overall record
    team_conference = team_response["team"]["standingSummary"].split("in", 1)[1].strip()
    team_logo_url = team_response["team"]["logos"][0]["href"]

    for stat in team_record:
        match stat["name"]:
            case "wins":
                wins = stat["value"]
            case "losses":
                losses = stat["value"]
            case "pointsFor":
                points_for = stat["value"]
            case "pointsAgainst":
                points_against = stat["value"]
            case "avgPointsFor":
                avg_points_for = stat["value"]
            case "avgPointsAgainst":
                avg_points_against = stat["value"]
    
    row_arr.extend(
        [wins, losses, points_for, points_against, avg_points_for, avg_points_against, team_conference, team_logo_url]
    )

    final_arr.append(row_arr)

df = pandas.DataFrame(final_arr)
headers = df.iloc[0]
new_df  = pandas.DataFrame(df.values[1:], columns=headers)
#new_df['Color'] = new_df['Color'].apply('="{}"'.format)  # preserves leading 0s in 'Color' column (hex code) when opening in Excel

if os.path.isfile('espn_data.csv'):
    os.remove('espn_data.csv')

new_df.to_csv('espn_data.csv', index=False, header=True)

