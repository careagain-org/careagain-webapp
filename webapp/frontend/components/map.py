import plotly.graph_objects as go
import reflex as rx
import folium
from ..states.org_state import OrgState
from typing import List, Dict,Any
from ..constants import urls
import httpx
import pandas as pd
import requests

@rx.dynamic
def create_map(org_state: OrgState):
    # Create map centered on [0, 0] with zoom level 2
    map_ = folium.Map(location=[0, 0], zoom_start=2)

    # Fetch organization locations
    orgs = org_state.orgs_locations 
    
    # Only add markers if orgs is a non-empty list
    if orgs:
        for org in orgs:
            folium.Marker(
                location=[float(org["latitude"]), float(org["longitude"])],
                popup=org["org_name"],
                icon=folium.Icon(color="red")
            ).add_to(map_)

    # Return the map as an HTML box
    return rx.box(
        rx.html(map_._repr_html_()),
        style={"width": "80%","align":"center"}
        )

def pin_map():
    map_ = folium.Map(location=[0, 0], zoom_start=2)