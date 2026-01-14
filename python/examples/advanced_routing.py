"""
Advanced routing example: Using advanced query features.
"""
import sys
sys.path.insert(0, 'build/python')

import pynigiri as ng
from datetime import datetime, timedelta

def main():
    # Load timetable (as in basic example)
    sources = [ng.TimetableSource("my_gtfs", "path/to/gtfs")]
    timetable = ng.load_timetable(sources, "2024-01-01", "2024-12-31")
    
    print("=== Advanced Routing Examples ===\n")
    
    # Example 1: Routing with via stops
    print("1. Routing with intermediate stops (via):")
    query = ng.Query()
    
    start_loc = timetable.find_location("STATION_A")
    via_loc = timetable.find_location("STATION_B")
    dest_loc = timetable.find_location("STATION_C")
    
    if all([start_loc, via_loc, dest_loc]):
        query.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
        query.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
        
        # Add via stop with 10 minute minimum stay
        query.via_stops = [ng.ViaStop()]
        query.via_stops[0].location = via_loc
        query.via_stops[0].stay = ng.Duration(10)
        
        query.start_time = ng.UnixTime(int(datetime.now().timestamp()))
        query.max_transfers = 5
        
        journeys = ng.route(timetable, query)
        print(f"   Found {len(journeys)} journeys with via stop\n")
    
    # Example 2: Time interval search
    print("2. Search within time interval:")
    query2 = ng.Query()
    
    if start_loc and dest_loc:
        now = int(datetime.now().timestamp())
        later = int((datetime.now() + timedelta(hours=2)).timestamp())
        
        # Create time interval
        time_interval = ng.TimeInterval(
            ng.UnixTime(now),
            ng.UnixTime(later)
        )
        query2.start_time = time_interval
        
        query2.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
        query2.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
        query2.max_transfers = 3
        
        journeys = ng.route(timetable, query2)
        print(f"   Found {len(journeys)} journeys in time window\n")
    
    # Example 3: Class filtering (e.g., only buses and trams)
    print("3. Routing with transport class filter:")
    query3 = ng.Query()
    
    if start_loc and dest_loc:
        query3.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
        query3.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
        query3.start_time = ng.UnixTime(int(datetime.now().timestamp()))
        
        # Filter to only use buses and trams
        # Note: You'll need to construct the appropriate clasz mask
        # query3.allowed_claszes = custom_mask
        
        query3.max_transfers = 3
        
        journeys = ng.route(timetable, query3)
        print(f"   Found {len(journeys)} journeys with class filter\n")
    
    # Example 4: Bicycle transport required
    print("4. Routing requiring bicycle transport:")
    query4 = ng.Query()
    
    if start_loc and dest_loc:
        query4.start = [ng.Offset(start_loc, ng.Duration(0), ng.TransportModeId(0))]
        query4.destination = [ng.Offset(dest_loc, ng.Duration(0), ng.TransportModeId(0))]
        query4.start_time = ng.UnixTime(int(datetime.now().timestamp()))
        query4.require_bike_transport = True
        query4.max_transfers = 3
        
        journeys = ng.route(timetable, query4)
        print(f"   Found {len(journeys)} journeys with bike transport\n")
    
    # Example 5: Multiple start/destination points
    print("5. Routing with multiple start/destination points:")
    query5 = ng.Query()
    
    start_a = timetable.find_location("STATION_A")
    start_b = timetable.find_location("STATION_B")
    dest_a = timetable.find_location("STATION_C")
    dest_b = timetable.find_location("STATION_D")
    
    if all([start_a, start_b, dest_a, dest_b]):
        # Multiple start points
        query5.start = [
            ng.Offset(start_a, ng.Duration(0), ng.TransportModeId(0)),
            ng.Offset(start_b, ng.Duration(5), ng.TransportModeId(1))  # 5 min walk
        ]
        
        # Multiple destination points
        query5.destination = [
            ng.Offset(dest_a, ng.Duration(0), ng.TransportModeId(0)),
            ng.Offset(dest_b, ng.Duration(3), ng.TransportModeId(1))  # 3 min walk
        ]
        
        query5.start_time = ng.UnixTime(int(datetime.now().timestamp()))
        query5.max_transfers = 3
        
        journeys = ng.route(timetable, query5)
        print(f"   Found {len(journeys)} journeys with multiple points\n")

if __name__ == "__main__":
    main()
