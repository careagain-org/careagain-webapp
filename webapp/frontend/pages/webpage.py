import reflex as rx 

from .webpage_base import base_page
from ..constants import urls
from ..components.map import create_map
from ..states.org_state import OrgState
from ..components.speed_dial import SpeedDialMenu

speed_dial_menu = SpeedDialMenu.create

def home_logo() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to a Open Source Community",size="8",color="gray",
                   high_contrast=True,align="center"),
        rx.image('full_logo.png', width="50%",),
        rx.heading("to facilitate the access to medical technology",
                   size="8",color="gray",high_contrast=True,align="center"), 
        rx.spacer(size=5),   
        margin="12px",
        padding="5",
        width="100%",
        border="10px",
        align="center",
        justify="center",
        id="home_logo",
    )

def problem_section(direction: str) -> rx.Component:
    return rx.flex(
                rx.image('hombre_repadando_equipos.webp',
                        # height="50em",
                        align="start"),
                rx.vstack(
                    rx.heading("Current situation", size="9"),
                    create_feature_box(
                        icon_tag="dollar-sign",
                        heading_text="High Costs",
                        description_text="Medical devices are often prohibitively expensive, limiting access to essential healthcare technologies.",
                    ),
                    create_feature_box(
                        icon_tag="lock",
                        heading_text="Limited Access",
                        description_text="Many regions lack access to crucial medical devices, creating disparities in healthcare quality.",
                    ),
                    create_feature_box(
                        icon_tag="frown",
                        heading_text="Slow Innovation",
                        description_text="Closed development processes hinder rapid innovation and improvement of medical devices.",
                    ),
                    spacing="5",
                    justify="center",
                    align="center",
                    min_height="60vh",
                    
                ),
                direction=direction,
                width="100%",
                bg=rx.color("teal", 2),
                id="problem_section",
                spacing="5",
                justify="center",
                align="center",
                padding="5"
            ),

def solution_section(direction: str) ->rx.Component:
    return rx.flex(
            rx.vstack(
                rx.heading("Our proposal", size="9",align = "center"),
                # create_feature_box(
                #     icon_tag="hand-helping",
                #     heading_text="High Costs",
                #     description_text="Desde Care Again proponemos crear un repositorio y plataforma colaborativa donde se desarrollen y compartan planos y guías para la construcción de dispositivos médicos con materiales accesibles. ",
                # ),
                create_feature_box(
                    icon_tag="telescope",
                    heading_text="Our vision",
                    description_text="Facilitate access to essential medical equipment globally through a free platform for sharing open-source projects aimed at local production and the exchange of medical equipment.",
                ),
                create_feature_box(
                    icon_tag="earth",
                    heading_text="Our mision",
                    description_text="Connect development teams with local creators of medical equipment and provide open-source resources and designs to empower communities to build their own medical devices.",
                ),
                spacing="5",
                justify="center",
                align="center",
                min_height="60vh",
                # spacing="5",
                # justify="center",
                # min_height="85vh",
                # padding="15px",
                # margin="100px"
            ),
            rx.image('padre_hijo_reparando.png',
                    align="center",
                    justify="center",),
            width="100%",
            direction=direction,
            padding="5",
            id="solution_section",
        )

def community_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Make it possible! Join the community!",size="9",align="center"),
        create_map(),
        align="center",
        # bg=rx.color("teal", 1),
        spacing="5",
        padding="1%",
        color_scheme="teal",
        width="100%",
        id="community_section",
        on_mount=OrgState.get_location
    )

def support_section(direction:str) -> rx.Component:
    return rx.vstack(
        rx.heading("Would you like to support us?",size="9", align="center"),
        rx.text("You can support us on different ways:",size="6",align="center"),
        rx.flex(
            create_feature_box(
                icon_tag="speech",
                heading_text="Spread the word",
                description_text="Talk about it with friends, let us know of any organizations sharing our purpose of making medical devices more acccessible",
            ),
            create_feature_box(
                icon_tag="users",
                heading_text="Be part of the community",
                description_text="Add your institution or organization—whether involved in medical device R&D, manufacturing, logistics, or healthcare—to join a unified network and help build a thriving community.",
            ),
            create_feature_box(
                icon_tag="atom",
                heading_text=rx.link("Upload your project",href = urls.PATREON_URL),
                description_text="If you have developed medical tecnology or you want to start your project, don't hesitate on sharing your knowledge with the community.",
            ),
            # create_feature_box(
            #     icon_tag="handshake",
            #     heading_text=rx.link("Become a patreon",href = urls.PATREON_URL),
            #     description_text="Your financial support help us to mantain, improve and grow the community. Be in touch with all the new advances",
            # ),
            columns="3",
            width="90%",
            flow="column",
            justify="center",
            spacing="5",
            direction=direction,
            align="center",
        ),
        justify="center",
        align="center",
        bg=rx.color("teal", 2),
        spacing="5",
        padding="1%",
        color_scheme="teal",
        width="100%",
        id="support_section",
    )

