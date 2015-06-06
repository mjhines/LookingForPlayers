"""
User matching functions
"""
from __future__ import division
from math import sqrt
import pickle
from dataCollecting.privateData import pdir
import dataCollecting.collect as co

def match(steamid,userGames,nMatches,userDict):

    print 'Please wait a moment while the database is loaded...'
    #with open(pdir + 'data/usersGamesDict', 'rb') as f:

    if steamid not in userGames.keys():
        print 'Updating user into database...'
        userGames = co.getOwnedGames(steamid,userGames) # Collect data about each player's games

    if steamid not in userGames.keys():
        print 'Cannot compare: User either does not have enough playtime or has profile set to private'
        return 

    print 'Calculating similarity metrics...'
    matches = getMatches(userGames,steamid,n=nMatches)

    names = []
    for person in matches:
        # print str(type(person[1]))
        user = userDict[person[3]]
        names.append({'name': user['personaname'].encode('ascii','ignore'),'percent':str(int(person[0]*100)), 'ncommonGames':str(int(person[1])),
            'url': user['profileurl'].encode('ascii','ignore'),'avatar': user['avatarfull'].encode('ascii','ignore')})

    #name = getMatchesNames(matches)
    return names

def getMatchesNames(matches):
    details = []

    # sqlcon = mdb.connect('localhost','root',sqlpwd,'lfp')
    # gameData = pd.read_sql('SELECT * FROM users WHERE steamid = ' str(person[1]), con = sqlcon,index_col = 'index')
    # sqlcon.close()

    for person in matches:
        #temp = co.getUserDetails(person[1],{})  # Method using API calls 
        
        details.append({'name': gameData})
        details.append({'name': temp[person[1]]['personaname'].encode('ascii','ignore'),'percent':str(int(person[0]*100)),
            'url': temp[person[1]]['profileurl'].encode('ascii','ignore'),'avatar': temp[person[1]]['avatarmedium'].encode('ascii','ignore')})
    return details

# Returns the cosine similarity for p1 and p2
def sim_cosine(prefs,p1,p2,normalizeFactor = 1):
    # Get the list of mutually rated items
    si={}
    n = 0
    commonPlaytime = 0
    for item in prefs[p1]:
        if (isinstance(item,int)) and (item in prefs[p2]):
            n+=1   
            si[item]=1
            if prefs[p1][item][0] > prefs[p2][item][0]:
                commonPlaytime = commonPlaytime + prefs[p1][item][0]
            else:
                commonPlaytime = commonPlaytime + (prefs[p2][item][0]-prefs[p1][item][0])

    # if they have no ratings in common, return 0

    if len(si)==0: return (0,n,commonPlaytime,p2)

    # norm1 = sqrt(sum([pow(prefs[p1][item][0],2) for item in prefs[p1]]))
    # norm2 = sqrt(sum([pow(prefs[p2][item][0],2) for item in prefs[p2]]))
    num = sum([prefs[p1][item][0]*prefs[p2][item][0] for item in si if isinstance(item,int)])
    den = prefs[p1]['norm'] * prefs[p2]['norm']
    # den = norm1*norm2
    if den != 0:
        sim = num/den/normalizeFactor
    else:
        sim = 0

    return (sim,n,commonPlaytime,p2)

def nCommon(gameslist,p1,p2):
    si={}
    n = 0
    commonPlaytime = 0
    for item in prefs[p1]:
        if (isinstance(item,int)) and (item in prefs[p2]):
            n+=1   
            si[item]=1
            if prefs[p1][item][0] > prefs[p2][item][0]:
                commonPlaytime = commonPlaytime + prefs[p1][item][0]
            else:
                commonPlaytime = commonPlaytime + (prefs[p2][item][0]-prefs[p1][item][0])

    return (n,commonPlaytime)

def topMatches(prefs,user,compareKeys,n=5,similarity=sim_cosine):
    
    normalizeFactor = similarity(prefs,user,user)[0]
    scores=[similarity(prefs,user,other,normalizeFactor) for other in prefs if (other!=user) & (other in compareKeys)]
    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

def allMatches(prefs,user,compareKeys,n=5,similarity=sim_cosine):
    
    normalizeFactor = similarity(prefs,user,user)
    scores=[(similarity(prefs,user,other)/normalizeFactor,other) for other in prefs]
    
    # Sort the list so the highest scores appear at the top
    return scores[0:n]    

def getMatches(prefs,user,n=5,similarity=sim_cosine):
    
    normalizeFactor = similarity(prefs,user,user)[0]
    scores=[similarity(prefs,user,other,normalizeFactor) for other in prefs if (other!=user)]
    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]