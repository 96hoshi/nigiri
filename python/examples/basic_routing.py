"""
Basic example: Load GTFS data and perform routing.
"""

import pynigiri as ng
from datetime import date, datetime, timedelta
from const import GTFS_PATH, STATION_ID_A, STATION_ID_B

def main():
    print("Loading timetable...")
    
    # Configure data source
    sources = [
        ng.TimetableSource(
            tag="my_gtfs",
            path=str(GTFS_PATH),  # Update with your GTFS path
            config=ng.LoaderConfig()
        )
    ]
    
    # Load timetable for date range, date format "YYYY-MM-DD"
    # Use current year for routing
    current_year = date.today().year
    timetable = ng.load_timetable(
        sources=sources,
        start_date=f"{current_year}-01-01",
        end_date=f"{current_year}-12-31"
    )
    
    print(f"Loaded timetable: {timetable}")
    print(f"Number of locations: {timetable.n_locations()}")
    print(f"Number of routes: {timetable.n_routes()}")
    print(f"Date range: {current_year}-01-01 to {current_year}-12-31")
    
    # Find locations
    # Note: Replace these with actual location IDs from your GTFS data
    start_loc_id = timetable.find_location(STATION_ID_A) # Example: Hamburg Hbf ID
    dest_loc_id = timetable.find_location(STATION_ID_B) # Example: Berlin Hbf ID
    
    if start_loc_id is None or dest_loc_id is None:
        print("Error: Could not find one or both locations")
        return
    
    print(f"\nStart: {timetable.get_location_name(start_loc_id)}")
    print(f"Destination: {timetable.get_location_name(dest_loc_id)}")
    
    # Create routing query
    query = ng.Query()
    
    # Convert timestamp to minutes since epoch (bindings expect minutes, not seconds)
    # Use a date that matches the timetable date range
    query_time = datetime(current_year, 1, 15, 10, 0, 0)
    query.start_time = int(query_time.timestamp()) // 60
    
    # Set matching modes
    query.start_match_mode = ng.LocationMatchMode.EQUIVALENT
    query.dest_match_mode = ng.LocationMatchMode.EQUIVALENT
    
    # Set start and destination with offsets (0 offset, any transport mode)
    query.start = [ng.Offset(start_loc_id, timedelta(0), 0)]
    query.destination = [ng.Offset(dest_loc_id, timedelta(0), 0)]
    
    # Set routing parameters
    query.max_transfers = 6
    query.min_connection_count = 1
    query.max_travel_time = timedelta(hours=10)  # Hamburg-Berlin takes ~2 hours
    
    print(f"\nQuery details:")
    print(f"  Start time: {query_time}")
    print(f"  Max transfers: {query.max_transfers}")
    print(f"  Max travel time: {query.max_travel_time}")
    
    print(f"\nExecuting routing query...")
    journeys = ng.route(timetable, query)
    
    print(f"Found {len(journeys)} journey(s)")
    
    # Print results
    for i, journey in enumerate(journeys, 1):
        print(f"\n--- Journey {i} ---")
        
        # Note: journey times may show as 1970 dates due to datetime conversion issues in bindings
        # The routing is working correctly, but displaying the actual time requires workarounds
        print(f"Transfers: {journey.transfers}")
        print(f"Number of legs: {len(journey)}")
        
        for j, leg in enumerate(journey.legs, 1):
            # Use getattr() to access 'from' which is a Python keyword
            from_loc = getattr(leg, 'from')
            to_loc = leg.to
            from_name = timetable.get_location_name(from_loc)
            to_name = timetable.get_location_name(to_loc)
            
            print(f"  Leg {j}: {from_name} -> {to_name}")

if __name__ == "__main__":
    main()
