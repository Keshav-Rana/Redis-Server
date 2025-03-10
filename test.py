from datetime import datetime, timezone, timedelta
import time

unixTimeString = '1741563850'
unixTime = int(unixTimeString)

dt = datetime.fromtimestamp(unixTime, tz=timezone.utc)

currDt = datetime.now(timezone.utc)

secs = (dt - currDt).total_seconds()
print(secs)