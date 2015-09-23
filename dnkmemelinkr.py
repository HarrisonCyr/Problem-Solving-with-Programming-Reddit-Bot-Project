# imports praw, Python Reddit Api Wrapper
import praw
# imports obot, a file which should be in your Lib folder inside your python installation. It contains the function login() for logging in to reddit with O Auth 2
import obot
# imports sqlite3 so we can use a database for storing comment ids so we don't reply to a comment more than once
import sqlite3
# subreddit the bot monitors. Add a + between subreddits to fetch comments from more than one
SUBREDDIT = "test+eve+australia+funny"
# number of the most recent comments the bot will get from the subreddit(s)
MAXPOSTS = 100
# Put trigger phrases & responses here
BATTLEISJOINED = ["RAPIER IS THE FUCKING PRIMARY","ALLAH", "RAPIER IS PRIMARY", "primary is the rapier", "rapier", "primary rapier", "allahhhhhhhhhh",]
BATTLEISJOINED_RESPONSE = "https://www.youtube.com/watch?v=otEC3Ultq2k"
MONEYGUN_GIF = ["money gun","money gun gif","moneygun.gif","money_gun.gif"]
MONEYGUN_GIF_RESPONSE = "http://i.imgur.com/CVHxR4g.webm"
JARED_FOGGLE = ["jared foggle"]
JARED_FOGGLE_RESPONSE = "eat fresh"
EVE_CYNO_UP = ["WE HAVE BEEN SUMMONED","cyno up","jump jump jump" "cyno up jump jump jump", "here we go boys"]
EVE_CYNO_UP_RESPONSE = "http://gfycat.com/AlienatedScarceJuliabutterfly#"
FACEPALM = ["facepalm.jpg","facepalm.gif","facepalm.png"]
FACEPALM_RESPONSE = "http://img2.wikia.nocookie.net/__cb20141214203128/fossils-archeology/images/f/f6/640px-Annoyed-facepalm-picard-l.png"

print('Opening database')
sql = sqlite3.connect('sql.db')
cur = sql.cursor()
# creates the database 'oldposts' if it doesn't already exist with just a text field meant for containing comment ids
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
# saves the database
sql.commit()

print("Logging in to reddit")
# logs into reddit with praw
r = obot.login()


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
                    if any(key.lower() in cbody for key in JARED_FOGGLE):
                        print("Replying to " + cauthor)
                        comment.reply(JARED_FOGGLE_RESPONSE)
                    if any(key.lower() in cbody for key in EVE_CYNO_UP):
                        print("Replying to " + cauthor)
                        comment.reply(EVE_CYNO_UP_RESPONSE)
                    if any(key.lower() in cbody for key in BATTLEISJOINED):
                        print("Replying to " + cauthor)
                        comment.reply(BATTLEISJOINED_RESPONSE)
                    if any(key.lower() in cbody for key in MONEYGUN_GIF):
                        print("Replying to " + cauthor)
                        comment.reply(MONEYGUN_GIF_RESPONSE)
                    if any(key.lower() in cbody for key in FACEPALM):
                        print("Replying to " + cauthor)
                        comment.reply(FACEPALM_RESPONSE)
            except AttributeError:
                pass
            # inserts the comment id into the database
            cur.execute('INSERT INTO oldposts VALUES(?)', [comment.id])
        # saves the database
        sql.commit()
while True:
    replybot()
