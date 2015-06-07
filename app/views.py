from flask import render_template, flash, redirect, request, url_for
from app import app
import userMatch
from dataCollecting.privateData import pdir
import pickle
# import MySQLdb as mdb

with open(pdir + 'data/userGamesDictPreCompute', 'rb') as f:
    userGames = pickle.load(f)

# with open(pdir + 'data/userDict', 'rb') as f:
#     userDict = pickle.load(f)

# Landing Page 
@app.route('/')
def landing():
    return render_template('landing.html')

# User Matched Page
@app.route('/index', methods=['POST'])
def index():
	steamid = request.form['steamid']	
	nMatches = request.form['nMatches']	

	try: 
		nMatches = int(nMatches)
	except:
		return render_template('landing.html')

	try:
		steamNumber = int(steamid)
	except:
		return render_template('landing.html')

	if nMatches > 100:
		nMatches = 100


	# if steamid not in userGames.keys():
	# 	print 'Updating user into database...'
	# 	userGames = co.getOwnedGames(steamid,userGames) # Collect data about each player's games

	# if steamid not in userGames.keys():
	# 	print 'Cannot compare: User either does not have enough playtime or has profile set to private'
	# 	return 

	# print 'Calculating similarity metrics...'
	# matches = getMatches(userGames,steamid,n=10)
	# topMatches = getMatchesNames(matches)

	topMatches = userMatch.match(steamid,userGames,int(nMatches))

	return render_template('index.html',steamid=steamid,topMatches = topMatches,nMatches=nMatches)

# @app.route("/userMatches")
# def slide():
# 	return "User Matches"

# About Me Page
@app.route("/about")
def about():
	return render_template('about.html')

# Slides 
@app.route("/slides")
def slide():
    return render_template('slides.html')
#	return "Slides Here!"

