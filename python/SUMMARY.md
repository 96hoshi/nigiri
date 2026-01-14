# PyNigiri - Complete Python Bindings for Nigiri

## Overview

This directory contains complete Python bindings for the nigiri C++ transit routing library. The bindings are created using pybind11 and provide a Pythonic interface to all major functionality of the library.

## What's Included

### Core Bindings (`src/`)

1. **types.cc** - Basic types and data structures
   - Location indices and IDs
   - Duration and time types
   - Enumerations (transport classes, location types, etc.)
   - Footpaths and intervals

2. **timetable.cc** - Timetable data access
   - Location queries and information
   - Route and transport data
   - Coordinate access
   - Date range information

3. **loader.cc** - Data loading functionality
   - GTFS/HRD/NetEx data loading
   - Loader configuration
   - Footpath generation
   - Timetable source management

4. **routing.cc** - Routing algorithms
   - Query configuration
   - Journey planning
   - RAPTOR search
   - Multi-criteria optimization
   - Via stops and intervals

5. **rt.cc** - Real-time updates
   - GTFS-RT support
   - Real-time timetable creation
   - Update statistics
   - File/bytes/string input

### Python Package (`pynigiri/`)

- `__init__.py` - Package initialization and exports

### Examples (`examples/`)

1. **basic_routing.py** - Simple routing example
2. **realtime_updates.py** - GTFS-RT updates
3. **advanced_routing.py** - Advanced features (via stops, intervals, filters)
4. **explore_timetable.py** - Data exploration

### Tests (`tests/`)

1. **test_types.py** - Type system tests
2. **test_loader.py** - Data loading tests
3. **test_routing.py** - Routing functionality tests
4. **test_rt.py** - Real-time update tests

### Documentation

1. **README.md** - Quick start guide
2. **INSTALL.md** - Detailed installation instructions
3. **API.md** - Complete API reference
4. **LICENSE** - MIT license

### Build Configuration

1. **CMakeLists.txt** - CMake build configuration
2. **pyproject.toml** - Modern Python packaging
3. **setup.py** - Build script
4. **MANIFEST.in** - Package manifest

## Features Covered

### ✅ Data Loading
- Load GTFS, HRD, and NetEx data
- Configure loading options
- Generate footpaths
- Merge duplicates
- Support for multiple data sources

### ✅ Timetable Access
- Find locations by ID
- Get location names, coordinates, types
- Access route and transport data
- Query date ranges
- Navigate location hierarchies

### ✅ Routing
- Single and multi-criteria routing
- Forward and backward search
- Time intervals
- Via stops with minimum stay times
- Multiple start/destination points
- Transport class filtering
- Bicycle/car transport requirements
- Custom transfer times
- Maximum transfers and travel time limits

### ✅ Real-Time Updates
- GTFS-RT trip updates
- GTFS-RT service alerts
- GTFS-RT vehicle positions
- Update from files, bytes, or strings
- Detailed statistics
- Multiple data sources

### ✅ Advanced Features
- Location matching modes (exact, equivalent, child, on-trip)
- Time-dependent footpaths
- Transport mode identification
- Journey comparison and domination
- Extensible query configuration

## Architecture

```
pynigiri (Python Module)
    │
    ├── Core Types (types.cc)
    │   └── Basic data structures
    │
    ├── Timetable (timetable.cc)
    │   └── Data access and queries
    │
    ├── Loader (loader.cc)
    │   └── Data import functionality
    │
    ├── Routing (routing.cc)
    │   └── Journey planning algorithms
    │
    └── Real-Time (rt.cc)
        └── Live data updates
```

## Building

### Quick Start
```bash
pip install ./python
```

### Development Mode
```bash
pip install -e ./python
```

### With CMake
```bash
cmake -B build -DPYTHON_BINDING=ON
cmake --build build --target pynigiri
```

See [INSTALL.md](INSTALL.md) for detailed instructions.

## Usage Example

```python
import pynigiri as ng
from datetime import datetime

# Load data
sources = [ng.TimetableSource("gtfs", "/path/to/gtfs")]
tt = ng.load_timetable(sources, "2024-01-01", "2024-12-31")

# Create query
query = ng.Query()
query.start_time = ng.UnixTime(int(datetime.now().timestamp()))
query.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
query.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
query.max_transfers = 3

# Route
journeys = ng.route(tt, query)

# Process results
for journey in journeys:
    print(f"Travel time: {journey.travel_time().count()} minutes")
    print(f"Transfers: {journey.transfers}")
```

## API Coverage

The bindings cover all essential functionality:

- ✅ Core data types and structures
- ✅ Timetable loading and access
- ✅ Routing queries and configuration
- ✅ Journey representation and analysis
- ✅ Real-time data updates
- ✅ GTFS-RT support
- ✅ Multi-criteria optimization
- ✅ Advanced query features

## Performance

The bindings are designed for performance:

- Zero-copy data access where possible
- Efficient C++ to Python conversions
- Minimal overhead for common operations
- Native C++ speed for routing algorithms

## Testing

Run the test suite:
```bash
cd python
pytest tests/ -v
```

Test coverage includes:
- Unit tests for all major components
- Integration tests (with sample data)
- Example verification

## Contributing

When adding new features:

1. Add C++ bindings in `src/`
2. Export in `__init__.py`
3. Add tests in `tests/`
4. Add examples in `examples/`
5. Update API documentation

## Compatibility

- Python: 3.8+
- C++: C++23
- Platforms: Linux, macOS, Windows
- Compilers: GCC 11+, Clang 14+, MSVC 2022+

## Dependencies

- pybind11 (automatically fetched)
- numpy (optional, for array operations)
- Python development headers

## License

MIT License - see LICENSE file

## Support

- Documentation: See API.md
- Examples: See examples/
- Issues: GitHub Issues
- Questions: GitHub Discussions

## Future Enhancements

Potential additions:
- Numpy array support for batch operations
- Async/await support for long-running queries
- Progress callbacks
- More detailed journey information
- Shape/polyline data access
- Fare calculation bindings
- Additional data format support

## Acknowledgments

Built on the excellent nigiri C++ library and pybind11 binding framework.
