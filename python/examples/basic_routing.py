"""
Basic example: Load GTFS data and perform routing.
"""
import sys
sys.path.insert(0, 'build/python')

import pynigiri as ng
from datetime import datetime

def main():
    print("Loading timetable...")
    
    # Configure data source
    sources = [
        ng.TimetableSource(
            tag="my_gtfs",
            path="path/to/gtfs",  # Update with your GTFS path
            config=ng.LoaderConfig()
        )
    ]
    
    # Load timetable for date range
    timetable = ng.load_timetable(
        sources=sources,
        start_date="2024-01-01",
        end_date="2024-12-31"
    )
    
    print(f"Loaded timetable: {timetable}")
    print(f"Number of locations: {timetable.n_locations()}")
    print(f"Number of routes: {timetable.n_routes()}")
    
    # Find locations
    # Note: Replace these with actual location IDs from your GTFS data
    start_loc_id = timetable.find_location("STATION_A_ID")
    dest_loc_id = timetable.find_location("STATION_B_ID")
    
    if start_loc_id is None or dest_loc_id is None:
        print("Error: Could not find one or both locations")
        return
    
    print(f"\nStart: {timetable.get_location_name(start_loc_id)}")
    print(f"Destination: {timetable.get_location_name(dest_loc_id)}")
    
    # Create routing query
    query = ng.Query()
    
    # Set start time (Unix timestamp)
    query_time = ng.UnixTime(int(datetime(2024, 6, 1, 8, 0).timestamp()))
    query.start_time = query_time
    
    # Set start and destination with offsets
    query.start = [ng.Offset(start_loc_id, ng.Duration(0), ng.TransportModeId(0))]
    query.destination = [ng.Offset(dest_loc_id, ng.Duration(0), ng.TransportModeId(0))]
    
    # Set routing parameters
    query.max_transfers = 3
    query.max_travel_time = ng.Duration(120)  # 120 minutes
    
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
