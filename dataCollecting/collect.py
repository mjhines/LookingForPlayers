"""
Module defining all functions needed for API calls and parsing data 
"""
import urllib2
import json
from privateData import api_key
from datetime import datetime

site = 'http://api.steampowered.com/'

# Function to flatten dictionary for SQL 
def flatten_dict(d):
    for k,v in d.items():  # user dict keys 
        for kk,vv in v.items():  # game dict keys 
            yield [k] + [kk] + vv

# Function to convert a list of dictionaries to a dict of dictionaries 
def listToDict(inputList,popStr):
    outputDict = {}
    for item in inputList:
        name = item.pop(popStr)
        outputDict[name] = item
    return outputDict

# Function for acquiring player details from Steam API 
def getUserDetails(steamid,userDict): 
    try: # Is user data public? 
        playerSummary = json.load(urllib2.urlopen(site + 'ISteamUser/GetPlayerSummaries/v0002/?key=' + api_key + '&steamids=' + steamid))
    except:
        return userDict

    playerSummary = (playerSummary.pop('response')).pop('players')
    userDict.update({steamid: playerSummary[0]})

    # Get number of friends if list is available
    friends = getFriendList(steamid)
    userDict[steamid].update({'friend_cnt': len(friends)})
    return userDict

# Function for acquiring Steam user's friends list with Steam API 
def getFriendList(steamid):
    try:
        friendList = json.load(urllib2.urlopen(site + 'ISteamUser/GetFriendList/v0001/?key=' + api_key + '&steamid=' + steamid + '&relationship=friend'))
    except:
        return {}

    friendList = (friendList.pop('friendslist')).pop('friends')
    return friendList

# Function for creating a list of user IDs by crawling through friends lists
def updateUserList(steamid,userIDList):
    try:
        friends = getFriendList(steamid)
        friendIDs = friends.keys()
        userIDList.extend([int(friend) for friend in friendIDs if friend not in userIDList])
    except:
        pass
    
    return userIDList

# Function for acquiring and parsing Steam user's owned games and playtimes from Steam API  
def getOwnedGames(steamid,userGameDict):
    try:
        ownedGames = json.load(urllib2.urlopen(site + 'IPlayerService/GetOwnedGames/v0001/?key=' + api_key + '&steamid=' + steamid +'&include_played_free_games=1&format=json'))
    except:
        print 'failed'
        return userGameDict
    
    if bool(ownedGames['response']):
        if ownedGames['response']['game_count'] > 0:
            ownedGames = (ownedGames.pop('response')).pop('games')
            games = {}
            for item in ownedGames:
                name = item.pop('appid')
                if 'playtime_2weeks' in item.keys():
                    games[name] = [item['playtime_forever'],item['playtime_2weeks']]
                else:
                    games[name] = [item['playtime_forever'],0]
        else:
            games = {}
    else:
        games = {}
    
    if (len(games) > 0) & (sum([games[item][0] for item in games]) > 3000):
        userGameDict[steamid] = games
    
    return userGameDict

def getGameIDs():
    # Get list of all apps on Steam
    data = json.load(urllib2.urlopen('http://api.steampowered.com/ISteamApps/GetAppList/v0001/'))
    data = ((data.pop('applist')).pop('apps')).pop('app')
    gameids = {}
    for item in data:
        name = item.pop('appid')
        gameids[name] = item
    return gameids


# Function for acquiring and parsing Steam game data from Steam Store API  
def getGameData(gameList,appID):
    appIDs = str(appID)

    try:
        gameData = json.load(urllib2.urlopen('http://store.steampowered.com/api/appdetails/?appids=' + appIDs))
    except:
        return gameList
    
    try:    
        gameData = (gameData.pop(appIDs)).pop('data')
    except:
        return gameList

    try:
        gameList.update({appID: {'name': gameData['name']}})
    except:    
        raise gameList
    
    try:
        gameList[appID].update({'age': gameData['required_age']})
    except:
        pass

    try:
        gameList[appID].update({'is_free': gameData['is_free']})
        if gameList[appID]['is_free'] == True:
            gameList[appID].update({'original_price': 0}) 
    except:
        pass

    try:
        gameList[appID].update({'original_price': gameData['price_overview']['initial']})
    except:
        pass        

    try:
        gameList[appID].update({'developers': fixListFormat(gameData['developers'])})
    except:
        pass

    try:
        gameList[appID].update({'publishers': fixListFormat(gameData['publishers'])})
    except:
        pass

    try:
        gameList[appID].update({'release_date': datetime.strptime(gameData['release_date']['date'],'%b %d, %Y')})
    except:
        pass

    try:
        gameList[appID].update({'achievements': gameData['achievements']['total']})
    except:
        gameList[appID].update({'achievements': 0})

    try:
        gameList[appID].update({'recommendations': gameData['recommendations']['total']})
    except:
        gameList[appID].update({'recommendations': 0})

    try:
        gameList[appID].update({'genres': fixDictFormat(gameData['genres'],'description')})
    except:
        pass

    try:
        gameList[appID].update({'categories': fixDictFormat(gameData['categories'],'description')})
    except:
        pass

    try:
#        dropIDs = gameData['dlc']
        gameList[appID].update({'dlc': len(gameData['dlc'])})
    except:
        dropIDs = []
        gameList[appID].update({'dlc': 0})

    try:
        gameList[appID].update({'metacritic': gameData['metacritic']['score']})
    except:
        pass

#    for it in dropIDs:
#        try:
#            gameList.pop(it)
#        except:
#            pass

    return gameList

# fixes the categories and genres to no longer be dictionaries 
def fixFormat(inputCol,innerKey):
    j = 0
    for j in arange(0,len(inputCol)):
        if isinstance(inputCol.iloc[j],list):
            inputCol.iloc[j] = "|".join([inputCol.iloc[j][i][innerKey] for i in arange(0,len(inputCol.iloc[j]))]) 
        j += 1

def fixDictFormat(inputList,innerKey):
    return "|".join([i[innerKey] for i in inputList]) 

def fixListFormat(inputList):
    return "|".join([i for i in inputList]) 

def changeEncoding(x):
    if isinstance(x,float): 
        return x
    else: 
        return x.encode('ascii','ignore')      