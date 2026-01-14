# PyNigiri - Python Bindings for Nigiri Transit Routing Library

Complete Python bindings for the [nigiri](https://github.com/motis-project/nigiri) C++ transit routing library.

## Status

✅ **Working** - All core functionality is available and tested.

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
import pynigiri as pn

# Load GTFS data
config = pn.LoaderConfig()
config.default_tz = "Europe/Berlin"
timetable = pn.load_timetable(["/path/to/gtfs"], config, pn.FinalizeOptions())

# Create a routing query
query = pn.Query()
query.start_time = pn.UnixTime(1704067200)  # 2024-01-01 00:00:00 UTC
query.start_match_mode = pn.LocationMatchMode.EXACT
query.dest_match_mode = pn.LocationMatchMode.EXACT

# Add start and destination locations
start_id = pn.LocationId(pn.LocationIdx(0), pn.SourceIdx(0))
dest_id = pn.LocationId(pn.LocationIdx(1), pn.SourceIdx(0))

# Run routing
journeys = pn.route(timetable, start_id, dest_id, query, pn.Direction.FORWARD)

# Process results
for journey in journeys:
    print(f"Journey with {len(journey.legs)} legs")
    for leg in journey.legs:
        print(f"  Transport: {leg.transport}")
```

## Available Types

### Enums
- `Clasz`: Transport class (REGIONAL, REGIONAL_FAST, LONG_DISTANCE, etc.)
- `LocationType`: Location types (STATION, TRACK, GENERATED_TRACK)
- `EventType`: Event types (DEP, ARR)
- `Direction`: Search direction (FORWARD, BACKWARD)
- `LocationMatchMode`: Location matching (EXACT, EQUIVALENT, ONLY_CHILDREN)

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

```bash
cd /home/p4b/pyNigiri/nigiri
python3 test_bindings.py
```

Expected output:
```
============================================================
PYNIGIRI FUNCTIONALITY TEST
============================================================
...
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
