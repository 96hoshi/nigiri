# PyNigiri Quick Reference

⚠️ **Important**: Use `datetime`/`timedelta` instead of `ng.UnixTime`/`ng.Duration` (see below)

## Installation
```bash
pip install ./python
```

## Basic Usage

### Load Timetable
```python
import pynigiri as ng
from datetime import date

current_year = date.today().year
sources = [ng.TimetableSource("gtfs", "/path/to/gtfs")]
tt = ng.load_timetable(sources, f"{current_year}-01-01", f"{current_year}-12-31")
```

### Find Locations
```python
loc = tt.find_location("STATION_ID")
name = tt.get_location_name(loc)
coords = tt.get_location_coords(loc)
```

### Create Query
```python
from datetime import datetime, timedelta

query = ng.Query()

# CRITICAL: Convert to MINUTES (not seconds!)
query_time = datetime(2026, 1, 15, 10, 0, 0)
query.start_time = int(query_time.timestamp()) // 60  # Divide by 60!

# Use timedelta and plain int
query.start = [ng.Offset(start_loc, timedelta(0), 0)]
query.destination = [ng.Offset(dest_loc, timedelta(0), 0)]
query.max_transfers = 6
query.max_travel_time = timedelta(hours=10)
query.start_match_mode = ng.LocationMatchMode.EQUIVALENT
query.dest_match_mode = ng.LocationMatchMode.EQUIVALENT
```

### Route
```python
journeys = ng.route(tt, query)

for journey in journeys:
    print(f"Duration: {journey.travel_time().count()} min")
    print(f"Transfers: {journey.transfers}")
    for leg in journey.legs:
        # Use getattr for 'from' (Python keyword)
        from_loc = getattr(leg, 'from')
        from_name = tt.get_location_name(from_loc)
        to_name = tt.get_location_name(leg.to)
        print(f"  {from_name} → {to_name}")
```

## Advanced Features

### Via Stops
```python
from datetime import timedelta

via = ng.ViaStop()
via.location = intermediate_loc
via.stay = timedelta(minutes=10)  # 10 min minimum stay
query.via_stops = [via]
```

### Time Interval
```python
from datetime import datetime, timedelta

# For time intervals, still use integers (minutes)
start_time = datetime.now()
end_time = start_time + timedelta(hours=2)
query.start_time = int(start_time.timestamp()) // 60
# Note: TimeInterval support may have limitations
```

### Transport Filters
```python
query.require_bike_transport = True
query.allowed_claszes = ng.all_clasz_allowed()
```

## Real-Time Updates

### Create RT Timetable
```python
from datetime import date

rt_tt = ng.create_rt_timetable(tt, date.today())
```

### Apply GTFS-RT
```python
# From file
stats = ng.gtfsrt_update_from_file(
    tt, rt_tt, ng.SourceIdx(0), "updates", "gtfsrt.pb"
)

# From bytes
stats = ng.gtfsrt_update_from_bytes(
    tt, rt_tt, ng.SourceIdx(0), "updates", data
)
```

### Route with RT
```python
journeys = ng.route_with_rt(tt, rt_tt, query)
```

## Common Types

⚠️ **Note:** Use Python's `datetime`/`timedelta` instead of `Duration`/`UnixTime` for inputs!

| Type | Purpose | Recommended Usage |
|------|---------|-------------------|
| `LocationIdx(n)` | Location index | `ng.LocationIdx(42)` |
| `timedelta(minutes=m)` | Duration (use instead of Duration) | `timedelta(minutes=30)` |
| `datetime(...)` | Timestamp (use instead of UnixTime) | `datetime(2026, 1, 15, 10, 0)` |
| `LatLng(lat, lng)` | Coordinates | `ng.LatLng(52.52, 13.40)` |
| `Offset(loc, dur, mode)` | Start/dest point | `ng.Offset(loc, timedelta(0), 0)` |

## Enums

### Transport Classes (Clasz)
`AIR`, `COACH`, `HIGHSPEED`, `LONG_DISTANCE`, `NIGHT`, `REGIONAL`, `REGIONAL_FAST`, `SUBWAY`, `TRAM`, `BUS`, `SHIP`, `OTHER`

⚠️ **Note:** Use `SUBWAY` (not `METRO`)

### Location Types
`TRACK`, `STATION`, `GENERATED_TRACK`

⚠️ **Note:** Only these three are exposed

### Event Types
`DEP`, `ARR`

### Direction
`FORWARD`, `BACKWARD`

### Location Match Modes
`EXACT`, `EQUIVALENT`, `ONLY_CHILDREN`, `ON_TRIP`

⚠️ **Note:** Use `ONLY_CHILDREN` (not `CHILD`)

## Timetable Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `find_location(id)` | `Optional[LocationIdx]` | Find location by ID |
| `get_location_name(loc)` | `str` | Get location name |
| `get_location_coords(loc)` | `LatLng` | Get coordinates |
| `get_location_type(loc)` | `LocationType` | Get type |
| `n_locations()` | `int` | Total locations |
| `n_routes()` | `int` | Total routes |
| `date_range()` | `(date, date)` | Date range |

## Query Parameters

⚠️ **Critical:** For `start_time`, convert to MINUTES: `int(timestamp()) // 60`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_time` | `int` (minutes) | - | Start time (convert with `// 60`) |
| `start` | `List[Offset]` | `[]` | Start locations |
| `destination` | `List[Offset]` | `[]` | Destinations |
| `max_transfers` | `int` | `7` | Max transfers |
| `max_travel_time` | `timedelta` | - | Max duration |
| `via_stops` | `List[ViaStop]` | `[]` | Via stops |
| `require_bike_transport` | `bool` | `False` | Need bike |
| `require_car_transport` | `bool` | `False` | Need car |

## Journey Properties

| Property | Type | Description |
|----------|------|-------------|
| `legs` | `List[Leg]` | Journey legs |
| `transfers` | `int` | Transfer count |
| `travel_time()` | `Duration` | Total duration (call `.count()` for minutes) |

⚠️ **Note:** `start_time`/`dest_time` may show as 1970 dates due to conversion issues
| `departure_time()` | `UnixTime` | Departure |
| `arrival_time()` | `UnixTime` | Arrival |

## Files

| File | Purpose |
|------|---------|
| `README.md` | Quick start |
| `INSTALL.md` | Installation |
| `API.md` | API reference |
| `examples/` | Usage examples |
| `tests/` | Unit tests |

## Help

- Examples: `python/examples/*.py`
- Tests: `pytest python/tests/`
- Docs: `less python/API.md`
- Build: `./python/build.sh`
