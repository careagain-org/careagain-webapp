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
    marker_cluster = folium.plugins.MarkerCluster(control=False)
    map_.add_child(marker_cluster)
    
    g1 = folium.plugins.FeatureGroupSubGroup(marker_cluster, "Research & Dev")
    map_.add_child(g1)

    g2 = folium.plugins.FeatureGroupSubGroup(marker_cluster, "Logistics & Transport")
    map_.add_child(g2)
    
    g3 = folium.plugins.FeatureGroupSubGroup(marker_cluster, "Hospital")
    map_.add_child(g3)
    
    g4 = folium.plugins.FeatureGroupSubGroup(marker_cluster, "Manufacturer")
    map_.add_child(g4)

    # Fetch organization locations
    orgs = org_state.orgs
    
    # Only add markers if orgs is a non-empty list
    if orgs:
        for org in orgs:
            try:
                if org["type"] == "Research & Development":
                    folium.Marker(
                        location=[float(org["latitude"]), float(org["longitude"])],
                        popup=org["name"],
                        icon=folium.Icon(color="green",icon="cogs", prefix="fa") #atom
                    ).add_to(g1)
                elif org["type"] == "Logistics & transport":
                    folium.Marker(
                        location=[float(org["latitude"]), float(org["longitude"])],
                        popup=org["name"],
                        icon=folium.Icon(color="blue",icon="truck", prefix="fa") #route
                    ).add_to(g2)
                elif org["type"] == "Hospital":
                    folium.Marker(
                        location=[float(org["latitude"]), float(org["longitude"])],
                        popup=org["name"],
                        icon=folium.Icon(color="red",icon="medkit", prefix="fa")
                    ).add_to(g3)
                elif org["type"] == "Manufacturer":
                    folium.Marker(
                        location=[float(org["latitude"]), float(org["longitude"])],
                        popup=org["name"],
                        icon=folium.Icon(color="beige",icon="wrench")
                    ).add_to(g4)
            except Exception as err:
                print(err)
                  
    folium.LayerControl(collapsed=False).add_to(map_)
    
    map_html=map_._repr_html_()

    # Return the map as an HTML box (save)
    return rx.box(
        rx.html(map_html),
        style={"width": "80%","align":"center"}
        )


def find_popup_variable_name(html):
    pattern = "var lat_lng"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]


def interactive_map():
    map_ = folium.Map(location=[40.463667, -3.74922], zoom_start=2)

    folium.ClickForMarker(popup="<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}").add_to(map_)
    folium.ClickForLatLng(format_str='lat + "," + lng', alert=True).add_to(map_)

    return rx.box(
        rx.html(map_._repr_html_()),
        style={"width": "100%","align":"center"}
        )
    
@rx.dynamic
def map_org(org_state: OrgState):
    
    try:
        map_ = folium.Map(location=[org_state.selected_org["latitude"], 
                                    org_state.selected_org["longitude"]], zoom_start=7)
        
        folium.Marker(
                location=[float(org_state.selected_org["latitude"]), 
                        float(org_state.selected_org["longitude"])],
                popup=org_state.selected_org["name"],
                icon=folium.Icon(color="red") 
            ).add_to(map_)
    except Exception as err:
        map_ = folium.Map(location=[40.463667, -3.74922], zoom_start=2)
        print(err)

    return rx.box(
        rx.html(map_._repr_html_()),
        style={"width": "100%","align":"center"}
        )

