# PyNigiri Quick Reference

## Installation
```bash
pip install ./python
```

## Basic Usage

### Load Timetable
```python
import pynigiri as ng

sources = [ng.TimetableSource("gtfs", "/path/to/gtfs")]
tt = ng.load_timetable(sources, "2024-01-01", "2024-12-31")
```

### Find Locations
```python
loc = tt.find_location("STATION_ID")
name = tt.get_location_name(loc)
coords = tt.get_location_coords(loc)
```

### Create Query
```python
from datetime import datetime

query = ng.Query()
query.start_time = ng.UnixTime(int(datetime.now().timestamp()))
query.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
query.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
query.max_transfers = 3
```

### Route
```python
journeys = ng.route(tt, query)

for journey in journeys:
    print(f"Duration: {journey.travel_time().count()} min")
    print(f"Transfers: {journey.transfers}")
    for leg in journey.legs:
        from_name = tt.get_location_name(leg.from_)
        to_name = tt.get_location_name(leg.to_)
        print(f"  {from_name} → {to_name}")
```

## Advanced Features

### Via Stops
```python
via = ng.ViaStop()
via.location = intermediate_loc
via.stay = ng.Duration(10)  # 10 min minimum stay
query.via_stops = [via]
```

### Time Interval
```python
start = ng.UnixTime(int(datetime.now().timestamp()))
end = ng.UnixTime(int((datetime.now() + timedelta(hours=2)).timestamp()))
query.start_time = ng.TimeInterval(start, end)
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

| Type | Purpose | Example |
|------|---------|---------|
| `LocationIdx(n)` | Location index | `ng.LocationIdx(42)` |
| `Duration(m)` | Time in minutes | `ng.Duration(30)` |
| `UnixTime(s)` | Unix timestamp | `ng.UnixTime(1234567890)` |
| `LatLng(lat, lng)` | Coordinates | `ng.LatLng(52.52, 13.40)` |
| `Offset(loc, dur, mode)` | Start/dest point | `ng.Offset(loc, ng.Duration(0), ng.TransportModeId(0))` |

## Enums

### Transport Classes (Clasz)
`AIR`, `COACH`, `HIGHSPEED`, `LONG_DISTANCE`, `NIGHT`, `REGIONAL`, `REGIONAL_FAST`, `METRO`, `SUBWAY`, `TRAM`, `BUS`, `SHIP`, `OTHER`

### Location Types
`STOP`, `STATION`, `ENTRANCE`, `GENERALIZED_NODE`, `BOARDING_AREA`

### Event Types
`DEP`, `ARR`

### Direction
`FORWARD`, `BACKWARD`

### Location Match Modes
`EXACT`, `EQUIVALENT`, `CHILD`, `ON_TRIP`

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

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_time` | `UnixTime\|TimeInterval` | - | Start time |
| `start` | `List[Offset]` | `[]` | Start locations |
| `destination` | `List[Offset]` | `[]` | Destinations |
| `max_transfers` | `int` | `7` | Max transfers |
| `max_travel_time` | `Duration` | - | Max duration |
| `via_stops` | `List[ViaStop]` | `[]` | Via stops |
| `require_bike_transport` | `bool` | `False` | Need bike |
| `require_car_transport` | `bool` | `False` | Need car |

## Journey Properties

| Property | Type | Description |
|----------|------|-------------|
| `legs` | `List[Leg]` | Journey legs |
| `start_time` | `UnixTime` | Start time |
| `dest_time` | `UnixTime` | End time |
| `transfers` | `int` | Transfer count |
| `travel_time()` | `Duration` | Total duration |
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
