"""Domain entities should not create or reconstitute
themselves. For example, there may be different
domain logic around the creation of domain entities,
that need to be applied from the outside.
We could put creation logic at the service layer,
but that means the service layer itself will need
to have domain logic if there were any.
The approach is to use a domain factory, whose job is
to create or reconstitute domain entities. This
This factory will understand domain logic and honour
them in the creation.

In this particular case the is hardly any domain
logic around creation, but establishing a factory now
establishes a pattern we can use moving forward.

We don't need to use a class for this, just a function."""

import decimal
from typing import Optional

from src.domain.store import Store


def create_store(
    name: str,
    postcode: str,
    lat: Optional[decimal.Decimal] = None,
    long: Optional[decimal.Decimal] = None,
):
    return Store(name, postcode, lat, long)
