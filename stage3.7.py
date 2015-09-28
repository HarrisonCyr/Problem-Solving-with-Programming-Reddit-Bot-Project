import praw
import obot
import sqlite3
import re
SUBREDDIT = "test"
MAXPOSTS = 100
print("Opening database...")
sql = sqlite3.connect('stage3.db')
cur = sql.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()
print("Logging in to reddit..."
print("Brushing Sheep...")
r = obot.login()
botRespondsTo = ["tstAccountPleaseIgno","Animatronic-Panda"]

def replyBot():
      print("Fetching subreddit /r/" + SUBREDDIT)
      subreddit = r.get_subreddit(SUBREDDIT)
      print("Fetching comments from /r/" + SUBREDDIT)
      comments =
