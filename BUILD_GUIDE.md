# Nigiri Python Wheel Build Process

This document describes the complete process for building the Nigiri transit routing library as a Python wheel.

## Overview

Nigiri is a C++23 transit routing library with Python bindings created using pybind11. This build process compiles the C++ code and packages it into a distributable Python wheel (.whl) file.

## Quick Start

To build the wheel, run from the nigiri directory:

```bash
./build_wheel.sh
```

The wheel will be created at `dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl`

## Requirements

- **Python**: 3.11+
- **pybind11**: Python binding library (`sudo apt install python3-pybind11` or `pip install pybind11`)
- **CMake**: 3.25.1+
- **C++ Compiler**: Supporting C++23 (GCC 13+ or Clang 16+)
- **System Libraries**: All C++ dependencies are bundled/built from source

## Build Process Details

The build script performs the following steps:

### 1. Clean Previous Builds
Removes any existing build artifacts:
- `build/` directory
- `dist/` directory  
- `*.egg-info` directories

### 2. CMake Configuration
Configures the project with the following key settings:
- `CMAKE_BUILD_TYPE=Release` for optimized code
- `CMAKE_POSITION_INDEPENDENT_CODE=ON` (critical for shared libraries)
- All dependencies built from source (LuaJIT, PROJ, protobuf, boost, etc.)

### 3. C++ Compilation
Builds the following components:
- nigiri C++ library (`libnigiri.a`)
- Python extension module (`_nigiri.cpython-311-x86_64-linux-gnu.so`)
- All dependencies (abseil, protobuf, PROJ, geo, etc.)

Uses parallel compilation with `-j$(nproc)` for faster builds.

### 4. Python Wheel Creation
Packages the compiled extension into a wheel using `setup.py`:
- Copies the `.so` file into the `nigiri/` package directory
- Creates proper Python package structure with `__init__.py`
- Generates wheel metadata
- Creates distributable `.whl` file

## Package Structure

```
nigiri-0.1.0-cp311-cp311-linux_x86_64.whl
├── nigiri/
│   ├── __init__.py                                    # Python package init
│   └── _nigiri.cpython-311-x86_64-linux-gnu.so       # Compiled C++ extension (6.2M)
└── nigiri-0.1.0.dist-info/
    ├── METADATA                                       # Package metadata
    ├── WHEEL                                          # Wheel format info
    ├── top_level.txt                                  # Top-level package names
    ├── RECORD                                         # File checksums
    └── licenses/LICENSE                               # MIT License
```

## Installation

Install the wheel using uv or pip:

```bash
# Using pip
pip install dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl

# Or with uv
uv pip install dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl
```

## Testing the Installation

Verify the installation works:

```python
import nigiri

print(f"Version: {nigiri.__version__}")
print(f"Available classes: {[x for x in dir(nigiri) if not x.startswith('_')]}")

# Available classes and functions:
# - Timetable: Main timetable data structure
# - Query: Routing query configuration
# - Journey, JourneyLeg: Routing results
# - Direction: FORWARD, BACKWARD, EQUIVALENT
# - LocationMatchMode: EXACT, INTERMODAL, ONLY_CHILDREN
# - load_timetable(): Load GTFS/HRD data
# - hello(): Test function
```

Or use the provided test script:

```bash
./test_import.py
# or
./test_wheel.sh
```

## Platform Compatibility

**Current Build:**
- **OS**: Linux x86_64
- **Python**: 3.11
- **Wheel Name**: `nigiri-0.1.0-cp311-cp311-linux_x86_64.whl`

**Important Notes:**
- This wheel is **platform-specific** and will only work on Linux x86_64 with Python 3.11
- For other platforms (macOS, Windows) or Python versions, separate wheels must be built
- The C++ extension is compiled as a shared library with platform-specific binary format

### Building for Other Platforms

To build wheels for multiple platforms, consider using:
- **cibuildwheel**: Automated multi-platform wheel builder
- **Docker**: Build wheels in controlled environments for different Linux distributions
- **Native builds**: Build directly on target platforms (macOS, Windows)

