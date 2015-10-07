# Imports the necessary modules
# PRAW (Python Reddit Api Wrapper) is what we use to connect to reddit.
import praw
# OBOT is a file we have in out Python34/Lib folder that has a login function to log into reddit with O Auth 2.
import obot
# SQLITE3 is imported so we can use a database to store comment ids that the bot has alreayd seen so it doesn't waste time on them.
import sqlite3
# regex necessary for the moveWord function. Without it we cannot filter out commas for the words.
import re
# Used for making graphs
import matplotlib.pyplot as plt
from optparse import OptionParser
# for uploading pictures/graphs to imgur
import json, requests
# We need the time module to give matplotlib time to generate and save the graph (may not be necessary on good pcs)
import time
# We need this to upload images to imgur
import ibot

# Here we declare some variables that won't be changed while running the bot

# What subreddits will the bot browse? Seperate subreddits with a + sign like news+worldnews . To browse all subreddits type all.
SUBREDDIT = "test"
# The number of most recent comments the bot will get from the subreddit(s). It can import 100 every 2 seconds, so if you need the 1000 latest comments it'll take 20 seconds due to reddit's limit of a query every 2 seconds.
MAXPOSTS = 100
# The Bot's name
BOTNAME = "DnkMemeLinkr"

# Startup, stuff that only runs once when the bot starts up.

print("Opening database...")
# Here we connect to the database that is possible thanks to the sqlite3 module we imported earlier.
sql = sqlite3.connect("stage3.db")
cur = sql.cursor()
# Creates the 'oldposts' database if it doesn't already exist.
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
# Saves the database
sql.commit()

print("Logging in to reddit...")
# logs into reddit with praw
r = obot.login()

# List of people who the bot will respond to
totalListOfWords = []
listOfWords = []

# Graph Stuff
# Make a square figure and axes
plt.figure(1, figsize=(16,9))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
fracs = []
labels = []
explode = []

# We use this function to organize words in a list to a much better looking list. example: ["cow","meow","pig","cow","pig"] turns into [["cow",2],["meow",1],["pig",2]]
def moveWord (word):
    word = word.lower()
    word = re.sub('[^A-Za-z0-9-]+', '', word)
    if len(totalListOfWords) > 0:
        listLength = len(totalListOfWords)
        currentArray = 0
        foundWord = False
        while (currentArray<listLength):
            if foundWord == False:
                if totalListOfWords[currentArray][0] == word:
                    totalListOfWords[currentArray][1] += 1
                    foundWord = True
                if currentArray == (listLength - 1):
                    if totalListOfWords[currentArray][0] != word:
                        totalListOfWords.append([word,1])
            currentArray += 1
    elif len(totalListOfWords) == 0:
        totalListOfWords.append([word,1])
        
def sortTotalListOfWords():
    # The current list in the list we're looking at
    fooCounter = 1
    # The number of lists in the list
    maxCounter = len(totalListOfWords)
    # Just a place to quickly save the list we're looking at
    memOne = []
    # Just a place to quickly save the list before the list we're looking at
    memTwo = []
    while fooCounter < maxCounter:
        if totalListOfWords[fooCounter][1] > totalListOfWords[fooCounter-1][1]:
            memOne = totalListOfWords[fooCounter]
            memTwo = totalListOfWords[fooCounter-1]
            totalListOfWords[fooCounter - 1] = memOne
            totalListOfWords[fooCounter] = memTwo
        fooCounter += 1

def replybot():
    print("Fetching subreddit /r/" + SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    print("Fetching comments from /r/" + SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        # checks if the comment is already in the database by comparing the current comment's id to the ones in the database.
        cur.execute("SELECT * FROM oldposts WHERE ID=?", [comment.id])
        if not cur.fetchone():
            # We're using a try, so if the bot tries to comment on a comment without an author (due to the author being deleted) it won't crash.
            try:
                # The comment author is saved as cauthor
                cauthor = comment.author.name
                # The comment author is saved as user so we can get their comment history
                user = r.get_redditor(cauthor)
                # checks if the bot is replying to itself
                if cauthor.lower() != BOTNAME.lower():
                    # The current comment's content or body is saved as cbody
                    cbody = comment.body.lower()
                    # This string is used for storing all the user's comments content
                    allCommentsString = ""
                    if cbody == "analyzeMyComments".lower():
                        for pastComment in user.get_comments(limit=1000):
                            allCommentsString += pastComment.body.lower() + " "
                        listOfWords = allCommentsString.split()
                        replyMsg = "------------------------- \n\n Bleep Bloop, I am a WIP bot. \n\n Please don't be mad at me \n\n -------------------------- \n\n"
                        for word in listOfWords:
                            moveWord(word)
                        # this part is for the orginization of the totalListOfWords list
                        i = 0
                        mi = len(totalListOfWords)
                        while i < mi:
                            sortTotalListOfWords()
                            i += 1
                        # Adds words and their values from the list to the graph
                        wordsOnGraph = 0
                        for array in totalListOfWords:
                            # The condition after the and eliminates the issue with there being an empty string in the graph
                            if wordsOnGraph < 15 and array[0] != "":
                                explode.append(0.1)
                                fracs.append(array[1])
                                labels.append(array[0])
                                wordsOnGraph += 1
                        # Creates the graph here
                        # autopct='%1.1f%%', somewhere to get percentages
                        plt.pie(fracs, explode=explode, labels=labels, autopct='%.2f', shadow=False, colors=colors)
                        plt.title(cauthor + "\'s comment history", bbox={'facecolor':'0.8', 'pad':5})
                        # saves the graph as 1.png
                        plt.savefig('1.png', bbox_inches='tight')
                        # Gives matplotlib 40 seconds to generate and save the graph
                        print("Giving matplotlib 40 seconds to save the graph...")
                        time.sleep(40)
                        # Uploads the graph to imgur
                        uploadImage = requests.post(
                        'https://api.imgur.com/3/image',
                        data = { 'image': open('1.png', 'rb').read(), 'type': 'file' },
                                headers = {'Authorization': 'Client-ID ' + ibot.api_key}
                                )
                        # Adds the image link to the comment reply string
                        replyMsg += uploadImage.json()['data']['link']
                        print ("Replying to " + cauthor)
                        comment.reply(replyMsg)
                        # Clears the data the bot was using
                        listOfWords.clear()
                        totalListOfWords.clear()
                        fracs.clear()
                        labels.clear()
                        explode.clear()
            except AttributeError:
                pass
            # inserts the comment id into the database
            cur.execute("INSERT INTO oldposts VALUES(?)", [comment.id])
        # saves the database
        sql.commit()

replybot()