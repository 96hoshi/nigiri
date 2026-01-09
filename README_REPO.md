# Nigiri Python Bindings

Python wheel package for [nigiri](https://github.com/motis-project/nigiri) transit routing C++ library with pybind11 bindings.

## Features

- 🚄 Fast transit routing using the nigiri C++ library
- 🐍 Python 3.11 bindings via pybind11
- 📦 Packaged as a Python wheel for easy installation
- 🔧 Self-contained build system with automated scripts
- 🏗️ CMake-based build with Position Independent Code (PIC) support

## Quick Start

### Prerequisites

- Python 3.11
- CMake 3.22+
- C++23 compatible compiler (GCC 12+, Clang 16+)
- Build tools: `build-essential`, `cmake`, `python3-dev`
- uv package manager (or pip)

### Build the Wheel

```bash
# Simple one-command build
./build_wheel.sh

# Output will be in dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl
```

### Install and Test

```bash
# Install the wheel
uv pip install dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl

# Test the installation
python3 test_import.py
```

Or use the automated test script:

```bash
./test_wheel.sh
```

## Usage

```python
import nigiri

# Load a timetable
timetable = nigiri.load_timetable("path/to/gtfs")

# Create a routing query
query = nigiri.Query()
# ... configure query ...

# Perform routing
journeys = timetable.route(query)
```

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed documentation.

## Repository Structure

```
.
├── build_wheel.sh          # Main build script
├── test_wheel.sh           # Test script
├── test_import.py          # Python import test
├── BUILD_GUIDE.md          # Complete build documentation
├── CHANGES.md              # Summary of modifications
├── CMakeLists.txt          # CMake configuration (with PIC enabled)
├── setup.py                # Python packaging
├── pyproject.toml          # Python project metadata
├── nigiri/                 # Python package directory
│   └── __init__.py        # Package initialization
├── python/                 # pybind11 bindings
│   ├── CMakeLists.txt
│   └── bindings.cpp
├── include/               # C++ headers
├── src/                   # C++ source
└── cmake/                 # CMake modules
```

## Platform Support

Currently builds for:
- **Linux x86_64** with Python 3.11

For other platforms (macOS, Windows), you need to rebuild the wheel on that platform using the same build script.

## Key Modifications

This repository includes modifications to the original nigiri library to enable Python wheel building:

1. **CMakeLists.txt**: Added `CMAKE_POSITION_INDEPENDENT_CODE ON` (line 4) for shared library compatibility
2. **setup.py**: Updated to properly package the Python extension module
3. **Build scripts**: Automated build and test scripts for wheel creation
4. **.gitignore**: Enhanced to exclude build artifacts while tracking source code

See [CHANGES.md](CHANGES.md) for complete details.

## Documentation

- [BUILD_GUIDE.md](BUILD_GUIDE.md) - Complete build guide with troubleshooting
- [CHANGES.md](CHANGES.md) - Summary of modifications made to nigiri

## License

This project inherits the license from the original [nigiri](https://github.com/motis-project/nigiri) library. See [LICENSE](LICENSE) for details.

## Credits

- Original nigiri library: https://github.com/motis-project/nigiri
- Python bindings and build system: This repository

## Contributing

Contributions are welcome! Please ensure:
1. The build script runs successfully
2. Tests pass with `./test_wheel.sh`
3. Code follows existing style conventions

## Troubleshooting

### Build fails with PIC errors
The `CMAKE_POSITION_INDEPENDENT_CODE ON` flag should be enabled in CMakeLists.txt (line 4).

### Import fails after installation
Ensure you're using Python 3.11 and the wheel matches your platform (Linux x86_64).

### Missing dependencies
Run the build script, which auto-fetches all required dependencies via CMake.

For more troubleshooting, see [BUILD_GUIDE.md](BUILD_GUIDE.md#troubleshooting).
