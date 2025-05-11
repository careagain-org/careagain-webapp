import reflex as rx
import uuid
from typing import List,Dict
from .user_input_text import SimpleTextInput
from .upload import upload_logo_org
from ..states.project_state import ProjectState
from ..states.org_state import OrgState
from .upload import upload_logo_org
from .map import interactive_map
import clipboard
import os
from ..components.org_card import org_grid_vertical


def form_org() -> rx.Component:
    all_organization: list[str] = ["Hospital", "Logistics & transport",
                                    "Research & Development","Manufacturer"]

    return rx.dialog.content(
        rx.dialog.title(f"Add new organization"),
        rx.dialog.description(
                f"Add new organization details, required fields marked with *",
                size="2",
                margin_bottom="16px",
            ),
        rx.form(
                rx.flex(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Name *",size="3"),
                            rx.input(placeholder="Enter organization name",
                            name="name",
                            required=True,
                            width="100%"),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.heading("Type of organization *",size="3"),
                            rx.select(all_organization, 
                                    placeholder="Select Organization Type",
                                    name="type",
                                    default_value=None,
                                    required=True,
                                    width="100%"),
                            width="100%"
                        ),
                        width="100%",
                    ),
                    rx.heading("Organization Description",size="3"),
                    rx.text_area(
                        placeholder="Type here...",
                        name="description",),
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Website url / social media",size="3"),
                            rx.input(placeholder="Enter url link",
                                name= "website",
                                width="100%"),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.heading("E-mail",size="3"),
                            rx.input(placeholder="Enter organization email",
                                name="email",width="100%"),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.hstack(
                            upload_logo_org(title="Logo",my_image=rx.get_upload_url(OrgState.logo)),
                            rx.vstack(
                                rx.hstack(rx.heading("Locate in the map",color="grey",size="3"),
                                        rx.text(value=OrgState.longitude,name="location")),
                                interactive_map(),
                                rx.text("** one click to add a new pin, double-click to remove it",size="1"),
                                rx.flex(
                                    rx.text("Visibility in the community map"),
                                    rx.switch(id="visibility",on_change=OrgState.update_location),
                                    spacing="5",
                                    ),
                                ),
                            ),
                    rx.heading("Address",size="3"),
                    rx.text_area(placeholder="Enter organization address",
                        name="address",),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                color_scheme="gray",
                                variant="soft",
                                justify="start",),
                        ),
                        rx.dialog.close(
                            rx.button("Save",
                                type ="submit",
                                justify="end",
                                color_scheme="teal",),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                        width="100%",
                    ),
                    spacing = "3",
                    direction = "column",
                    width="100%",
                ),
                on_submit=OrgState.create_new_org,
                reset_on_submit=True,
            )
        )



def search_org() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Search existing organization"),
        rx.form(
            rx.flex(
            rx.input(rx.icon("search"),
                        placeholder="Enter organization name",
                        default_value="",
                        name="name",
                        required=True,
                        width="100%",
                        align="start",
                        on_change=lambda value:OrgState.filter_org(value)),
            org_grid_vertical(OrgState.filtered_orgs),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                        justify="start",
                        type ="button",
                    ),
                ),
                rx.dialog.close(
                    rx.button("Add",
                        type ="submit",
                        justify="end",
                        color_scheme="teal")
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
                width="100%",
            ),
            width="100%",
            spacing = "3",
            direction = "column",
        ),
        on_submit=OrgState.join_org,
        reset_on_submit=True,
    )
)
    
def discover_org():
    return rx.form(
            rx.text('Discover the different organizations:',),
            rx.hstack(
                rx.input(name="search",
                         width="30vw"),
                rx.icon_button("search"),
                width="100%"
            ),
            on_submit=OrgState.search_orgs,
            width="100%",
            spacing="2"
        ),
    
def update_coordinates_form():
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Update coordenates")),
        rx.dialog.content(
            rx.dialog.title("Update location"),
            interactive_map(),
            rx.text("** one click to add a new pin, double-click to remove it",size="1"),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                        justify="start",),
                ),
                rx.dialog.close(
                    rx.button("Save",
                        type ="submit",
                        justify="end",
                        color_scheme="teal",
                        on_click=OrgState.update_coordinates),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
                width="100%",
                min_height="100px",
            ),
        ),
    ),

# class OrganizationForm(rx.ComponentState):
#     form_data: dict = {}
#     form_fields: list[str] = [
#         "org_id",
#         "name",
#         "type",
#         "description",
#         "latitude",
#         "longitude",
#         "logo",
#         ""

