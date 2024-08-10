import decimal
import math
from typing import Optional

EARTH_RADIUS_NM = 3440.1
NM_TO_KM = 1.852


class Store:
    """This is a domain class that provides relevant
    domain logic. In this case it is a place to put
    logic that determines if the store is within distance
    from a given lat and long."""

    def __init__(
        self,
        name: str,
        postcode: str,
        lat: Optional[decimal.Decimal] = None,
        long: Optional[decimal.Decimal] = None,
    ):
        self.name = name
        self.postcode = postcode
        self.lat = lat
        self.long = long

    def is_within_radius(
        self,
        query_lat,
        query_long,
        radius_km,
    ):
        if not self.lat or not self.long:
            return False

        if radius_km < 0:
            raise ValueError("radius_km cannot be negative.")

        dist_km = self.distance_km_from(query_lat, query_long)
        return dist_km <= radius_km

    def distance_km_from(self, compare_lat, compare_long):
        """Exposing this as a public method as it could be
        useful later, i.e, to display how far away"""
        return self._haversine_km_from_deg(
            self.lat,
            self.long,
            compare_lat,
            compare_long,
        )

    def _haversine_nm_from_deg(self, lat_a, long_a, lat_b, long_b):
        """Using haversine formula under the hood to calculate
        distance between 2 points on earth. This makes it easier
        to change later if needed. If we really don't want to open
        up this code again then we should inject the calculation
        strategy into this class, but making this into a private
        method would suffice and keep things simple."""

        long_a_rad, lat_a_rad, long_b_rad, lat_b_rad = map(
            math.radians, [long_a, lat_a, long_b, lat_b]
        )

        return EARTH_RADIUS_NM * math.acos(
            (math.sin(lat_a_rad) * math.sin(lat_b_rad))
            + math.cos(lat_a_rad)
            * math.cos(lat_b_rad)
            * math.cos(long_a_rad - long_b_rad)
        )

    def _haversine_km_from_deg(self, lat_a, long_a, lat_b, long_b):
        """Using haversine formula under the hood to calculate
        distance between 2 points on earth. This makes it easier
        to change later if needed. If we really don't want to open
        up this code again then we should inject the calculation
        strategy into this class, but making this into a private
        method would suffice and keep things simple."""

        return (
            self._haversine_nm_from_deg(
                lat_a,
                long_a,
                lat_b,
                long_b,
            )
            * NM_TO_KM
        )