## Build Artifacts

After a successful build:

```
nigiri/
├── build/                                    # CMake build directory
│   ├── _nigiri.cpython-311-x86_64-linux-gnu.so  # Compiled extension (6.2M)
│   ├── libnigiri.a                           # Static library
│   └── deps/                                 # Compiled dependencies
├── dist/                                     # Distribution directory
│   └── nigiri-0.1.0-cp311-cp311-linux_x86_64.whl  # Final wheel (2.3M)
├── nigiri/                                   # Python package source
│   └── __init__.py                          # Package init file
├── python/                                   # Python bindings source
│   ├── CMakeLists.txt                       # Python build config
│   └── bindings.cpp                         # pybind11 bindings
├── deps/                                     # C++ dependencies (generated)
├── build_wheel.sh                           # Build script
├── test_wheel.sh                            # Test script
├── test_import.py                           # Python test script
├── setup.py                                 # Wheel packaging script
├── pyproject.toml                           # Project metadata
└── CMakeLists.txt                          # CMake build configuration
```

## Key Technical Details

### CMAKE_POSITION_INDEPENDENT_CODE

**Critical Setting:** The global `CMAKE_POSITION_INDEPENDENT_CODE ON` setting is essential for building Python extensions. Without this, you'll encounter linking errors:

```
relocation R_X86_64_TPOFF32 against symbol `<name>' can not be used when making 
a shared object; recompile with -fPIC
```

This setting ensures all static libraries are compiled with `-fPIC` flag, making them suitable for linking into shared libraries.

### Dependencies

All dependencies are built from source as part of the CMake build:
- **LuaJIT**: Embedded Lua interpreter
- **PROJ**: Cartographic projections library
- **protobuf**: Protocol buffers for GTFS-RT
- **abseil-cpp**: C++ utility library
- **boost**: C++ libraries (variant, etc.)
- **zlib-ng**: Compression library
- **fmt**: Formatting library
- **date**: Date/time library
- **geo**: Geographic utilities
- **opentelemetry**: Observability framework
- **pybind11**: C++/Python binding library

### Build Time

Approximate build time on a modern multi-core system:
- **Clean build**: 3-5 minutes
- **Incremental build**: 10-30 seconds (if only nigiri sources changed)

## Troubleshooting

### Common Issues

1. **Missing CMAKE_POSITION_INDEPENDENT_CODE**
   ```
   Error: relocation ... can not be used when making a shared object
   Solution: Add `set(CMAKE_POSITION_INDEPENDENT_CODE ON)` to CMakeLists.txt
   ```

2. **Module not found after installation**
   ```
   Solution: Ensure the wheel has proper package structure with __init__.py
   ```

3. **Import error: cannot import name '_nigiri'**
   ```
   Solution: Check that __init__.py uses `from nigiri._nigiri import *`
   ```

4. **Build failures with dependencies**
   ```
   Solution: Clean rebuild with `rm -rf build dist`
   ```

## Integration with GOAT Repository

To use this wheel in the GOAT project:

### Option 1: Direct Installation

```bash
cd /app
uv pip install ./packages/cpp/nigiri/dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl
```

### Option 2: Add to pyproject.toml

```toml
[project]
dependencies = [
    "nigiri @ file:///app/packages/cpp/nigiri/dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl"
]
```

## CI/CD Considerations

For automated builds:

1. **Build in Docker**: Ensures consistent build environment
2. **Cache Dependencies**: Cache the `build/deps/` directory to speed up builds
3. **Artifact Storage**: Store wheels as build artifacts
4. **Version Tagging**: Use git tags to version wheels
5. **Platform Matrix**: Build for multiple platforms if needed

## License

Nigiri is licensed under the MIT License. See the LICENSE file for details.

## Additional Resources

- [pybind11 Documentation](https://pybind11.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [CMake Documentation](https://cmake.org/documentation/)
- [Wheel Format Specification](https://packaging.python.org/specifications/binary-distribution-format/)
