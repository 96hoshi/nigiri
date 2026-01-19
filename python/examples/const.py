from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "test" / "test_data"
GTFS_PATH = DATA_DIR / "gtfs" / "de"


GTFS_RT_URL = "https://example.com/gtfs-rt/tripupdates"  # Update with actual URL
GTFS_RT_PATH = "path/to/gtfs-rt.pb"  # Update with actual path

# Valid station IDs from the test GTFS data (German stations)
STATION_ID_A = "390686"  # Aachen Hbf (main station)
STATION_ID_B = "465374"  # Bremen Hbf (main station)
STATION_ID_C = "465102"  # Aschaffenburg Hbf
STATION_ID_D = "432997"  # Augsburg Hbf
STATION_ID_E = "567631"  # Bayreuth Hbf

# Invalid location index constant (UINT32_MAX)
INVALID_LOCATION_IDX = 4294967295