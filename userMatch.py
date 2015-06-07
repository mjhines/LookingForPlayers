"""
User matching functions
"""
from __future__ import division
from math import sqrt
import pickle
from dataCollecting.privateData import pdir
import dataCollecting.collect as co
import sys

def match(steamid,userGames,nMatches):

    if steamid not in userGames:
        print 'Updating user into database...'
        userGames = co.getOwnedGames(steamid,userGames) # Collect data about each player's games
        userGames[steamid].update({'norm': sqrt(sum([pow(userGames[steamid][item][0],2) for item in userGames[steamid]]))})

    if steamid not in userGames:
        print 'Cannot compare: User either does not have enough playtime or has profile set to private'
        return 

    print 'Calculating similarity metrics...'
    matches = getMatches(userGames,steamid,n=nMatches,similarity=sim_cosineRecent)

    print 'Collecting data on matches...'

    matchIDs = '['
    for person in matches:
        matchIDs = matchIDs + str(person[3]) +','
    matchIDs = matchIDs + ']'    
    userData = co.getNumerousUsers(matchIDs); names = []
    for match in matches:
        names.append({'name': userData[str(match[3])]['personaname'].encode('ascii','ignore'),
                      'percent':str(int(match[0]*100)), 
                      'ncommonGames':str(int(match[1])),
                      'url': userData[str(match[3])]['profileurl'].encode('ascii','ignore'),
                      'avatar': userData[str(match[3])]['avatarfull'].encode('ascii','ignore')})

    return names

# Returns the euclidian similarity for p1 and p2
def sim_euclidian(prefs,p1,p2,normalizeFactor = 1):
    # Get the list of mutually rated items
    si={}; n = 0
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

    vec1 = [pow(prefs[p1][item][0]-prefs[p2][item][0],2) for item in si]
    vec2 = [pow(prefs[p1][item][0],2) for item in prefs[p1] if item not in prefs[p2]]
    vec3 = [pow(prefs[p2][item][0],2) for item in prefs[p2] if item not in prefs[p1]]

    sum_of_squares = sum(vec1+vec2+vec3)
    sim = 1/(1+sqrt(sum_of_squares))/normalizeFactor

    return (sim,n,commonPlaytime,p2)

# Returns the tanimoto similarity for p1 and p2
def sim_tanimoto(prefs,p1,p2,normalizeFactor = 1):
    # Get the list of mutually rated items
    si={}; n = 0
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

    num = sum([(prefs[p1][item][0]*prefs[p2][item][0]) for item in si if isinstance(item,int)])
    den = pow(prefs[p1]['norm'],2)+pow(prefs[p2]['norm'],2)-num
    if den != 0:
        sim = num/den/normalizeFactor
    else:
        sim = 0

    return (sim,n,commonPlaytime,p2)

# Returns the cosine similarity for p1 and p2
def sim_cosineRecent(prefs,p1,p2,normalizeFactor = 1,w1=0.75):
    # Get the list of mutually rated items
    si={}; n = 0
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

    recent1 = sqrt(sum([pow(prefs[p1][item][1],2) for item in prefs[p1] if isinstance(item,int)]))
    recent2 = sqrt(sum([pow(prefs[p2][item][1],2) for item in prefs[p2] if isinstance(item,int)]))

    num_recent = sum([(prefs[p1][item][1]*prefs[p2][item][1]) for item in si if isinstance(item,int)])
    den_recent = recent1*recent2

    num_alltime = sum([(prefs[p1][item][0]*prefs[p2][item][0]) for item in si if isinstance(item,int)])
    den_alltime = (prefs[p1]['norm']*prefs[p2]['norm'])
    # den = norm1*norm2
    if (den_alltime != 0) & (den_recent != 0):
        sim = ((1-w1)*(num_alltime/den_alltime) + w1*(num_recent/den_recent))/normalizeFactor
    elif (den_alltime != 0):
        sim = (1-w1)*(num_alltime/den_alltime)/normalizeFactor
    else:
        sim = 0

    return (sim,n,commonPlaytime,p2)

# Returns the cosine similarity for p1 and p2
def sim_cosine(prefs,p1,p2,normalizeFactor = 1):
    # Get the list of mutually rated items
    si={}; n = 0
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

    # sump1 = sum([prefs[p1][item][0] for item in prefs[p1]])
    # sump2 = sum([prefs[p2][item][0] for item in prefs[p2]])

    # norm1 = sqrt(sum([pow(prefs[p1][item][0],2) for item in prefs[p1]]))
    # norm2 = sqrt(sum([pow(prefs[p2][item][0],2) for item in prefs[p2]]))

    # nGames1 = len(prefs[p1])
    # nGames2 = len(prefs[p2])

    num = sum([(prefs[p1][item][0]*prefs[p2][item][0]) for item in si if isinstance(item,int)])
    den = (prefs[p1]['norm']*prefs[p2]['norm'])
    # den = norm1*norm2
    if den != 0:
        sim = num/den/normalizeFactor
    else:
        sim = 0

    return (sim,n,commonPlaytime,p2)

def nCommon(gameslist,p1,p2):
    n = 0; commonPlaytime = 0
    for item in prefs[p1]:
        if (isinstance(item,int)) and (item in prefs[p2]):
            n+=1   
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



# Old code for SQL server 
    # userGrab = [str(person[3]) for person in matches]
    # sqlcon = mdb.connect('localhost','root',sqlpwd,'lfp')

    # urlstart = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/'
    # urlend = '_full.jpg'
    
    # matchIDs = '['
    # for person in matches:
    #     matchIDs = matchIDs + str(person[3]) +','
    # matchIDs = matchIDs + ']'

    # names = []
    # for match in matches:
        # print str(type(person[1]))
        # user = pd.read_sql('SELECT * FROM users WHERE steamid = '+str(person[3]), con = sqlcon,index_col = 'index')

        # names.append({'name': user.ix['76561197972322556'].personaname,
        #               'percent':str(int(person[0]*100)), 
        #               'ncommonGames':str(int(person[1])),
        #                'url': user.ix['76561197972322556'].profileurl,
        #                'avatar': urlstart + user.ix['76561197972322556'].avatar + urlend})

        # # user = userDict[person[3]]
        # names.append({'name': user['personaname'].encode('ascii','ignore'),'percent':str(int(person[0]*100)), 'ncommonGames':str(int(person[1])),
        #     'url': user['profileurl'].encode('ascii','ignore'),'avatar': user['avatarfull'].encode('ascii','ignore')})

    # sqlcon.close()
    #name = getMatchesNames(matches)