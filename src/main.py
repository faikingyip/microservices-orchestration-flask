from src import constants
from src.adapters.factory import DefaultStoreRepoFactory
from src.app import app
from src.entrypoints import routes

_ = app, routes


app.config[constants.STORE_REPO_FACTORY] = DefaultStoreRepoFactory
