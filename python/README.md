# PyNigiri - Python Bindings for Nigiri Transit Routing Library

Complete Python bindings for the [nigiri](https://github.com/motis-project/nigiri) C++ transit routing library.

## Status

✅ **Working** - All core functionality is available and tested.
- ✅ 23 unit tests passing
- ✅ Routing verified working with test GTFS data
- ⚠️ Known datetime conversion issues (workarounds documented)

## Features

- **Data Loading**: Load GTFS, GTFS-RT, HRD, and NeTEx transit data
- **Routing**: Fast RAPTOR-based public transit routing
- **Real-time Updates**: Apply GTFS-RT trip updates and alerts
- **All Transport Types**: Support for all public transit modes (bus, train, tram, ferry, etc.)

## Building

The bindings are built as part of the main nigiri build system:

```bash
cd /home/p4b/pyNigiri/nigiri
cmake -B build -DPYTHON_BINDING=ON -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build build --target pynigiri -j8
```

The compiled module will be at: `build/python/pynigiri.cpython-*.so`

## Usage

```python
import sys
sys.path.insert(0, 'build/python')
import pynigiri as ng
from datetime import datetime, timedelta, date

# Load GTFS data (use current year for your data)
current_year = date.today().year
sources = [ng.TimetableSource("gtfs", "/path/to/gtfs")]
timetable = ng.load_timetable(sources, f"{current_year}-01-01", f"{current_year}-12-31")

# Find locations
start_loc = timetable.find_location("STATION_A_ID")
dest_loc = timetable.find_location("STATION_B_ID")

# Create routing query
query = ng.Query()

# CRITICAL: Convert datetime to MINUTES (not seconds!)
query_time = datetime(current_year, 1, 15, 10, 0, 0)
query.start_time = int(query_time.timestamp()) // 60  # Divide by 60!

# Use timedelta and plain int
query.start = [ng.Offset(start_loc, timedelta(0), 0)]
query.destination = [ng.Offset(dest_loc, timedelta(0), 0)]
query.max_transfers = 6
query.max_travel_time = timedelta(hours=10)
query.start_match_mode = ng.LocationMatchMode.EQUIVALENT
query.dest_match_mode = ng.LocationMatchMode.EQUIVALENT

# Run routing
journeys = ng.route(timetable, query)

# Process results
for journey in journeys:
    print(f"Transfers: {journey.transfers}")
    print(f"Travel time: {journey.travel_time().count()} minutes")
    for leg in journey.legs:
        # Use getattr for 'from' (Python keyword)
        from_loc = getattr(leg, 'from')
        from_name = timetable.get_location_name(from_loc)
        to_name = timetable.get_location_name(leg.to)
        print(f"  {from_name} -> {to_name}")
```

## Available Types

### Enums
- `Clasz`: Transport class (REGIONAL, LONG_DISTANCE, SUBWAY, TRAM, BUS, etc.)
  - ⚠️ Use `SUBWAY` (not `METRO`)
- `LocationType`: Location types (STATION, TRACK, GENERATED_TRACK)
- `EventType`: Event types (DEP, ARR)
- `Direction`: Search direction (FORWARD, BACKWARD)
- `LocationMatchMode`: Location matching (EXACT, EQUIVALENT, ONLY_CHILDREN)
  - ⚠️ Use `ONLY_CHILDREN` (not `CHILD`)

### Core Types
- `Timetable`: Main timetable data structure
- `Query`: Routing query configuration
- `Journey`: Routing result with legs
- `LoaderConfig`: Configuration for data loading
- `RtTimetable`: Real-time timetable

### Functions
- `load_timetable()`: Load transit data
- `route()`: Perform routing query
- `gtfsrt_update_from_bytes()`: Apply GTFS-RT updates from bytes
- `gtfsrt_update_from_string()`: Apply GTFS-RT updates from string
- `gtfsrt_update_from_file()`: Apply GTFS-RT updates from file

## Testing

Run the test suite to verify the bindings work correctly:
nigiri/python
pytest tests/
```

Expected output:
```
======================== 23 passed ========================
```

All tests should pass. The test suite covers:
- Core types (Duration, LocationIdx, Footpath, etc.)
- Timetable loading and queries
- Routing query setup and execution
- Real-time updates

⚠️ **Note**: Tests use correct API patterns (timedelta/datetime, not Duration/UnixTime)
ALL TESTS PASSED!
```

## Installation via pip (TODO)

Future work: Package as a proper Python wheel for easy installation:

```bash
cd python
pip install .
```

## Implementation Notes

- Built with [pybind11](https://github.com/pybind/pybind11) v2.11.1
- Requires C++23 compiler (GCC 13+ or Clang 16+)
- Uses CMake for build configuration
- All static libraries compiled with `-fPIC` for shared library compatibility
- Strong type wrappers for type safety (LocationIdx, TransportIdx, etc.)

## Files

- `src/main.cc`: Module entry point
- `src/types.cc`: Core types and enums
- `src/timetable.cc`: Timetable access
- `src/loader.cc`: Data loading
- `src/routing.cc`: Routing algorithms
- `src/rt.cc`: Real-time updates
- `pybind_common.h`: Common headers

## License

Same as nigiri - MIT License
