#!/bin/bash
# Quick test script to verify the nigiri wheel installation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WHEEL_FILE="$SCRIPT_DIR/dist/nigiri-0.1.0-cp311-cp311-linux_x86_64.whl"

echo "========================================="
echo "Nigiri Wheel Installation Test"
echo "========================================="
echo ""

# Check if wheel exists
if [ ! -f "$WHEEL_FILE" ]; then
    echo "❌ Error: Wheel file not found at $WHEEL_FILE"
    echo "Please run ./build_wheel.sh first"
    exit 1
fi

echo "Found wheel: $(basename "$WHEEL_FILE")"
echo ""

# Install the wheel
echo "Installing nigiri wheel..."
python3 -m pip install --force-reinstall "$WHEEL_FILE" --quiet

echo "✓ Installation complete"
echo ""

# Test import
echo "Testing nigiri import..."
python3 << 'EOF'
import nigiri
print("✓ Nigiri imported successfully!")
print(f"  Module location: {nigiri.__file__}")
print(f"  Version: {nigiri.__version__}")

# List available attributes
attrs = [x for x in dir(nigiri) if not x.startswith("_")]
if attrs:
    print(f"  Available attributes: {len(attrs)} items")
else:
    print("  Note: No public attributes exposed (this may be normal)")
EOF

echo ""
echo "========================================="
echo "✓ All tests passed!"
echo "========================================="
