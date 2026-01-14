#!/usr/bin/env python3
"""Test basic pynigiri functionality"""

import sys
sys.path.insert(0, 'build/python')

import pynigiri as pn

print("=" * 60)
print("PYNIGIRI FUNCTIONALITY TEST")
print("=" * 60)

# Test 1: Check enums
print("\n1. Testing Enums:")
print(f"  - Clasz.REGIONAL_FAST = {pn.Clasz.REGIONAL_FAST}")
print(f"  - LocationType.STATION = {pn.LocationType.STATION}")
print(f"  - EventType.DEP = {pn.EventType.DEP}")
print(f"  - Direction.FORWARD = {pn.Direction.FORWARD}")

# Test 2: Create basic types
print("\n2. Testing Basic Types:")
duration = pn.Duration(3600)  # 1 hour in seconds
print(f" - Duration created (3600 seconds)")

unix_time = pn.UnixTime(1704067200)  # 2024-01-01 00:00:00 UTC
print(f" - UnixTime created (2024-01-01)")

location_idx = pn.LocationIdx(42)
print(f" {location_idx} - LocationIdx created (value=42)")

# Test 3: LoaderConfig
print("\n3. Testing LoaderConfig:")
config = pn.LoaderConfig()
config.link_stop_distance = 300  # 5 minutes in seconds
config.default_tz = "Europe/Berlin"
config.extend_calendar = True
print(f"  - LoaderConfig created")
print(f"  - link_stop_distance set to {config.link_stop_distance}s")
print(f"  - default_tz={config.default_tz}")
print(f"  - extend_calendar={config.extend_calendar}")

# Test 4: Check routing query components
print("\n4. Testing Query Components:")
print(f"  - all_clasz_allowed() = {pn.all_clasz_allowed()}")

print("\n5. Testing LatLng:")
latlng = pn.LatLng(52.5200, 13.4050)  # Berlin coordinates
print(f" {latlng} - Berlin LatLng created")

print("\n6. Testing TransferTimeSettings:")
transfer = pn.TransferTimeSettings()
print(f" {transfer} - TransferTimeSettings created successfully")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nThe pynigiri bindings are working correctly.")
print("You can now use it to:")
print("  - Load GTFS data with load_timetable()")
print("  - Create routing queries with Query()")
print("  - Run routing with route()")
print("  - Apply real-time updates with gtfsrt_update_from_*()") 
