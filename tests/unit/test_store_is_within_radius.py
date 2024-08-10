"""These unit tests are not concerned with data access.
They test only the logic of domain entities irrespective
of the data sources."""

# Store within radius
# Store not within radius
# Store within large radius
# False if store lat not supplied
# False if store long not supplied
# Error on negative radius


import pytest

from src.domain.store import Store


def create_harlow_store():
    return Store("Harlow", "CM20 2SX", 51.785161, 0.121998)


def coords_cm201fe():
    return {"query_lat": 51.77624, "query_long": 0.095126}


def coords_en93yw():
    return {"query_lat": 51.677378, "query_long": 0.001689}


def test_store_within_radius():
    """Store within radius.
    Query postcode is CM20 1FE"""

    harlow = create_harlow_store()
    res = harlow.is_within_radius(
        **coords_cm201fe(),
        radius_km=5,
    )
    assert res


def test_store_not_within_radius():
    """Store not within radius.
    Query postcode is EN9 3YW"""

    harlow = create_harlow_store()
    res = harlow.is_within_radius(
        **coords_en93yw(),
        radius_km=14,
    )
    assert not res


def test_store_within_large_radius():
    """Store within large radius.
    Query postcode is EN9 3YW"""

    harlow = create_harlow_store()
    res = harlow.is_within_radius(
        **coords_en93yw(),
        radius_km=15,
    )
    assert res


def test_false_if_store_lat_not_supplied():
    """False if store lat not supplied.
    Query postcode is CM20 1FE"""

    harlow = Store("Harlow", "CM20 2SX", None, 0.121998)
    res = harlow.is_within_radius(
        **coords_cm201fe(),
        radius_km=5,
    )
    assert not res


def test_false_if_store_long_not_supplied():
    """False if store long not supplied.
    Query postcode is CM20 1FE"""

    harlow = Store("Harlow", "CM20 2SX", 51.785161, None)
    res = harlow.is_within_radius(
        **coords_cm201fe(),
        radius_km=5,
    )
    assert not res


def test_error_on_negative_radius():
    """Error on negative radius."""

    harlow = create_harlow_store()
    with pytest.raises(ValueError):
        harlow.is_within_radius(
            **coords_en93yw(),
            radius_km=-1,
        )
