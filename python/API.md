# PyNigiri API Reference

Complete API reference for the PyNigiri Python bindings.

## Table of Contents

- [Core Types](#core-types)
- [Timetable](#timetable)
- [Loading Data](#loading-data)
- [Routing](#routing)
- [Real-Time Updates](#real-time-updates)

---

## Core Types

### LocationIdx

Represents a location index in the timetable.

```python
LocationIdx(value: int)
```

**Methods:**

- `__int__() -> int`: Convert to integer
- `__eq__, __ne__, __lt__`: Comparison operators

**Example:**

```python
idx = ng.LocationIdx(42)
print(int(idx))  # 42
```

### Duration

Represents a time duration in minutes.

```python
Duration(minutes: int)
```

**Methods:**

- `count() -> int`: Get duration in minutes
- `__int__() -> int`: Convert to integer

**Example:**

```python
d = ng.Duration(30)
print(d.count())  # 30
```

### UnixTime

Represents a Unix timestamp.

```python
UnixTime(seconds: int)
```

**Methods:**

- `count() -> int`: Get timestamp in seconds
- `__int__() -> int`: Convert to integer

**Example:**

```python
from datetime import datetime
t = ng.UnixTime(int(datetime.now().timestamp()))
```

### LatLng

Represents geographical coordinates.

```python
LatLng(lat: float, lng: float)
```

**Attributes:**

- `lat`: Latitude
- `lng`: Longitude

**Example:**

```python
coords = ng.LatLng(52.5200, 13.4050)  # Berlin
```

### LocationId

Identifies a location with source and ID.

```python
LocationId(src: SourceIdx, id: str)
```

**Attributes:**

- `src`: Source index
- `id`: Location ID string

### Footpath

Represents a walking connection.

```python
Footpath(target: LocationIdx, duration: Duration)
```

**Attributes:**

- `target`: Target location
- `duration`: Walking duration

### TimeInterval

Represents a time range.

```python
TimeInterval(from_: UnixTime, to_: UnixTime)
```

**Attributes:**

- `from_`: Start time
- `to_`: End time

**Methods:**

- `contains(time: UnixTime) -> bool`: Check if time is in interval

### Enums

#### Clasz

Transport class/type:

- `AIR`, `COACH`, `HIGHSPEED`, `LONG_DISTANCE`, `NIGHT`
- `REGIONAL`, `REGIONAL_FAST`, `METRO`, `SUBWAY`
- `TRAM`, `BUS`, `SHIP`, `OTHER`

#### LocationType

- `STOP`, `STATION`, `ENTRANCE`, `GENERALIZED_NODE`, `BOARDING_AREA`

#### EventType

- `DEP` (Departure), `ARR` (Arrival)

#### Direction

- `FORWARD`, `BACKWARD`

---

## Timetable

### Timetable

Main timetable object containing all schedule data.

**Methods:**

#### `find_location(id: str, src: SourceIdx = 0) -> Optional[LocationIdx]`

Find a location by its ID.

```python
loc = timetable.find_location("STATION_123")
if loc is not None:
    print(f"Found: {loc}")
```

#### `get_location_name(loc: LocationIdx) -> str`

Get the name of a location.

```python
name = timetable.get_location_name(loc)
```

#### `get_location_coords(loc: LocationIdx) -> LatLng`

Get coordinates of a location.

```python
coords = timetable.get_location_coords(loc)
print(f"Lat: {coords.lat}, Lng: {coords.lng}")
```

#### `get_location_type(loc: LocationIdx) -> LocationType`

Get the type of a location.

```python
loc_type = timetable.get_location_type(loc)
```

#### `get_location_parent(loc: LocationIdx) -> LocationIdx`

Get the parent location (e.g., station for a platform).

```python
parent = timetable.get_location_parent(loc)
```

#### `n_locations() -> int`

Get total number of locations.

#### `n_routes() -> int`

Get total number of routes.

#### `n_transports() -> int`

Get total number of transport services.

#### `date_range() -> Tuple[date, date]`

Get the date range covered by the timetable.

---

## Loading Data

### TimetableSource

Specifies a data source for loading.

```python
TimetableSource(
    tag: str,
    path: str,
    config: LoaderConfig = LoaderConfig()
)
```

**Attributes:**

- `tag`: Identifier for the source
- `path`: File system path to data
- `loader_config`: Configuration options

**Example:**

```python
source = ng.TimetableSource(
    tag="my_gtfs",
    path="/path/to/gtfs",
    config=ng.LoaderConfig()
)
```

### LoaderConfig

Configuration for data loading.

**Attributes:**

- `link_stop_distance`: Distance for linking stops
- `default_tz`: Default timezone
- `ignore_errors`: Whether to ignore errors
- `adjust_footpaths`: Whether to adjust footpaths

### FinalizeOptions

Options for finalizing timetable after loading.

**Attributes:**

- `merge_duplicates`: Merge duplicate trips
- `adjust_footpaths`: Adjust footpath durations
- `footpaths`: Footpath settings

### FootpathSettings

Settings for footpath generation.

**Attributes:**

- `max_duration`: Maximum footpath duration

### load_timetable()

Load timetable from sources.

```python
load_timetable(
    sources: List[TimetableSource],
    start_date: str,
    end_date: str,
    options: FinalizeOptions = FinalizeOptions()
) -> Timetable
```

**Parameters:**

- `sources`: List of data sources
- `start_date`: Start date (format: "YYYY-MM-DD")
- `end_date`: End date (format: "YYYY-MM-DD")
- `options`: Finalization options

**Example:**

```python
sources = [ng.TimetableSource("gtfs", "/path/to/gtfs")]
tt = ng.load_timetable(sources, "2024-01-01", "2024-12-31")
```

### load_timetable_dt()

Load timetable using datetime objects.

```python
load_timetable_dt(
    sources: List[TimetableSource],
    start: datetime,
    end: datetime,
    options: FinalizeOptions = FinalizeOptions()
) -> Timetable
```

---

## Routing

### Query

Routing query configuration.

```python
Query()
```

**Attributes:**

- `start_time`: Start time (UnixTime or TimeInterval)
- `start`: List of start locations with offsets
- `destination`: List of destination locations with offsets
- `max_transfers`: Maximum number of transfers (default: 7)
- `max_travel_time`: Maximum travel time
- `max_start_offset`: Maximum offset from start location
- `start_match_mode`: Location matching mode for start
- `dest_match_mode`: Location matching mode for destination
- `use_start_footpaths`: Use footpaths at start
- `prf_idx`: Profile index
- `allowed_claszes`: Mask of allowed transport classes
- `require_bike_transport`: Require bicycle transport
- `require_car_transport`: Require car transport
- `via_stops`: List of intermediate stops
- `extend_interval_earlier`: Extend search interval earlier
- `extend_interval_later`: Extend search interval later
- `slow_direct`: Allow slower direct connections

**Methods:**

- `flip_dir()`: Flip query direction (forward/backward)

**Example:**

```python
query = ng.Query()
query.start_time = ng.UnixTime(int(datetime.now().timestamp()))
query.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
query.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
query.max_transfers = 3
```

### Offset

Location offset for start/destination.

```python
Offset(
    target: LocationIdx,
    duration: Duration,
    transport_mode: TransportModeId = 0
)
```

**Methods:**

- `target() -> LocationIdx`: Get target location
- `duration() -> Duration`: Get duration
- `type() -> TransportModeId`: Get transport mode

### ViaStop

Intermediate stop requirement.

```python
ViaStop()
```

**Attributes:**

- `location`: Location index
- `stay`: Minimum stay duration

### LocationMatchMode

Enum for location matching:

- `EXACT`: Exact location match
- `EQUIVALENT`: Match equivalent locations
- `CHILD`: Match child locations
- `ON_TRIP`: Match any stop on trip

### Journey

Routing result representing one journey.

**Attributes:**

- `legs`: List of journey legs
- `start_time`: Journey start time
- `dest_time`: Journey destination time
- `transfers`: Number of transfers
- `price`: Journey price (if available)

**Methods:**

- `travel_time() -> Duration`: Get total travel time
- `departure_time() -> UnixTime`: Get departure time
- `arrival_time() -> UnixTime`: Get arrival time
- `dominates(other: Journey) -> bool`: Check if dominates another journey
- `__len__() -> int`: Get number of legs
- `__getitem__(index: int) -> Leg`: Get leg by index

**Example:**

```python
for journey in journeys:
    print(f"Departure: {journey.departure_time()}")
    print(f"Arrival: {journey.arrival_time()}")
    print(f"Travel time: {journey.travel_time().count()} minutes")
    print(f"Transfers: {journey.transfers}")

    for leg in journey.legs:
        print(f"  {leg}")
```

### Leg

One segment of a journey.

**Attributes:**

- `from_`: Start location
- `to_`: End location
- `dep_time`: Departure time
- `arr_time`: Arrival time
- `uses_`: Transport used (run, footpath, or offset)

### route()

Execute routing query.

```python
route(timetable: Timetable, query: Query) -> List[Journey]
```

**Example:**

```python
journeys = ng.route(timetable, query)
```

### route_with_rt()

Execute routing with real-time data.

```python
route_with_rt(
    timetable: Timetable,
    rt_timetable: RtTimetable,
    query: Query
) -> List[Journey]
```

---

## Real-Time Updates

### RtTimetable

Real-time timetable with live updates.

```python
RtTimetable()
```

### create_rt_timetable()

Create real-time timetable for a day.

```python
create_rt_timetable(
    timetable: Timetable,
    day: date
) -> RtTimetable
```

**Example:**

```python
from datetime import date
rt_tt = ng.create_rt_timetable(timetable, date.today())
```

### gtfsrt_update_from_bytes()

Apply GTFS-RT update from bytes.

```python
gtfsrt_update_from_bytes(
    timetable: Timetable,
    rt_timetable: RtTimetable,
    source: SourceIdx,
    tag: str,
    data: bytes
) -> Statistics
```

### gtfsrt_update_from_string()

Apply GTFS-RT update from string.

```python
gtfsrt_update_from_string(
    timetable: Timetable,
    rt_timetable: RtTimetable,
    source: SourceIdx,
    tag: str,
    data: str
) -> Statistics
```

### gtfsrt_update_from_file()

Apply GTFS-RT update from file.

```python
gtfsrt_update_from_file(
    timetable: Timetable,
    rt_timetable: RtTimetable,
    source: SourceIdx,
    tag: str,
    file_path: str
) -> Statistics
```

**Example:**

```python
stats = ng.gtfsrt_update_from_file(
    timetable, rt_tt, ng.SourceIdx(0), "updates", "gtfsrt.pb"
)
print(f"Success: {stats.total_entities_success}")
```

### Statistics

GTFS-RT update statistics.

**Attributes:**

- `parser_error`: Parser error flag
- `total_entities`: Total entities processed
- `total_entities_success`: Successful updates
- `total_entities_fail`: Failed updates
- `total_alerts`: Total alerts processed
- `total_vehicles`: Total vehicle positions
- And more...

---

## Utility Functions

### all_clasz_allowed()

Get mask allowing all transport classes.

```python
mask = ng.all_clasz_allowed()
query.allowed_claszes = mask
```

### no_clasz_allowed()

Get mask allowing no transport classes.

```python
mask = ng.no_clasz_allowed()
```

---

For more examples, see the `examples/` directory.
