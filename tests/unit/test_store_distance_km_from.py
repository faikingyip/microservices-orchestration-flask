"""These unit tests are not concerned with data access.
They test only the logic of domain entities irrespective
of the data sources."""

# Distance correct from different coordinates in different hemispheres

from src.domain.store import Store

# We can put these mappings in a different file
# if they become larger or are used more extensively.
COORDS_BY_HEMSIPHERE = {
    "NW": {"lat": 45.000000, "long": -120.000000},
    "NE": {"lat": 45.000000, "long": 30.000000},
    "SW": {"lat": -45.000000, "long": -120.000000},
    "SE": {"lat": -45.000000, "long": 120.000000},
    "N": {"lat": 45.000000, "long": 0.000000},
    "S": {"lat": -45.000000, "long": 0.000000},
    "W": {"lat": 0.000000, "long": -120.000000},
    "E": {"lat": 0.000000, "long": 120.000000},
    "NW2": {"lat": 50.000000, "long": -160.000000},
    "NE2": {"lat": 25.000000, "long": 10.000000},
    "SW2": {"lat": -25.000000, "long": -90.000000},
    "SE2": {"lat": -25.000000, "long": 110.000000},
    "N2": {"lat": 42.000000, "long": 0.000000},
    "S2": {"lat": -41.000000, "long": 0.000000},
    "W2": {"lat": 0.000000, "long": -128.000000},
    "E2": {"lat": 0.000000, "long": 126.000000},
    "0": {"lat": 0.000000, "long": 0.000000},
}

# These are expected distances that should be
# outputted by our method that calculates distance
# between 2 coordinates. The expected distances
# were taken from various only sites that calculate
# distances using the Haversine formula.
# We can add more expected distances if required.
# We can put these mappings in a different file
# if they become larger or are used more extensively.
EXPT_COORDS_DIST = {
    "NW_NW": 0,
    "NW_NE": 9580.5,
    "NW_SW": 10007.6,
    "NW_SE": 15410.6,
    "NW_N": 8397.7,
    "NW_S": 15410.6,
    "NW_W": 5003.8,
    "NW_E": 12309.8,
    "NW_NW2": 3018.4,
    "NW_NE2": 10729.7,
    "NW_SW2": 8357.2,
    "NW_SE2": 15044.4,
    "NW_N2": 8657,
    "NW_S2": 15227.9,
    "NW_W2": 5065.5,
    "NW_E2": 11866.1,
    "NW_0": 12309.8,
    "SE_NW": 15410.6,
    "SE_NE": 13343.4,
    "SE_SW": 0,
    "SE_SE": 0,
    "SE_N": 15410.6,
    "SE_S": 8397.7,
    "SE_W": 12309.8,
    "SE_E": 5003.8,
    "SE_NW2": 13072.6,
    "SE_NE2": 13476.8,
    "SE_SW2": 11658,
    "SE_SE2": 2398.7,
    "SE_N2": 15276.2,
    "SE_S2": 8743.7,
    "SE_W2": 11715.5,
    "SE_E2": 5038.6,
    "SE_0": 12309.8,
}


def dist_correct_from_different_coords_in_different_hemispheres():
    """Distance correct from different coordinates in different hemispheres"""
    hemispheres = [key for key in COORDS_BY_HEMSIPHERE]
    for hem in hemispheres:

        store = Store(
            "Store 1",
            "Postcode 1",
            COORDS_BY_HEMSIPHERE[hem].get("lat"),
            COORDS_BY_HEMSIPHERE[hem].get("long"),
        )

        # Compare each entry with each other.
        for hem_2 in hemispheres:
            if hem == hem_2:
                continue

            dist = store.distance_km_from(
                COORDS_BY_HEMSIPHERE[hem_2].get("lat"),
                COORDS_BY_HEMSIPHERE[hem_2].get("long"),
            )

            if exp_dist := EXPT_COORDS_DIST.get(f"{hem}_{hem_2}"):
                # Accounts for slight variation in results.
                assert abs(exp_dist - dist) <= 0.2
