"""
Function for collecting and organizing user data given a list of user ids 
"""
import pickle
import collect as co
from privateData import sqlpwd, pdir
from pandas import DataFrame  
from __future__ import division  
import sys
import MySQLdb as mdb

# Start with list of 50,000 user ids 
with open(pdir + 'data/userList50', 'rb') as f:
    userIDList = pickle.load(f)

nUsers = len(userIDList)

# Create two dictionaries, one for user information and the other for their games and playtime
j = 0
userGamesDict = {}
userDict = {}
while j < nUsers:
    steamid = str(userIDList[j])

    # Collect data about each player's games
    userGamesDict = co.getOwnedGames(steamid,userGamesDict) 

    # If the user qualified for the database (i.e. had enough playtime) then get their player data 
    if steamid in userGamesDict.keys(): 

        # Collect data about each player that had enough games to qualify
        userDict = co.getUserDetails(steamid,userDict)      

        # Determine the user's total playtime and maximum game preference 
        totalTime = sum([v[0] for item,v in userGamesDict[steamid].items()])
        userDict[steamid].update({'total_playtime': totalTime})
        userDict[steamid].update({'max_preference': max([v[0]/totalTime for item,v in userGamesDict[steamid].items()])*100})
    j += 1

# Pickle original dictionaries 
with open(pdir + 'data/userGamesDict', 'wb') as f: 
    pickle.dump(userGamesDict, f)
with open(pdir + 'data/userDict', 'wb') as f: 
    pickle.dump(userDict, f)

# Flatten users-game dictionary and store in MySQL
flatUserGames = DataFrame(list(co.flatten_dict(userGamesDict)))
flatUserGames.columns = ['user_id','game_id','playtime','playtime_2weeks']
con = mdb.connect('localhost', 'root', sqlpwd, 'lfp'); 
flatUserGames.to_sql(con=con,name='usersGameData',if_exists='replace',flavor='mysql')
con.close()

# Convert user dictionary to a dataframe and store in MySQL
userdf = DataFrame(userDict); userdf = userdf.T
con = mdb.connect('localhost', 'root', sqlpwd, 'lfp');
userdf.to_sql(con=con,name='userData',if_exists='replace',flavor='mysql')
con.close()