"""e2e tests using the real AppContext."""

# Display success
# Display in alphabetical order
# Display lat and long success


import pytest
from bs4 import BeautifulSoup

# COMMENTED OUT AS IT MAKES REAL CALLS TO POSTCODES.IO.
# UNCOMMENT TESTS TO RUN


# def test_display_success(e2e_client):
#     """Display success"""
#     response = e2e_client.get("/")
#     assert response.status_code == 200
#     assert b"DA11 0DQ" in response.data
#     assert b"RH15 9QT" in response.data
#     assert b"Southend-on-Sea" in response.data
#     assert b"West_Drayton" in response.data


# def test_display_in_alphabetical_order(e2e_client):
#     """Display in alphabetical order"""
#     response = e2e_client.get("/")
#     assert response.status_code == 200
#     soup = BeautifulSoup(response.data, "html.parser")
#     p_store_names = soup.find_all("p", class_="store-name")
#     displayed_store_names = [p.text for p in p_store_names]
#     new_list = displayed_store_names[:]
#     assert displayed_store_names is not new_list
#     assert displayed_store_names == new_list
#     assert displayed_store_names == sorted(new_list)
#     assert displayed_store_names != sorted(new_list, reverse=True)


# def test_display_lat_and_long_success(e2e_client):
#     """Display lat and long success"""
#     response = e2e_client.get("/")
#     assert response.status_code == 200
#     soup = BeautifulSoup(response.data, "html.parser")
#     p_coords = soup.find_all("p", class_="coords")
#     assert any("Lat:" in p.text for p in p_coords)
