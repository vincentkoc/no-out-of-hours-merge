import datetime
import sys
from typing import Dict, List, Tuple

import pytz

# Timezone and restricted times configuration
tz = pytz.timezone("Australia/Sydney")
restricted_times: Dict[str, List[Tuple[float, float]]] = {
    "mon": [(0, 7), (16.5, 24)],
    "tue": [(0, 7), (16.5, 24)],
    "wed": [(0, 7), (16.5, 24)],
    "thu": [(0, 7), (16.5, 24)],
    "fri": [(0, 7), (16.5, 24)],
    "sat": [(0, 24)],
    "sun": [(0, 24)],
}

now = datetime.datetime.now(tz)
weekday = now.strftime("%a").lower()
hour = now.hour + (now.minute / 60)

if any(start <= hour < end for start, end in restricted_times[weekday]):
    print("❌ Merging is not allowed during the specified time.")
    sys.exit(1)
else:
    print("✅ Merging is allowed at this time.")
    sys.exit(0)
