[LookingForSteamPlayers.com] (http://www.lookingforsteamplayers.com/) was developed during the [Insight Data Science program] (http://www.insightdatascience.com/). 

The goal of this project was to create a website where PC gamers could quickly and easily find people to play with based on their gaming tastes. When this project was developed the only way in which to find other gamers was to happen upon them in game, or to post, and search, on forums such as http://www.reddit.com/r/steamship.  But in the digital age with numerous websites matching people for marriage, there had to be a better way!  

LookingForSteamPlayers.com uses a database of Steam users, their games, and their respective playtimes on those games in order to then rate similarity with other uses based on cosine similarity. The database of Steam users is currently 50,000 and growing. Additionally, when a user makes a request to the site, they are permanently added to the database. 

The iPython Notebook titled UserMatching_Validation discusses the metrics used in more detail, and presents a validation method for the user matching process. The similarity scores are merited by the fact that Steam friends tend to have higher similarity scores compared to Steam users matched with random users sharing at least one game. Greater similarities can then be achieved by ranking all available users for highest similarity score. 
 
Finally, the Steam_Games_Analysis notebook contains an interesting data story concerning Steam's games and users. This includes visualizations for the upward trend of game releases and indie developers participation to that trend, an analysis of game genres by playtime and playtime per dollar, and the striking realization that the total playtime for 6 games is equivalent to the total playtime of all of the other games on Steam!  

LookingForSteamPlayers will continue to be supported and improved. Currently, a video game recommendation system based on relative gameplay per game is being added, as well as incorporating Steam achievements into the user matching system which would reflect on gameplay style. Please continue to check the site for new data! 

Presentation: http://www.slideshare.net/mjhines13/looking-for-steam-players-insight-project
