"""The integrations test will use the FakePostcodesIORepo to 
pull the postcodes data from test_store_postcodes.json
instead of making actual calls to the postcodesio api.
This file will also include some additional postcodes for
querying nearby stores."""

# Nearby stores sorted from North to South


from src.srv_layer import views
from tests.conftest import FakeStoreRepoFactory


def query_enfield_postcode():
    return "EN9 3YW"


def query_harlow_postcode():
    return "CM20 1FE"


def test_nearby_stores_sorted_from_north_to_south():
    """Nearby stores sorted from North to South."""

    store_repo_factory = FakeStoreRepoFactory()

    stores = views.nearby_stores(
        store_repo_factory,
        postcode=query_harlow_postcode(),
        radius_km=30,
    )

    # Lat and long must both be present for all.
    assert all(s.get("lat") and s.get("long") for s in stores)

    # The lat should be ordered from greatest to smallest.
    assert all(
        stores[i].get("lat") >= stores[i + 1].get("lat") for i in range(len(stores) - 1)
    )
