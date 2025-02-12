import plotly.graph_objects as go
import reflex as rx
import folium
from folium import plugins
from ..states.org_state import OrgState
from typing import List, Dict,Any
from ..constants import urls
import httpx
import pandas as pd
import requests
import clipboard
import logging

@rx.dynamic
def create_map(org_state: OrgState):
    # Create map centered on [0, 0] with zoom level 2
    map_ = folium.Map(location=[0, 0], zoom_start=2)

    # add markercluster
    marker_cluster = plugins.MarkerCluster().add_to(map_)

    # Fetch organization locations
    orgs = org_state.orgs_locations 
    
    # Only add markers if orgs is a non-empty list
    if orgs:
        for org in orgs:
            folium.Marker(
                location=[float(org["latitude"]), float(org["longitude"])],
                popup=org["name"],
                # tooltip=org["org_name"],
                icon=folium.Icon(color="red")
            ).add_to(marker_cluster)

    # Return the map as an HTML box (save)
    return rx.box(
        rx.html(map_._repr_html_()),
        style={"width": "80%","align":"center"}
        )


def find_popup_variable_name(html):
    pattern = "var lat_lng"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

# Reflex app state
class MapState(rx.State):
    lat: float = 0.0
    lng: float = 0.0

    def update_location(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

def interactive_map():
    map_ = folium.Map(location=[40.463667, -3.74922], zoom_start=1)

    # if OrgState.str_location is None:
    # folium.LatLngPopup().add_to(map_)
    folium.ClickForMarker(popup="<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}").add_to(map_)
    folium.ClickForLatLng(format_str='lat + "," + lng', alert=True).add_to(map_)

    return rx.box(
        rx.html(map_._repr_html_()),
        style={"width": "100%","align":"center"}
        )