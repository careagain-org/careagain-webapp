import reflex as rx
from typing import List,Dict
from .input_text import SimpleTextInput
from ..states.project_state import ProjectState


class ProjectForm(rx.ComponentState):
    # Define form state variables
    name: str = ""
    link: str = ""
    description: str = ""
    image: str = ""
    project_props: Dict[str,str]

    @classmethod
    def set_name(self, value: str):
        self.name = value
        self.project_props["project_id"] = 0
        self.project_props["project_name"] = value

    @classmethod
    def set_link(self, value: str):
        self.link = value
        self.project_props["link"] = value
    
    @classmethod
    def set_description(self, value: str):
        self.description = value
        self.project_props["description"] = value

    # @classmethod
    # def handle_submit(cls):
    #     ProjectState.create_project(cls)

    #     # Handle form submission (e.g., print or send data)
    #     print(f"Form submitted with Name:")

    @classmethod
    def get_component(cls, **props):

        return rx.dialog.content(
            rx.dialog.title(f"Add new Project"),
            rx.dialog.description(
                f"Add new Project details",
                size="2",
                margin_bottom="16px",
            ),
            rx.form(
                rx.flex(
                    rx.heading("Name",size="4"),
                    rx.input(placeholder="Enter your Name",
                        value=cls.name,
                        on_change=cls.set_name,),
                    rx.heading("Project Description",size="4"),
                    rx.text_area(
                        placeholder="Type here...",
                        value=cls.description,
                        on_change=cls.set_description,
                    ),
                    SimpleTextInput.create(
                        title="Link of the project website (if applicable)",
                        placeholder="Enter your Project Link",
                        value=cls.link,
                        on_change=cls.set_link,
                    ),
                    # upload_image("Image","my_image",ProjectState    ),
                    direction="column",
                    spacing="3",
                ),
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                    ),
                ),
                rx.dialog.close(
                    rx.button("Save"),
                    type ='submit',
                    on_click=ProjectState.create_project(cls.project_props)
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            width="100%",
            reset_on_submit=True,
        )



class InstitutionForm(rx.ComponentState):
    # Define form state variables
    name: str = ""
    address: str = ""
    type: str = ""
    uploaded_img: str = ""
    map_visible: bool = True
    all_institution: list[str] = ["Hospital","Intermediate NGO","University","Organization"]

    @classmethod
    def set_name(cls, value: str):
        cls.name = value
    
    @classmethod
    def set_type(cls, value: str):
        cls.type = value

    @classmethod
    def set_address(cls, value: str):
        cls.address = value

    @classmethod
    def handle_submit(cls):
        # Handle form submission (e.g., print or send data)
        print(f"Form submitted with Name")

    @classmethod
    def get_component(cls, **props):
        return rx.dialog.content(
            rx.dialog.title(f"Add new Institution"),
            rx.dialog.description(
                f"Add new Institution details",
                size="2",
                margin_bottom="16px",
            ),
            rx.form(
            rx.flex(
                SimpleTextInput.create(
                    title="Name",
                    placeholder="Enter your Name",
                    value=cls.name,
                    on_change=cls.set_name,
                ),
                rx.select(cls.all_institution, 
                          placeholder="Selection of Fruits",
                          on_change=cls.set_type),
                SimpleTextInput.create(
                    title="Adress",
                    placeholder="Enter your Adress",
                    value=cls.address,
                    on_change=cls.set_address,
                ),
                # upload_image("Image","my_image"),
                rx.flex(
                    rx.switch(default_checked=True),
                    rx.text("Appear in the community map"),
                    spacing="2",
                ),
                direction="column",
                spacing="3",
            ),
            width="100%"
            ),
            rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Save"),
                        type ='submit',
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                width="100%",
                reset_on_submit=True,
        )


    
class VideoForm(rx.ComponentState):
    # Define form state variables
    name: str = ""
    link: str = ""
    description: str = ""
    uploaded_img: str = ""

    @classmethod
    def set_name(cls, value: str):
        cls.name = value

    @classmethod
    def set_link(cls, value: str):
        cls.link = value
    
    @classmethod
    def set_description(cls, value: str):
        cls.description = value

    @classmethod
    def handle_submit(cls):
        # Handle form submission (e.g., print or send data)
        print(f"Form submitted ")

    @classmethod
    def get_component(cls, **props):
        return rx.dialog.content(
            rx.dialog.title(f"Add new Video"),
            rx.dialog.description(
                f"Add new video details",
                size="2",
                margin_bottom="16px",
            ),
            rx.form(
                rx.flex(
                    SimpleTextInput.create(
                        title="Name",
                        placeholder="Enter your Name",
                        value=cls.name,
                        on_change=cls.set_name,
                    ),
                    SimpleTextInput.create(
                        title="Link to youtube video",
                        placeholder="Enter your youtube video",
                        value=cls.name,
                        on_change=cls.set_name,
                    ),
                    SimpleTextInput.create(
                        title="Video Description",
                        placeholder="Enter your Video Description",
                        value=cls.description,
                        on_change=cls.set_description,
                    ),

                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Save"),
                        type ='submit',
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                width="100%",
                reset_on_submit=True,
            ),
        )
        