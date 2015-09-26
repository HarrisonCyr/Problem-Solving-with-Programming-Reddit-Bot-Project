# imports praw, Python Reddit Api Wrapper
import praw
# imports obot, a file which should be in your Lib folder inside your python installation. It contains the function login() for logging in to reddit with O Auth 2
import obot
# imports sqlite3 so we can use a database for storing comment ids so we don't reply to a comment more than once
import sqlite3
import re
# subreddit the bot monitors. Add a + between subreddits to fetch comments from more than one
SUBREDDIT = "test+eve+australia+funny"
# number of the most recent comments the bot will get from the subreddit(s)
MAXPOSTS = 100
# Put trigger phrases & responses here


print('Opening database')
sql = sqlite3.connect('stage3.db')
cur = sql.cursor()
# creates the database 'oldposts' if it doesn't already exist with just a text field meant for containing comment ids
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
# saves the database
sql.commit()

print("Logging in to reddit")
# logs into reddit with praw
r = obot.login()

botRespondsTo = ["Ralph_Charante","GraphiteHippo"]

def replybot():
    print('Fetching subrredt /r/' + SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    print('Fetching comments from /r/' + SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        # checks if comment is already in the database
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [comment.id])
        # if it is, it'll skip that comment.
        if not cur.fetchone():
            # using a try so if the bot tries to comment on a comment without an author, it won't crash
            try:
                # the comment's author is saved as cauthor
                cauthor = comment.author.name
                # checks if the bot is replying to itself. If not then it procedes
                if cauthor.lower() != 'DnkMemeLinkr'.lower():
                    # the comment's body is saved as cbody
                    cbody = comment.body.lower()
                    for whale in botRespondsTo:
                        if cauthor.lower() == whale.lower():
                            listOfWords = []
                            totalListOfWords = []
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
                            print("Replying to " + cauthor)
                            listOfWords = cbody.split()
                            replyMsg = ""
                            for word in listOfWords:
                                moveWord(word)
                            for array in totalListOfWords:
                                replyMsg += array[0] + " was said: " + str(array[1]) + " times. \n\n"
                            comment.reply(replyMsg)
            except AttributeError:
                pass
            # inserts the comment id into the database
            cur.execute('INSERT INTO oldposts VALUES(?)', [comment.id])
        # saves the database
        sql.commit()
while True:
    replybot()
