import reflex as rx
import httpx
from ..states.org_state import OrgState

def ind_org(image: str, org_name: str, org_link: str, org_type: str)-> rx.Component:

    return rx.container(
        rx.divider(),
        rx.hstack(
            rx.image(src=image,
                     width="40px",
                    height="40px"),
            rx.vstack(
                rx.cond(org_link is not None,
                        rx.link(rx.heading(org_name,size="5"),
                               href=org_link),
                        rx.heading(org_name,size="5")),
                ),
                rx.text(org_type),
            ),
            width="100%",
            spacing="5"
        )

def list_org_vertical()-> rx.Component:
    return rx.vstack(
        rx.cond(
            OrgState.orgs != [],
            rx.foreach(OrgState.orgs, lambda value, i: 
                        ind_org(image = '/' + value["logo"],
                                org_name = value["org_name"],
                                org_link = value["org_link"],
                                org_type = value["org_type"])),
            rx.text("No projects available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )