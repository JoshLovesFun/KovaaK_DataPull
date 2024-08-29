import requests

# Input in scenario names
SCENARIO_NAMES = [
 'Pasu Voltaic',
 'B180 Voltaic',
 'Popcorn Voltaic',
 'ww3t Voltaic',
 '1w4ts Voltaic',
 '6 Sphere Hipfire Voltaic',
 'Smoothbot Voltaic',
 'Air Angelic 4 Voltaic',
 'PGTI Voltaic',
 'FuglaaXYZ Voltaic',
 'Ground Plaza Voltaic',
 'Air Voltaic',
 'patTS Voltaic',
 'psalmTS Voltaic',
 'voxTS Voltaic',
 'kinTS Voltaic',
 'B180T Voltaic',
 'Smoothbot TS Voltaic'
]

# Array setup
Leaderboard_ID = [0] * len(SCENARIO_NAMES)

VoltsReq = [
 [68, 116.8],
 [78, 128],
 [220, 490],
 [130, 175],
 [115, 158],
 [152, 220],
 [2600, 4212],
 [2700, 4245],
 [1100, 2755],
 [11300, 17050],
 [862, 897.9],
 [850, 891.6],
 [91, 120.8],
 [85, 118.1],
 [102, 135],
 [65, 95.5],
 [64, 97],
 [50, 70.9],
]

# Request scenario path one time to get amount of pages on the scenarios page
session = requests.Session()
r = session.get("https://kovaaks.com/webapp-backend/scenario/popular?page=0&max=100").json()
Max_Page = r['total']//100

# ITERATE THROUGH ALL PLAYLIST PAGES
for i in range(Max_Page + 1):
    r = session.get(f"https://kovaaks.com/webapp-backend/scenario/popular?page={i}&max=100").json()

    # ITERATE THROUGH ALL "data" ROWS ON EACH PLAYLIST PAGE
    for Data in r['data']:

        # IF SCENARIO NAME IS FOUND FILL THE CORRESPONDING INDEX IN THE LEADERBOARD ID ARRAY WITH THE "leaderboardId"
        try:
            index = SCENARIO_NAMES.index(Data['scenarioName'])
            Leaderboard_ID[index] = Data['leaderboardId']
            # print(f"Scenario ID Found for: {SCENARIO_NAMES[index]}, {Leaderboard_ID[index]}")
        except ValueError:
            pass

    # EXIT LOOP IF ALL LEADERBOARD IDs HAVE BEEN FOUND
    if all(value != 0 for value in Leaderboard_ID):
        break
session.close()

# CREATE DICTIONARY
Score_Dic = {}

# ITERATE THROUGH EACH LEADERBOARDS
for i in range(0, len(SCENARIO_NAMES)):

    # REQUEST LEADERBOARD PATH ONE TIME TO GET AMOUNT OF PAGES ON EACH LEADERBOARD
    session = requests.Session()
    r = session.get(f"https://kovaaks.com/webapp-backend/leaderboard/scores/global?leaderboardId={Leaderboard_ID[i]}&page=0&max=100").json()
    #Max_Page = r['total']//100
    Max_Page = 50
    # ITERATE THROUGH ALL LEADERBOARD PAGES
    for ii in range(Max_Page + 1):
        r = session.get(f"https://kovaaks.com/webapp-backend/leaderboard/scores/global?leaderboardId={Leaderboard_ID[i]}&page={ii}&max=100").json()
        #print(f"Leaderboard {i + 1} of {len(SCENARIO_NAMES)}. Page: {ii} of {Max_Page} data pull.")

        # ITERATE THROUGH ALL "data" ROWS ON EACH PLAYLIST PAGE AND SEND DATA TO LEADERBOARD COLUMN OF RELEVANT ARRAYS
        for Data in r['data']:
            try:
                Steam_Name = Data['steamAccountName']

                # IF STEAM NAME (KEY) EXISTS FILL IN RELEVANT SCORE LIST
                if Steam_Name in Score_Dic and Score_Dic[Steam_Name][i] is None:
                    Score = Data['score']
                    Volts = min(max(Score-VoltsReq[i][0], 0)/max(VoltsReq[i][1]-VoltsReq[i][0], 1) * 100, 100)
                    Score_Dic[Steam_Name][i] = Score
                    Score_Dic[Steam_Name][18] = Volts + Score_Dic[Steam_Name][18]

                # IF STEAM NAME (KEY) DOES NOT EXIST, CREATE NEW KEY FOR STEAM NAME AND FILL IN RELEVANT SCORE LIST
                elif Steam_Name not in Score_Dic:
                    Score_Dic[Steam_Name] = [None]*(len(SCENARIO_NAMES)+3)
                    Score = Data['score']
                    Volts = min(max(Score-VoltsReq[i][0], 0)/max(VoltsReq[i][1]-VoltsReq[i][0], 1) * 100, 100)
                    Score_Dic[Steam_Name][i] = Score
                    Score_Dic[Steam_Name][18] = Volts
            except KeyError:
                pass
    session.close()

# SORT DICTIONARY
Score_Dic_S = dict(sorted(Score_Dic.items(), key=lambda item: item[1][18], reverse=True))

