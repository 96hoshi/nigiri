"""
Unit tests for pynigiri routing functionality.
"""
import pytest
import pynigiri as ng


def test_offset():
    """Test Offset creation."""
    target = ng.LocationIdx(10)
    duration = ng.Duration(5)
    mode = ng.TransportModeId(0)
    
    offset = ng.Offset(target, duration, mode)
    
    assert offset.target() == target
    assert offset.duration() == duration
    assert offset.type() == mode


def test_td_offset():
    """Test TdOffset creation."""
    offset = ng.TdOffset()
    offset.duration = ng.Duration(10)
    
    assert offset.duration.count() == 10


def test_via_stop():
    """Test ViaStop creation."""
    via = ng.ViaStop()
    via.location = ng.LocationIdx(5)
    via.stay = ng.Duration(10)
    
    assert via.location == ng.LocationIdx(5)
    assert via.stay.count() == 10


def test_location_match_mode():
    """Test LocationMatchMode enum."""
    assert ng.LocationMatchMode.EXACT is not None
    assert ng.LocationMatchMode.EQUIVALENT is not None
    assert ng.LocationMatchMode.CHILD is not None


def test_transfer_time_settings():
    """Test TransferTimeSettings creation."""
    settings = ng.TransferTimeSettings()
    assert settings is not None
    
    settings.default_transfer_time = ng.Duration(2)
    assert settings.default_transfer_time.count() == 2


def test_query_creation():
    """Test Query creation and configuration."""
    query = ng.Query()
    assert query is not None
    
    # Set basic properties
    query.max_transfers = 3
    query.max_travel_time = ng.Duration(120)
    query.require_bike_transport = True
    query.slow_direct = False
    
    assert query.max_transfers == 3
    assert query.max_travel_time.count() == 120
    assert query.require_bike_transport == True
    assert query.slow_direct == False


def test_query_with_offsets():
    """Test Query with start and destination offsets."""
    query = ng.Query()
    
    start = ng.Offset(ng.LocationIdx(1), ng.Duration(0), ng.TransportModeId(0))
    dest = ng.Offset(ng.LocationIdx(2), ng.Duration(0), ng.TransportModeId(0))
    
    query.start = [start]
    query.destination = [dest]
    
    assert len(query.start) == 1
    assert len(query.destination) == 1


def test_query_with_via_stops():
    """Test Query with via stops."""
    query = ng.Query()
    
    via = ng.ViaStop()
    via.location = ng.LocationIdx(5)
    via.stay = ng.Duration(5)
    
    query.via_stops = [via]
    
    assert len(query.via_stops) == 1
    assert query.via_stops[0].location == ng.LocationIdx(5)


def test_journey_creation():
    """Test Journey creation."""
    journey = ng.Journey()
    assert journey is not None
    assert len(journey.legs) == 0


# Note: Full routing test would require a loaded timetable
# The following test is commented out as it requires real data

# def test_routing():
#     """Test routing (requires loaded timetable)."""
#     # Load timetable...
#     # timetable = ...
#     
#     query = ng.Query()
#     # Configure query...
#     
#     journeys = ng.route(timetable, query)
#     assert isinstance(journeys, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
