"""These tests are for the template html that 
renders the output. But they are still considered
integrations tests rather than e2e as they don't call
the live Postcodes.io api. Instead, the test AppContext
provides a fake repo with the same information as what
Postcodes.io would provide."""

# Display success
# Display in alphabetical order
# Display lat and long success


import pytest
from bs4 import BeautifulSoup


def test_display_success(integrations_client):
    """Display success"""
    response = integrations_client.get("/")
    assert response.status_code == 200
    assert b"DA11 0DQ" in response.data
    assert b"RH15 9QT" in response.data
    assert b"Southend-on-Sea" in response.data
    assert b"West_Drayton" in response.data


def test_display_in_alphabetical_order(integrations_client):
    """Display in alphabetical order"""
    response = integrations_client.get("/")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    p_store_names = soup.find_all("p", class_="store-name")
    displayed_store_names = [p.text for p in p_store_names]
    new_list = displayed_store_names[:]
    assert displayed_store_names is not new_list
    assert displayed_store_names == new_list
    assert displayed_store_names == sorted(new_list)
    assert displayed_store_names != sorted(new_list, reverse=True)


def test_display_lat_and_long_success(integrations_client):
    """Display lat and long success"""
    response = integrations_client.get("/")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    p_coords = soup.find_all("p", class_="coords")
    assert any("Lat:" in p.text for p in p_coords)
