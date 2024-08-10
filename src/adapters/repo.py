import abc
import json

import requests


class AbstractStoreRepo(abc.ABC):
    """The list of stores is conveniently provided in a stores.json file.
    However, this may not always be the case and we need to ensure that
    we can easily swap out store.json for another store such as a database
    when the time comes. The proposed approach is to use Repository Pattern
    to abstract away the concrete store that is being used. This way, we
    can easily swap out one concrete store for another and the calling code
    would not need any knowledge of it. Furthermore, the ability to easily
    swap out concrete implementations will make our code easier to test.

    In classic OOP the Repository Pattern is implemented by defining an
    Abstract Repository that provides the abstract methods for data access.
    We then subclass and implement the abstract methods. In Python, you can
    achieve the same effect by duck typing, however I'd go with the OOP
    style as this is an important pattern that defines our architecture so
    we should be formal and explicit about the pattern in use.

    What should the repository return? It is easy to convert the contents
    if the file into a standard python dict, but is this to correct approach
    given an alternative is to reconstitute a domain model representation
    from the data? The argument for returning as dict is that the data will
    be retrieved for read only purposes. We do not need to have any business
    logic at this stage so a domain model representation will complicate
    things. Dict it is!"""

    @abc.abstractmethod
    def list(self) -> list:
        raise NotImplementedError


class StoreFileRepo(AbstractStoreRepo):
    def __init__(self, store_file_path: str):
        self.store_file_path: str = store_file_path

    def list(self) -> list:
        with open(self.store_file_path, encoding="utf-8") as f:
            return json.load(f)


class AbstractStorePostcodeRepo(abc.ABC):
    @abc.abstractmethod
    def postcode_to_coords_map(
        self,
        postcodes: list[str],
    ) -> dict:
        raise NotImplementedError


class PostcodesIORepo(AbstractStorePostcodeRepo):
    def __init__(self, bulk_postcodes_url: str, timeout=10):
        self.bulk_postcodes_url: str = bulk_postcodes_url
        self.timeout = timeout

    def postcode_to_coords_map(
        self,
        postcodes: list[str],
    ) -> dict:
        # Call postcodes.io api for lat and long
        # of all stores.
        res = requests.post(
            self.bulk_postcodes_url,
            data={"postcodes": postcodes},
            timeout=self.timeout,
        )

        # Map postcodes to their coords.
        entries = res.json()["result"]
        return {
            e["query"]: {
                "lat": e["result"]["latitude"],
                "long": e["result"]["longitude"],
            }
            for e in entries
            if e["result"]
        }
