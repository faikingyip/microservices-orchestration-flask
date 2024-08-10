"""We need logic to aggregate lat and long data with the corresponding
stores, but where should we put this logic? Ideally we want all data
access to be abstracted away from the calling code. We could put this
logic into the repository, but that would increase the responsibility
of the repository since it would now be pulling data from the store
file as well as data from Postcodes.io. I would rule this out as the
guiding factor is to ensure maximum testability of code. A less
intrusive approach is to create another repository to retrieve the lat
and long information for the stores. This new repostory will use an
api client under the hood to retrieve the data. Still, we want to
abstract away the detail so the calling code doesn't need to know 2
repositories are at play. So the approach is to create a view, whose
responsibility is to aggregate and provide the requested data to the
calling code. I categorize this views module as part of a servicing
layer to the calling code and will create a srv_layer folder with
a views.py file inside.

Service layer objects are intended to make it simple for our higher
level code (i.e. routes) to call."""

from src.adapters.factory import StoreRepoFactory
from src.domain import factory


def _aggregate_coords(stores: list, postcode_coords_map: dict):
    for s in stores:
        if coords := postcode_coords_map.get(s["postcode"]):
            s["lat"], s["long"] = coords["lat"], coords["long"]


def stores(
    store_repo_factory: StoreRepoFactory,
):

    store_repo = store_repo_factory.create_store_repo()
    store_postcode_repo = store_repo_factory.create_store_postcode_repo()

    stores = store_repo.list()

    postcode_coords_map = store_postcode_repo.postcode_to_coords_map(
        [s["postcode"] for s in stores],
    )

    _aggregate_coords(stores, postcode_coords_map)

    return sorted(
        stores,
        key=lambda x: x["name"],
    )


def nearby_stores(
    store_repo_factory: StoreRepoFactory,
    postcode,
    radius_km,
):
    """We won't call stores, which seems like a convenience. Instead
    we have the opportunity to make only 1 call to Postcodes.io instead of 2.
    We do this by including the supplied postcode into the call to get the
    lat and long for the stores."""

    store_repo = store_repo_factory.create_store_repo()
    store_postcode_repo = store_repo_factory.create_store_postcode_repo()

    stores = store_repo.list()

    postcode_coords_map = store_postcode_repo.postcode_to_coords_map(
        [s["postcode"] for s in stores] + [postcode],
    )

    _aggregate_coords(stores, postcode_coords_map)

    if query_coords := postcode_coords_map.get(postcode):
        query_lat, query_long = query_coords["lat"], query_coords["long"]

    stores_within_radius = []
    for s in stores:
        store = factory.create_store(
            s["name"],
            s["postcode"],
            s.get("lat", None),
            s.get("long", None),
        )
        if store.is_within_radius(query_lat, query_long, radius_km):
            stores_within_radius.append(s)

    return sorted(
        stores_within_radius,
        key=lambda x: x["lat"],
        reverse=True,
    )
