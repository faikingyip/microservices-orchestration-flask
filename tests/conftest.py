import json

import pytest

from src import config, constants
from src.adapters import repo
from src.adapters.factory import DefaultStoreRepoFactory, StoreRepoFactory
from src.app import app as flask_app
from src.entrypoints import routes

_ = routes


class FakeStorePostcodesIORepo(repo.AbstractStorePostcodeRepo):
    def __init__(
        self,
        test_store_postcodes_file_path: str,
    ):
        self.test_store_postcodes_file_path = test_store_postcodes_file_path

    def postcode_to_coords_map(
        self,
        postcodes,
    ):
        _ = postcodes

        # Map postcodes to their coords.
        with open(self.test_store_postcodes_file_path, encoding="utf-8") as f:
            entries = json.load(f)["result"]

        return {
            e["query"]: {
                "lat": e["result"]["latitude"],
                "long": e["result"]["longitude"],
            }
            for e in entries
            if e["result"]
        }


class FakeStoreRepoFactory(StoreRepoFactory):
    def create_store_repo(self) -> repo.AbstractStoreRepo:
        return repo.StoreFileRepo(config.STORES_FILE)

    def create_store_postcode_repo(self) -> repo.AbstractStorePostcodeRepo:
        return FakeStorePostcodesIORepo(
            config.TEST_STORE_POSTCODES_FILE,
        )


@pytest.fixture
def e2e_app():
    flask_app.config.update(
        {
            "TESTING": True,
            "TEMPLATES_AUTO_RELOAD": True,
            "template_folder": "entrypoints/templates",
        },
    )

    flask_app.config[constants.STORE_REPO_FACTORY] = DefaultStoreRepoFactory

    yield flask_app


@pytest.fixture
def integrations_app():
    flask_app.config.update(
        {
            "TESTING": True,
            "TEMPLATES_AUTO_RELOAD": True,
            "template_folder": "entrypoints/templates",
        },
    )

    flask_app.config[constants.STORE_REPO_FACTORY] = FakeStoreRepoFactory

    yield flask_app


@pytest.fixture
def integrations_client(integrations_app):
    return integrations_app.test_client()


@pytest.fixture
def e2e_client(e2e_app):
    return e2e_app.test_client()
