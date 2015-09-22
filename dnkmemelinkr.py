import praw
import obot
import sqlite3

SUBREDDIT = "test"
MAXPOSTS = 10

BATTLEISJOINED = ["ALLAH", "RAPIER IS PRIMARY"]
BATTLEISJOINED_RESPONSE = "https://www.youtube.com/watch?v=FcmWaz_UTBQ"
MONEYGUN_GIF = ["money gun","money gun gif","moneygun.gif","money_gun.gif"]
MONEYGUN_GIF_RESPONSE = "http://i.imgur.com/CVHxR4g.webm"

print('Opening database')
sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
sql.commit()

print("Logging in to reddit")

r = obot.login()


def replybot():
    print('Fetching subrredt /r/' + SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    print('Fetching comments from /r/' + SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [comment.id])
        if not cur.fetchone():
            try:
                cauthor = comment.author.name
                if cauthor.lower() != 'DnkMemeLinkr'.lower():
                    cbody = comment.body.lower()
                    if any(key.lower() in cbody for key in BATTLEISJOINED):
                        print("Replying to " + cauthor)
                        comment.reply(BATTLEISJOINED_RESPONSE)
                    if any(key.lower() in cbody for key in MONEYGUN_GIF):
                        print("Replying to " + cauthor)
                        comment.reply(MONEYGUN_GIF_RESPONSE)
            except AttributeError:
                pass
            cur.execute('INSERT INTO oldposts VALUES(?)', [comment.id])
        sql.commit()
while True:
    replybot()
