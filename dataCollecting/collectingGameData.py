import time
import pickle
import collect as co
import _mysql
import sys
import MySQLdb as mdb
from privateData import sqlpwd

# listKnown = input('Use gameids stored in data/gameIDs.txt: (True/False):')

# # Get list of Steam game IDs if known or all app IDs if not
# if listKnown:
#     f = open('gameIDs.txt', 'r')  # Load in list of Steam game IDs
#     for line in f:
#         gameids.append(int(line))    
# else:
#     gameids = getGameIDs()

# n = len(gameids)

gameids = []
f = open('/home/midge/lookingForPlayers/data/gameIDs.txt', 'r')  # Load in list of Steam game IDs
for line in f:
    gameids.append(int(line))    

n = len(gameids)    

# Initialize Game Dictionary 
gameDict = {}

# Loop through game IDs and collect data 
j = 0
while j < n:
    time.sleep(-time.time()%2) 
    gameDict = co.getGameData(gameDict,gameids[j])
    j += 1
    if j % 100 == 0:
		print 'j = ' + str(j)
		with open('/home/midge/lookingForPlayers/data/unfinished_gameDict_' + str(j), 'wb') as f:
			pickle.dump(gameDict, f)

# Pickle original game format 
with open('/home/midge/lookingForPlayers/data/gameDict', 'wb') as f:
	pickle.dump(gameDict, f)

# Convert dictionary to a dataframe 
df = DataFrame(gameDict); df = df.T

# Convert video game titles to ascii
df['name'] = df['name'].map(lambda x: x.encode('ascii','ignore'))
df['publishers'] = df['publishers'].map(co.changeEncoding)
df['developers'] = df['developers'].map(co.changeEncoding)

# Save data into SQL
con = mdb.connect('localhost', 'root', sqlpwd, 'lfp');
df.to_sql(con=con,name='gamedata',if_exists='replace',flavor='mysql')
con.close()