# BRING IN RANK DATA ARRAY
RankReq = [
 [68, 76, 85, 95, 105, 110.2],
 [78, 88, 98, 108, 115, 123],
 [220, 260, 320, 390, 440, 450],
 [130, 138, 148, 160, 170, 172],
 [115, 120, 130, 142, 152, 156],
 [152, 160, 175, 192, 210, 213],
 [2600, 2900, 3400, 3800, 4000, 4134],
 [2700, 3000, 3400, 3900, 4100, 4226],
 [1100, 1400, 1800, 2200, 2500, 2588],
 [11300, 12500, 13800, 15200, 16000, 16840],
 [862, 870, 880, 888, 894, 896],
 [850, 860, 872, 883, 887, 890.7],
 [91, 97, 103, 110, 116, 118.2],
 [85, 90, 98, 107, 114, 117.5],
 [102, 110, 118, 125, 131, 133],
 [65, 72, 79, 84, 88, 91],
 [64, 70, 78, 85, 92, 95.8],
 [50, 55, 60, 65, 70, 70.4],
]

# CALCULATE RANK
RankC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for key, values in Score_Dic_S.items():
    C = 0
    A = 0
    N = 0
    RankL = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # ITERATE THOUGH SCENARIOS
    for i in range(0, len(SCENARIO_NAMES)):
        try:
            if values[i] >= RankReq[i][5]:
                C = C+1
            elif values[i] >= RankReq[i][4]:
                A = A+1
            elif values[i] >= RankReq[i][3]:
                N = N+1
        except:
            pass

        # ITERATE THROUGH RANKS
        for ii in range(0, 6):
            try:
                if values[i] >= RankReq[i][ii]:
                    RankL[i] = ii
            except:
                pass

    # CALCULATE RANKS
    if min(RankL) >= 5:
        values[19] = "Celestial Complete"
        RankC[0] = RankC[0] + 1
    elif max(RankL[0:3]) >= 5 and max(RankL[3:6]) >= 5 and max(RankL[6:9]) >= 5 and max(RankL[9:12]) >= 5 and max(RankL[12:15]) >= 5 and max(RankL[15:18]) >= 5:
        values[19] = "Celestial"
        RankC[1] = RankC[1] + 1
    elif min(RankL) >= 4:
        values[19] = "Astra Complete"
        RankC[2] = RankC[2] + 1
    elif max(RankL[0:3]) >= 4 and max(RankL[3:6]) >= 4 and max(RankL[6:9]) >= 4 and max(RankL[9:12]) >= 4 and max(RankL[12:15]) >= 4 and max(RankL[15:18]) >= 4:
        values[19] = "Astra"
        RankC[3] = RankC[3] + 1
    elif min(RankL) >= 3:
        values[19] = "Nova Complete"
        RankC[4] = RankC[4] + 1
    elif max(RankL[0:3]) >= 3 and max(RankL[3:6]) >= 3 and max(RankL[6:9]) >= 3 and max(RankL[9:12]) >= 3 and max(RankL[12:15]) >= 3 and max(RankL[15:18]) >= 3:
        values[19] = "Nova"
        RankC[5] = RankC[5] + 1
    elif min(RankL) >= 2:
        values[19] = "Grandmaster Complete"
        RankC[6] = RankC[6] + 1
    elif max(RankL[0:3]) >= 2 and max(RankL[3:6]) >= 2 and max(RankL[6:9]) >= 2 and max(RankL[9:12]) >= 2 and max(RankL[12:15]) >= 2 and max(RankL[15:18]) >= 2:
        values[19] = "Grandmaster"
        RankC[7] = RankC[7] + 1
    elif min(RankL) >= 1:
        values[19] = "Master Complete"
        RankC[8] = RankC[8] + 1
    elif max(RankL[0:3]) >= 1 and max(RankL[3:6]) >= 1 and max(RankL[6:9]) >= 1 and max(RankL[9:12]) >= 1 and max(RankL[12:15]) >= 1 and max(RankL[15:18]) >= 1:
        values[19] = "Master"
        RankC[9] = RankC[9] + 1
    elif min(RankL) >= 0:
        values[19] = "Jade Complete"
        RankC[10] = RankC[10] + 1
    elif max(RankL[0:3]) >= 0 and max(RankL[3:6]) >= 0 and max(RankL[6:9]) >= 0 and max(RankL[9:12]) >= 0 and max(RankL[12:15]) >= 0 and max(RankL[15:18]) >= 0:
        values[19] = "Jade"
        RankC[11] = RankC[11] + 1
    else:
        values[19] = "No Ranked"

    # SEND HIGH SCORES TO DICTIONARY
    if C > 0:
        V1 = f"Celestial: {C}; "
    else:
        V1 = ""
    if A > 0:
        V2 = f"Astra: {A}; "
    else:
        V2 = ""
    if N > 0:
        V3 = f"Nova: {N}; "
    else:
        V3 = ""
    values[20] = V1 + V2 + V3

# RANK COUNT
print(f"Celestial Complete #:   {RankC[0]}")
print(f"Celestial #:            {RankC[1]}")
print(f"Astra Complete #:       {RankC[2]}")
print(f"Astra #:                {RankC[3]}")
print(f"Nova Complete #:        {RankC[4]}")
print(f"Nova #:                 {RankC[5]}")
print(f"Grandmaster Complete #: {RankC[6]}")
print(f"Grandmaster #:          {RankC[7]}")
print(f"Master Complete #:      {RankC[8]}")
print(f"Master #:               {RankC[9]}")
print(f"Jade Complete #:        {RankC[10]}")
print(f"Jade #:                 {RankC[11]}")
print(f"")

# RAW PRINT DATA CUT ANYTHING BELOW 100 VOLTS
print(f" {'#':<5} {'Name':<30} {'Volts':<10} {'Rank':<20} {'Score #'}")
index = 1
for key, values in Score_Dic_S.items():
    if values[18] >= 100:
        try:
            print(f" {index:<5} {key:<30} {round(values[18],2):<10} {values[19]:<20} {values[20]}")
        except:
            pass
        index = index + 1
