"""
Basic example: Load GTFS data and perform routing.
"""

import pynigiri as ng
from datetime import date, datetime, timezone , timedelta
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
    
    # Load timetable for date range
    timetable = ng.load_timetable(
        sources=sources,
        start_date=date.today().isoformat(),
        end_date=date.today().isoformat()
    )
    
    print(f"Loaded timetable: {timetable}")
    print(f"Number of locations: {timetable.n_locations()}")
    print(f"Number of routes: {timetable.n_routes()}")
    
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
    
    # Set start time (use datetime object directly)
    query.start_time = datetime.now(timezone.utc)
    
    # Set matching modes
    query.start_match_mode = ng.LocationMatchMode.EQUIVALENT
    query.dest_match_mode = ng.LocationMatchMode.EQUIVALENT
    
    # Set start and destination with offsets (0 offset, any transport mode)
    query.start = [ng.Offset(start_loc_id, timedelta(0), ng.TransportModeId(0))]
    query.destination = [ng.Offset(dest_loc_id, timedelta(0), ng.TransportModeId(0))]
    
    # Set routing parameters
    query.max_transfers = 6
    query.min_connection_count = 1
    query.max_travel_time = timedelta(hours=10)  # Hamburg-Berlin takes ~2 hours
    
    print(f"\nQuery details:")
    print(f"  Start time: {query.start_time}")
    print(f"  Max transfers: {query.max_transfers}")
    print(f"  Max travel time: {query.max_travel_time}")
    
    print(f"\nExecuting routing query...")
    journeys = ng.route(timetable, query)
    
    print(f"Found {len(journeys)} journey(s)")
    
    # Print results
    for i, journey in enumerate(journeys, 1):
        print(f"\n--- Journey {i} ---")
        print(f"Departure: {datetime.fromtimestamp(journey.departure_time().__int__())}")
        print(f"Arrival: {datetime.fromtimestamp(journey.arrival_time().__int__())}")
        print(f"Travel time: {journey.travel_time().count()} minutes")
        print(f"Transfers: {journey.transfers}")
        print(f"Number of legs: {len(journey)}")
        
        for j, leg in enumerate(journey.legs, 1):
            dep_time = datetime.fromtimestamp(leg.dep_time.__int__())
            arr_time = datetime.fromtimestamp(leg.arr_time.__int__())
            from_name = timetable.get_location_name(leg.from_)
            to_name = timetable.get_location_name(leg.to_)
            
            print(f"  Leg {j}: {from_name} -> {to_name}")
            print(f"         {dep_time.strftime('%H:%M')} -> {arr_time.strftime('%H:%M')}")

if __name__ == "__main__":
    main()
