from models import Podcast
from datetime import datetime
from datetime import timezone
import calendar
import feedparser
import requests
import re
import os

for podcast in Podcast.select().order_by(Podcast.last_played_at.asc()):
    # Find the next due time and convert to UTC for comparison.
    now = datetime.now()
    duetime = datetime(
        now.year, now.month, now.day, podcast.play_at.hour, podcast.play_at.minute)
    duetime = datetime.utcfromtimestamp(duetime.timestamp())

    # See if it is time to play this podcast: we must have slightly gone over
    # the next due time and we can't have already played this episode today.
    if duetime > datetime.utcnow() or (podcast.last_played_at != None and podcast.last_played_at > duetime):
        print("Not due yet.")
        continue

    # Get the latest episode from our latest field
    feed = feedparser.parse(podcast.url)
    latest = feed.entries[0]

    # Comparing UTC struct_time to see if we played this episode already
    if podcast.last_played_update != None and latest.published_parsed <= podcast.last_played_update.utctimetuple():
        print("Already played this episode.")
        continue

    # If we got to this part, then we are clear to play this episode!
    # Let's download and play it!
    r = requests.get(latest.links[0].href, stream=True)

    audio_file_name = "%s.mp3" % re.sub('\s', '_', podcast.name.lower())
    print("Downloading %s" % audio_file_name)

    with open(audio_file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)

    # We should save all database datetime entries as UTC time
    # We are taking away the time zone because otherwise it will not parse properly
    podcast.last_played_update = datetime.fromtimestamp(
        calendar.timegm(latest.published_parsed), tz=timezone.utc).replace(tzinfo=None)
    podcast.last_played_at = datetime.utcnow()
    podcast.save()

    # For Raspberry Pi
    os.system("omxplayer %s" % audio_file_name)