def create_feature_box(
    icon_tag, heading_text, description_text
):
    """Create a feature box with an icon, heading, and description."""
    return rx.box(
        rx.icon(
            tag=icon_tag,
            height="3rem",
            margin_bottom="1rem",
            margin_left="auto",
            margin_right="auto",
            color="black",
            width="3rem",
        ),
        rx.heading(heading_text,size="6",align="center",),
        rx.text(
            description_text, text_align="center", color="#374151"
        ),
        background_color="#ffffff",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        width="70%",
    )

# def create_problem_section():
#     """Create the Problem section with multiple feature boxes."""
#     return rx.box(
#         rx.heading("The Problem",size="9"),
#         rx.box(
#             create_feature_box(
#                 icon_tag="dollar-sign",
#                 heading_text="High Costs",
#                 description_text="Medical devices are often prohibitively expensive, limiting access to essential healthcare technologies.",
#             ),
#             create_feature_box(
#                 icon_tag="lock",
#                 heading_text="Limited Access",
#                 description_text="Many regions lack access to crucial medical devices, creating disparities in healthcare quality.",
#             ),
#             create_feature_box(
#                 icon_tag="frown",
#                 heading_text="Slow Innovation",
#                 description_text="Closed development processes hinder rapid innovation and improvement of medical devices.",
#             ),
#             gap="2rem",
#             display="grid",
#             grid_template_columns=rx.breakpoints(
#                 {
#                     "0px": "repeat(1, minmax(0, 1fr))",
#                     "768px": "repeat(3, minmax(0, 1fr))",
#                 }
#             ),
#         ),
#         width="100%",
#         style=rx.breakpoints(
#             {
#                 "640px": {"max-width": "640px"},
#                 "768px": {"max-width": "768px"},
#                 "1024px": {"max-width": "1024px"},
#                 "1280px": {"max-width": "1280px"},
#                 "1536px": {"max-width": "1536px"},
#             }
#         ),
#         bg=rx.color("teal", 2),
#         margin_left="auto",
#         margin_right="auto",
#         padding_left="1.5rem",
#         padding_right="1.5rem",
#     )

def contact_section(direction:str) ->rx.Component:
    return rx.flex(
        rx.image("cor_nobackground.png"),
        rx.vstack(
            rx.heading("Contact us",size="9"),
            rx.hstack(
                rx.icon("mail"),
                rx.text(urls.EMAIL)
            ),
            rx.hstack(
                rx.icon("message-circle"),
                rx.link("Join us in Discord", href=urls.DISCORD_URL)
            ),
            align="center",
            justify="center",
            padding="5%",
            spacing="5",
        ),
        width="100%",
        align="center",
        color_scheme="teal",
        direction=direction,
        id="contact_section"
    )

def render_menu():
    return rx.box(
        speed_dial_menu(),
        height="250px",
        position="relative",
        width="100%",
    )

@rx.page(route=urls.HOME_URL, title = 'Home',on_load=OrgState.get_orgs)
def home_page() -> rx.Component:
    my_child = rx.box(
    rx.desktop_only(
        rx.vstack(
            rx.spacer(size="5"),
            rx.image("ai_hospital_pregnant.png",width="100%"),
            home_logo(),
            problem_section(direction="row"),
            solution_section(direction="row"),
            community_section(),
            support_section(direction="row"),
            contact_section(direction="row"),
            align="center"
        )
    ),
    rx.mobile_and_tablet(
        rx.vstack(
            rx.spacer(size="5"),
            rx.image("ai_hospital_pregnant.png",width="100%"),
            home_logo(),
            problem_section(direction="column"),
            solution_section(direction="column"),
            community_section(),
            support_section(direction="column"),
            contact_section(direction="column"),
        ),
        align="center",
        id="box-home"
    ),
    render_menu(),
    )
    return base_page(my_child)