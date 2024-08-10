from typing import Protocol

from src import config
from src.adapters import repo


class StoreRepoFactory(Protocol):
    def create_store_repo(self) -> repo.AbstractStoreRepo:
        raise NotImplementedError()

    def create_store_postcode_repo(self) -> repo.AbstractStorePostcodeRepo:
        raise NotImplementedError()


class DefaultStoreRepoFactory(StoreRepoFactory):
    def create_store_repo(self) -> repo.AbstractStoreRepo:
        return repo.StoreFileRepo(config.STORES_FILE)

    def create_store_postcode_repo(self) -> repo.AbstractStorePostcodeRepo:
        return repo.PostcodesIORepo(config.POSTCODESIO_BULK_POSTCODES_URL)
