"""
User matching functions
"""
from __future__ import division
from math import sqrt
import pickle
from privateData import pdir
import dataCollecting.collect as co

def match(steamid,userGames):

    print 'Please wait a moment while the database is loaded...'
    #with open(pdir + 'data/usersGamesDict', 'rb') as f:

    if steamid not in userGames.keys():
        print 'Updating user into database...'
        userGames = co.getOwnedGames(steamid,userGames) # Collect data about each player's games

    if steamid not in userGames.keys():
        print 'Cannot compare: User either does not have enough playtime or has profile set to private'
        return 

    print 'Calculating similarity metrics...'
    matches = getMatches(userGames,steamid,n=10)
    name = getMatchesNames(matches)
    return name

def getMatchesNames(matches):
    details = []
    for person in matches:
        temp = co.getUserDetails(person[1],{})  
        ngames = 1 

        details.append({'name': temp[person[1]]['personaname'].encode('ascii','ignore'),'percent':str(int(person[0]*100)),'url': temp[person[1]]['profileurl'].encode('ascii','ignore'),'avatar': temp[person[1]]['avatarmedium'].encode('ascii','ignore')})
        # details = (str(int(person[0]*100)),temp[person[1]]['personaname'].encode('ascii','ignore'))
        #details.append(
        # print(str(int(person[0]*100)) + ' percent match with ' + temp[person[1]]['personaname'].encode('ascii','ignore') + ', steamid = ' + str(person[1]) )
    return details

# Returns the cosine similarity for p1 and p2
def sim_cosine(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1

    # if they have no ratings in common, return 0

    if len(si)==0: return 0

    norm1 = sqrt(sum([pow(prefs[p1][item][0],2) for item in prefs[p1]]))
    norm2 = sqrt(sum([pow(prefs[p2][item][0],2) for item in prefs[p2]]))
    num = sum([prefs[p1][item][0]*prefs[p2][item][0] for item in si])
    den = norm1*norm2
    if den != 0:
        sim = num/(norm1*norm2)
    else:
        sim = 0

    return sim	

def topMatches(prefs,user,compareKeys,n=5,similarity=sim_cosine):
    
    normalizeFactor = similarity(prefs,user,user)
    scores=[(similarity(prefs,user,other)/normalizeFactor,other) for other in prefs if (other!=user) & (other in compareKeys)]
    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getMatches(prefs,user,n=5,similarity=sim_cosine):
    
    normalizeFactor = similarity(prefs,user,user)
    scores=[(similarity(prefs,user,other)/normalizeFactor,other) for other in prefs if (other!=user)]
    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]