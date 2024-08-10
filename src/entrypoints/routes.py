from flask import render_template

from src import constants
from src.adapters.factory import StoreRepoFactory
from src.app import app
from src.srv_layer import views


@app.route("/")
def stores():
    store_repo_factory: StoreRepoFactory = app.config[constants.STORE_REPO_FACTORY]
    return render_template(
        "index.html",
        stores=views.stores(
            store_repo_factory(),
        ),
    )


@app.route("/nearby/")
def nearby_stores():
    store_repo_factory: StoreRepoFactory = app.config[constants.STORE_REPO_FACTORY]
    return render_template(
        "index.html",
        stores=views.nearby_stores(
            store_repo_factory(),
            "CM20 1FE",
            30,
        ),
    )
