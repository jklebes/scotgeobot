from .context import calcGeohashes

def test_emptyrequest():
    """Query is empty list - expect output is empty dict"""
    # TODO how to assert empty dict/set
    assert(calcGeohashes.geohashes([]) is None)

def test_uniformity():
    """query is various graticules positive and negative but all east of -30: 
    expect output has same after-decimal digits everywhere"""
    pass

def test_zerolong():
    """expected behaviour at graticules with longitude 0"""
    pass

def test_zerolat():
    """expected behaviour at graticules with latitude 0"""
    pass

def test_noconnection():
    """desired behavior when internet it not reachable or carabiner.peeron.com is down"""
    pass