#     ]

#     @rx.event
#     def remove_all(cls):
#         CreateOrg.name = None
#         CreateOrg.name = None
#         CreateOrg.type = None
#         CreateOrg.description = None
#         CreateOrg.latitude = None
#         CreateOrg.longitude = None
#         CreateOrg.logo = None
#         CreateOrg.email = None
#         CreateOrg.web_link= None
#         CreateOrg.map_visible = True

#     @rx.event
#     def reset_form(cls):
#         """Reset all fields in the form."""
#         for field in vars(CreateOrg):
#             setattr(CreateOrg, field, None)
#         CreateOrg.map_visible = True

#     @rx.event
#     def set_name(cls, value: str):
#         CreateOrg.org_id = str(uuid.uuid4())
#         CreateOrg.name = value
    
#     @rx.event
#     def set_type(cls, value: str):
#         CreateOrg.type = value

#     @rx.event
#     def set_address(cls, value: str):
#         CreateOrg.address = value

#     @rx.event
#     def set_description(cls, value: str):
#         CreateOrg.description = value
    
#     @rx.event
#     def set_weblink(cls, value: str):
#         CreateOrg.web_link = value
    
#     @rx.event
#     def set_email(cls, value: str):
#         CreateOrg.email = value
    

#     # @rx.event
#     # async def handle_submit(cls):
#     #     OrgState.add_new_org

#     #     return rx.toast(OrgState.new_org["name"])
#         # OrgState.new_org["org_id"] = uuid.uuid4()
#         # print(OrgState.new_org)
#         # print(form_data)
#         # # Handle form submission (e.g., print or send data)
#         # print(f"Form submitted with Name")

#     @classmethod
#     def get_component(cls, **props):
#         all_organization: list[str] = ["Hospital","NGO", "Logistics & transport",
#                                    "University","Enterprise", "R&D",
#                                    "Manufacturer", "Religious entity"]
        
#         form_fields = rx.flex(
#                     rx.heading("Name *",size="3"),
#                     rx.input(placeholder="Enter organization name",
#                                 on_change = cls.set_name,
#                                 name="name",
#                                 required=True),
#                     rx.heading("Type of organization *",size="3"),
#                     rx.select(all_organization, 
#                             placeholder="Select Organization Type",
#                             on_change = cls.set_type,
#                             name="type"),
#                     rx.heading("Organization Description",size="3"),
#                     rx.text_area(
#                         placeholder="Type here...",
#                         name="description",
#                         on_change = cls.set_description,
#                     ),
#                     rx.heading("Website url (if aplicable)",size="3"),
#                     rx.input(placeholder="Enter url link",
#                              on_change = cls.set_weblink),
#                     rx.hstack(
#                         upload_image(title="Logo",my_image=""),
#                         rx.vstack(
#                             rx.heading("Locate in the map",color="grey",size="3"),
#                             interactive_map(),
#                             rx.text("** one click to add a new pin, double-click to remove it",size="1"),
#                             rx.flex(
#                                 rx.text("Visibility in the community map"),
#                                 rx.switch(checked=True,id="visibility"),
#                                 spacing="5",
#                                 )
#                             ),
#                         ),
#                     rx.heading("Address",size="3"),
#                     rx.input(placeholder="Enter organization address",
#                         name="address",
#                         on_change = cls.set_address,),
#                     rx.heading("E-mail",size="3"),
#                     rx.input(placeholder="Enter organization email",
#                         name="email",
#                         on_change = cls.set_email,),
#                 rx.flex(
#                     rx.dialog.close(
#                         rx.button(
#                             "Cancel",
#                             color_scheme="gray",
#                             variant="soft",
#                             justify="start",
#                         ),
#                     ),
#                     rx.dialog.close(
#                         rx.button("Save",
#                             type ="submit",
#                             on_click=[OrgState.create_new_org,cls.reset_form,],
#                             justify="end",
#                             color_scheme="teal",),
#                     ),
#                     spacing="3",
#                     margin_top="16px",
#                     justify="end",
#                     width="100%",
#                 ),
#                 spacing = "3",
#                 direction = "column"
#         )

#         return rx.dialog.content(
#             rx.dialog.title(f"Add new organization"),
#             rx.dialog.description(
#                     f"Add new organization details, required fields marked with *",
#                     size="2",
#                     margin_bottom="16px",
#                 ),
#             rx.form(
#                 form_fields,
#                 # on_submit=cls.handle_submit,
#                 reset_on_submit=True,
#             )
#         )