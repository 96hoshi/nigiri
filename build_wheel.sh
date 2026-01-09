#!/bin/bash
set -e  # Exit on error

# Nigiri Wheel Build Script
# This script automates the complete process of building the nigiri Python wheel
# from the C++ source code with pybind11 bindings.

echo "========================================="
echo "Nigiri Wheel Build Script"
echo "========================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
BUILD_DIR="$SCRIPT_DIR/build"
DIST_DIR="$SCRIPT_DIR/dist"
JOBS=${JOBS:-$(nproc)}

echo "Working directory: $SCRIPT_DIR"
echo "Build directory: $BUILD_DIR"
echo "Parallel jobs: $JOBS"
echo ""

# Step 1: Clean previous builds
echo "Step 1: Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR" "$SCRIPT_DIR/nigiri.egg-info"
mkdir -p "$BUILD_DIR"
echo "✓ Clean complete"
echo ""

# Step 2: Run CMake configuration
echo "Step 2: Configuring CMake..."
cd "$BUILD_DIR"
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DCMAKE_CXX_STANDARD=23
echo "✓ CMake configuration complete"
echo ""

# Step 3: Build the C++ extension
echo "Step 3: Building C++ extension module..."
cmake --build . --target _nigiri -j"$JOBS"

# Verify the .so file was created
SO_FILE=$(find "$BUILD_DIR" -name "_nigiri.cpython-*.so" -type f)
if [ -z "$SO_FILE" ]; then
    echo "❌ Error: Python extension module (.so file) not found!"
    exit 1
fi

SO_SIZE=$(du -h "$SO_FILE" | cut -f1)
echo "✓ Build complete: $SO_FILE ($SO_SIZE)"
echo ""

# Step 4: Create Python wheel
echo "Step 4: Creating Python wheel..."
cd "$SCRIPT_DIR"

# Ensure setuptools and wheel are installed (use --break-system-packages for newer systems)
python3 -m pip install --quiet --break-system-packages setuptools wheel 2>/dev/null || true

# Build the wheel
python3 setup.py bdist_wheel --quiet

# Find and report the wheel
WHEEL_FILE=$(find "$DIST_DIR" -name "*.whl" -type f | head -1)
if [ -z "$WHEEL_FILE" ]; then
    echo "❌ Error: Wheel file not found!"
    exit 1
fi

WHEEL_SIZE=$(du -h "$WHEEL_FILE" | cut -f1)
WHEEL_NAME=$(basename "$WHEEL_FILE")

echo "✓ Wheel created: $WHEEL_NAME ($WHEEL_SIZE)"
echo ""

# Step 5: Display installation instructions
echo "========================================="
echo "Build Complete!"
echo "========================================="
echo ""
echo "Wheel file: $WHEEL_FILE"
echo ""
echo "To install the wheel:"
echo "  pip install $WHEEL_FILE"
echo ""
echo "Or with uv:"
echo "  uv pip install $WHEEL_FILE"
echo ""
echo "To test the installation:"
echo "  python3 -c 'import nigiri; print(\"Nigiri version:\", nigiri.__version__)'"
echo ""
echo "========================================="
