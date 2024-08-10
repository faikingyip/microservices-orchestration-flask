"""This is the configuration for the application. A better practice is to
set these in environment variables and source values from there. These environment
variables can be set within docker or docker compose."""

STORES_FILE = "./stores.json"
POSTCODESIO_BULK_POSTCODES_URL = "https://api.postcodes.io/postcodes"

# Lat and long for some postcodes cannot be retrieved. We can agree with the business
# on what is an acceptable success rate of retrieval, i.e. 93%.
POSTCODESIO_BULK_POSTCODES_SUCCESS_RATE = 0.93

TEST_STORE_POSTCODES_FILE = "./test_store_postcodes.json"
