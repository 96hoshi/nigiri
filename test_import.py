#!/usr/bin/env python3
"""Test script to verify nigiri wheel installation and import."""

import sys

try:
    import nigiri
    print("✓ Nigiri imported successfully!")
    print(f"  Version: {nigiri.__version__}")
    print(f"  Module location: {nigiri.__file__}")
    print(f"  Available attributes: {[x for x in dir(nigiri) if not x.startswith('_')]}")
    sys.exit(0)
except ImportError as e:
    print(f"✗ Failed to import nigiri: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)
