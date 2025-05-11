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
from folium import Map, CustomIcon, Html, Element, MacroElement
from jinja2 import Template


class MapState(OrgState):
    lat= ""
    lng= ""
    
    @rx.var
    def folium_map_html(self) -> str:
        # Create map centered on [0, 0] with zoom level 2
        map_ = folium.Map(location=[0, 0], zoom_start=2)
        
        # add markercluster
        # marker_cluster = folium.plugins.MarkerCluster(control=False)
        # map_.add_child(marker_cluster)
        
        g1 = folium.plugins.FeatureGroupSubGroup(map_, "Research & Dev")
        map_.add_child(g1)

        g2 = folium.plugins.FeatureGroupSubGroup(map_, "Logistics & Transport")
        map_.add_child(g2)
        
        g3 = folium.plugins.FeatureGroupSubGroup(map_, "Hospital")
        map_.add_child(g3)
        
        g4 = folium.plugins.FeatureGroupSubGroup(map_, "Manufacturer")
        map_.add_child(g4)

        # Fetch organization locations
        orgs = self.orgs
        
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
        
        return map_._repr_html_()
    
    @rx.var
    def individual_folium_map_html(self)-> str:
    
        try:
            map_ = folium.Map(location=[self.selected_org["latitude"], 
                                        self.selected_org["longitude"]], zoom_start=7)
            
            folium.Marker(
                    location=[float(self.selected_org["latitude"]), 
                            float(self.selected_org["longitude"])],
                    popup=self.selected_org["name"],
                    icon=folium.Icon(color="red") 
                ).add_to(map_)
        except Exception as err:
            map_ = folium.Map(location=[40.463667, -3.74922], zoom_start=2)
            print(err)
            
        return map_._repr_html_()
    
    @rx.var
    def interactive_map_html(self)-> str:
        map_ = folium.Map(location=[40.463667, -3.74922], zoom_start=2)
        folium.ClickForMarker(popup="<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}").add_to(map_)
        folium.ClickForLatLng(format_str='lat + "," + lng', alert=True).add_to(map_)
        return map_._repr_html_()


def create_map() -> rx.Component:
    """Create a map component using Folium."""
    return rx.el.div(
        rx.el.iframe(
            src_doc=MapState.folium_map_html,
            class_name="w-full h-[calc(100vh-200px)] border-none rounded-lg shadow-md",
            width = "100%",
        ),
        class_name="p-1 bg-gray-50 rounded-lg shadow-inner",
        width = "80%",
    )


def find_popup_variable_name(html):
    pattern = "var lat_lng"
    if html:
        starting_index = html.find(pattern) + 4
        tmp_html = html[starting_index:]
        ending_index = tmp_html.find(" =") + starting_index

        return html[starting_index:ending_index]


def interactive_map():
    # MapState.lat = find_popup_variable_name(MapState.interactive_map_html)
    # MapState.interactive_map_html
    return rx.el.div(
            # rx.text(MapState.lat),
            rx.el.iframe(
                src_doc=MapState.interactive_map_html,
                class_name="w-full h-full border-none rounded-lg shadow-md",
                width = "100%",
                heigth = "100%",
            ),
            # class_name="p-1 bg-gray-50 rounded-lg shadow-inner",
            width = "100%",
            height = "100%",
        )

def map_org()-> rx.Component:

    return rx.el.div(
        rx.el.iframe(
            src_doc=MapState.individual_folium_map_html,
            class_name="w-full h-[calc(40vh-50px)] border-none rounded-lg shadow-md",
            width = "100%",
            heigth = "100%",
        ),
        class_name="p-1 bg-gray-50 rounded-lg shadow-inner",
        width = "100%",
    )

