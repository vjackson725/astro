
from datetime import datetime, timedelta
from pathlib import Path

from skyfield.api import load
from skyfield.almanac import seasons, SEASON_EVENTS_NEUTRAL, moon_phases, MOON_PHASES
from skyfield.searchlib import find_discrete

from icalendar import Calendar, Event

# 🌑🌒🌓🌔🌕🌖🌗🌘
# 🍂🌼🌸🌻⛄☀️❄️

eph = load('de421.bsp')

ts = load.timescale()

t0 = ts.utc(2024, 1, 1)
t1 = ts.utc(2050, 12, 31)

events = []

# Seasons

ts, ys = find_discrete(t0, t1, seasons(eph))

for yi, ti in zip(ys, ts):
  # shifted because we're in the southern hemisphere
  match SEASON_EVENTS_NEUTRAL[yi]:
    case "March Equinox":
      events.append((ti, "Autumn Equinox 🍂"))
    case "June Solstice":
      events.append((ti, "Winter Solstice ❄️"))
    case "September Equinox":
      events.append((ti, "Spring Equinox 🌸"))
    case "December Solstice":
      events.append((ti, "Summer Solstice ☀️"))

# Moon Phases

ts, ys = find_discrete(t0, t1, moon_phases(eph))

for yi, ti in zip(ys, ts):
  # note: quarters are reversed, again, because we are in the southern hemisphere
  match MOON_PHASES[yi]:
    case 'New Moon':      events.append((ti, "New Moon 🌑"))
    case 'First Quarter': events.append((ti, "First Quarter 🌗"))
    case 'Full Moon':     events.append((ti, "Full Moon 🌕"))
    case 'Last Quarter':  events.append((ti, "Last Quarter 🌓"))

events.sort(key=lambda p: p[0].utc_datetime())

# Calendar

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Astronomical Calendar//vjackson725.github.io//')
cal.add('x-wr-calname', 'Astronomical Calendar')

for evdat in events:
  event = Event()
  event.add("summary", evdat[1])
  event.add("dtstart", evdat[0].utc_datetime())
  event.add("dtend", evdat[0].utc_datetime())
  cal.add_component(event)

ics_path = Path("astrocal.ics")
with open(ics_path, mode="wb") as f:
  f.write(cal.to_ical())
