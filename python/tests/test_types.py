"""
Unit tests for pynigiri types.
"""
import pytest
import pynigiri as ng


def test_location_idx():
    """Test LocationIdx creation and operations."""
    idx1 = ng.LocationIdx(42)
    idx2 = ng.LocationIdx(42)
    idx3 = ng.LocationIdx(100)
    
    assert int(idx1) == 42
    assert idx1 == idx2
    assert idx1 != idx3
    assert idx1 < idx3
    assert "LocationIdx(42)" in repr(idx1)


def test_duration():
    """Test Duration creation and operations."""
    d1 = ng.Duration(30)
    d2 = ng.Duration(45)
    
    assert d1.count() == 30
    assert int(d1) == 30
    assert d1 < d2
    assert "Duration(30" in repr(d1)


def test_unixtime():
    """Test UnixTime creation and operations."""
    t1 = ng.UnixTime(1000000)
    t2 = ng.UnixTime(2000000)
    
    assert t1.count() == 1000000
    assert int(t1) == 1000000
    assert t1 < t2
    assert t1 != t2


def test_location_id():
    """Test LocationId creation."""
    src = ng.SourceIdx(0)
    loc_id = ng.LocationId(src, "STATION_123")
    
    assert loc_id.src == src
    assert loc_id.id == "STATION_123"
    assert "STATION_123" in repr(loc_id)


def test_footpath():
    """Test Footpath creation."""
    target = ng.LocationIdx(10)
    duration = ng.Duration(5)
    fp = ng.Footpath(target, duration)
    
    assert fp.target == target
    assert fp.duration == duration


def test_time_interval():
    """Test TimeInterval creation."""
    t1 = ng.UnixTime(1000)
    t2 = ng.UnixTime(2000)
    interval = ng.TimeInterval(t1, t2)
    
    assert interval.from_ == t1
    assert interval.to_ == t2
    
    t_mid = ng.UnixTime(1500)
    assert interval.contains(t_mid)


def test_enums():
    """Test enum values."""
    # Test Clasz enum
    assert ng.Clasz.BUS is not None
    assert ng.Clasz.TRAM is not None
    assert ng.Clasz.METRO is not None
    
    # Test LocationType enum
    assert ng.LocationType.STOP is not None
    assert ng.LocationType.STATION is not None
    
    # Test EventType enum
    assert ng.EventType.DEP is not None
    assert ng.EventType.ARR is not None
    
    # Test Direction enum
    assert ng.Direction.FORWARD is not None
    assert ng.Direction.BACKWARD is not None


def test_latlng():
    """Test LatLng creation."""
    coords = ng.LatLng(52.5200, 13.4050)  # Berlin
    
    assert coords.lat == 52.5200
    assert coords.lng == 13.4050
    assert "52.52" in repr(coords)
    
    coords2 = ng.LatLng(52.5200, 13.4050)
    assert coords == coords2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
