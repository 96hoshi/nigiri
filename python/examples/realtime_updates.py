"""
Real-time update example: Apply GTFS-RT updates to a timetable.
"""
import sys
sys.path.insert(0, 'build/python')

import pynigiri as ng
from datetime import datetime
import requests

def main():
    print("Loading static timetable...")
    
    # Load static timetable
    sources = [
        ng.TimetableSource(
            tag="my_gtfs",
            path="path/to/gtfs",
            config=ng.LoaderConfig()
        )
    ]
    
    timetable = ng.load_timetable(
        sources=sources,
        start_date="2024-01-01",
        end_date="2024-12-31"
    )
    
    print(f"Loaded timetable: {timetable}")
    
    # Create real-time timetable
    print("\nCreating real-time timetable...")
    today = datetime.now().date()
    # Note: You'll need to convert datetime.date to the appropriate format
    # This is a simplified example
    rt_tt = ng.create_rt_timetable(timetable, today)
    
    print("Real-time timetable created")
    
    # Option 1: Load GTFS-RT from URL
    try:
        url = "https://example.com/gtfs-rt/tripupdates"  # Update with actual URL
        response = requests.get(url)
        
        if response.status_code == 200:
            print("\nApplying GTFS-RT updates from URL...")
            stats = ng.gtfsrt_update_from_bytes(
                timetable=timetable,
                rt_timetable=rt_tt,
                source=ng.SourceIdx(0),
                tag="trip_updates",
                data=response.content
            )
            
            print(f"Update statistics: {stats}")
            print(f"  Total entities: {stats.total_entities}")
            print(f"  Success: {stats.total_entities_success}")
            print(f"  Failed: {stats.total_entities_fail}")
    except Exception as e:
        print(f"Error loading from URL: {e}")
    
    # Option 2: Load GTFS-RT from file
    try:
        print("\nApplying GTFS-RT updates from file...")
        stats = ng.gtfsrt_update_from_file(
            timetable=timetable,
            rt_timetable=rt_tt,
            source=ng.SourceIdx(0),
            tag="local_updates",
            file_path="path/to/gtfs-rt.pb"  # Update with actual path
        )
        
        print(f"File update statistics: {stats}")
    except Exception as e:
        print(f"Error loading from file: {e}")
    
    # Now use rt_tt for routing with real-time data
    print("\nExecuting routing with real-time data...")
    
    # Create query (similar to basic example)
    query = ng.Query()
    # ... configure query ...
    
    # Route with real-time data
    # journeys = ng.route_with_rt(timetable, rt_tt, query)

if __name__ == "__main__":
    main()
