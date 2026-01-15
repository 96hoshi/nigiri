from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "test" / "test_data"
GTFS_PATH = DATA_DIR / "gtfs" / "de"


GTFS_RT_URL = "https://example.com/gtfs-rt/tripupdates"  # Update with actual URL
GTFS_RT_PATH = "path/to/gtfs-rt.pb"  # Update with actual path

STATION_ID_A = "620363"  
STATION_ID_B = "112300"  

# Invalid location index constant (UINT32_MAX)
INVALID_LOCATION_IDX = 4294967295