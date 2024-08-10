"""The integrations test will use the FakePostcodesIORepo to 
pull the postcodes data from test_store_postcodes.json
instead of making actual calls to the postcodesio api."""

# Retrieve returns lat and long for all stores - ALWAYS FAIL
# Retrieve returns lat and long for most stores

from src import config
from src.srv_layer import views
from tests.conftest import FakeStoreRepoFactory

# Turns out that lat and long cannot be determined for
# some postcodes, so this test will always fail for
# our stores dataset.
# def test_bulk_returns_lat_and_long_for_all_stores():
#     """Retrieve returns lat and long for all stores"""

#     store_repo = StoreFileRepo(config.STORES_FILE)

#     stores = views.stores(
#         store_repo,
#         config.POSTCODESIO_BULK_POSTCODES_URL,
#     )

#     print(stores)
#     assert all(s.get("lat") for s in stores)


def test_bulk_returns_lat_and_long_for_most_stores2():
    """Retrieve returns lat and long for most stores.
    A expected % success should be confirmed with
    with the business."""

    store_repo_factory = FakeStoreRepoFactory()
    stores = views.stores(store_repo_factory)

    # Some may not have a lat and long as it wasn't
    # determined at source.
    assert any(s.get("lat") for s in stores)
    assert any(s.get("long") for s in stores)

    # Lat an long must both be present or not at all.
    assert all(s.get("lat") for s in stores if s.get("long"))
    assert all(s.get("long") for s in stores if s.get("lat"))

    # At least X% will have lat and long.
    assert (
        sum(1 for s in stores if s.get("lat")) / len(stores)
        >= config.POSTCODESIO_BULK_POSTCODES_SUCCESS_RATE
    )
