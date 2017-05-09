from peewee import *
from datetime import datetime

DATABASE = 'cache.db'

db = SqliteDatabase(DATABASE)


class Podcast(Model):
    name = CharField()
    url = CharField()
    last_played_update = DateTimeField(null=True)
    last_played_at = DateTimeField(null=True)
    play_at = TimeField()

    class Meta:
        database = db


# Hopefully run once to set up our database and tables
if __name__ == "__main__":
    db.connect()
    db.create_tables([Podcast], safe=True)

    # Seed data (it's the alarm I want!)
    scheduled_alarm = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour=7, minute=0)
    Podcast.create(name="Up First", url='https://www.npr.org/rss/podcast.php?id=510318',
                   last_played_update=None, last_played_at=None, play_at=scheduled_alarm)
