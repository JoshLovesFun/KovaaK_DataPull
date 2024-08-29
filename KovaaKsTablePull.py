import requests
import csv

# Input in scenario names
SCENARIO_NAMES = [
    '1wall 6targets small',
    '1w4ts Voltaic',
    '1w4ts reload',
]
CSV_File_Name = 'Test_X'

# Array setup
Leaderboard_ID = [0] * len(SCENARIO_NAMES)

# Request scenario path one time to get amount of pages on the scenarios page
session = requests.Session()
r = session.get(
    "https://kovaaks.com/webapp-backend/scenario/popular"
    "?page=0&max=100"
).json()
Max_Page = r['total'] // 100

# Iterate through all playlist pages
for i in range(Max_Page + 1):
    r = session.get(
        f"https://kovaaks.com/webapp-backend/scenario/popular"
        f"?page={i}&max=100"
    ).json()

    # Iterate through all "data" rows on each playlist page
    for Data in r['data']:

        # If scenario name is found, fill the corresponding index in the
        # leaderboard ID array with the "leaderboardId"
        try:
            index = SCENARIO_NAMES.index(Data['scenarioName'])
            Leaderboard_ID[index] = Data['leaderboardId']
            print(
                f"Scenario ID Found for: {SCENARIO_NAMES[index]}, "
                f"{Leaderboard_ID[index]}"
            )
        except ValueError:
            pass

    # Exit loop if all leaderboard IDs have been found
    if all(value != 0 for value in Leaderboard_ID):
        break
session.close()

# Create dictionary
Score_Dic = {}

# Iterate through each leaderboard
for i in range(0, len(SCENARIO_NAMES)):

    # Request leaderboard path one time to get amount of pages
    # on each leaderboard
    session = requests.Session()
    r = session.get(
        f"https://kovaaks.com/webapp-backend/leaderboard/scores/global?"
        f"leaderboardId={Leaderboard_ID[i]}&page=0&max=100"
    ).json()
    Max_Page = r['total'] // 100

    # Iterate through all leaderboard pages
    for ii in range(Max_Page + 1):
        r = session.get(
            f"https://kovaaks.com/webapp-backend/leaderboard/scores/global?"
            f"leaderboardId={Leaderboard_ID[i]}&page={ii}&max=100"
        ).json()
        print(
            f"Leaderboard {i + 1} of {len(SCENARIO_NAMES)}. "
            f"Page: {ii} of {Max_Page} data pull."
        )

        # Iterate through all "data" rows on each playlist page
        # and send data to leaderboard column of relevant arrays
        for Data in r['data']:
            try:
                Steam_Name = Data['steamAccountName']

                # If Steam name (key) exists, fill in relevant score list
                # for Steam name
                if Steam_Name in Score_Dic and Score_Dic[Steam_Name][
                        i] is None:
                    Score_Dic[Steam_Name][i] = Data['score']

                # If Steam name (key) does not exist, create new key for
                # Steam name and fill in relevant score list for Steam name
                elif Steam_Name not in Score_Dic:
                    Score_Dic[Steam_Name] = [None] * len(SCENARIO_NAMES)
                    Score_Dic[Steam_Name][i] = Data['score']
            except KeyError:
                pass
    session.close()

# CSV data writing
with open('Leaderboard_Pull_For_' + CSV_File_Name + '.csv', 'w',
          encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write in a header row
    Header = ["Steam Name"] + [
        SCENARIO_NAMES[i] for i in range(len(SCENARIO_NAMES))
    ]
    csvwriter.writerow(Header)
    for key, value in Score_Dic.items():
        try:  # Sometimes Excel writes errors here, so do this:
            csvwriter.writerow([key] + value)
        except:  # I don't know the error, so just do this for now
            pass
