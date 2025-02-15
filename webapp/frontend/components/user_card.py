import reflex as rx
import httpx
from ..states.user_state import UserState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
s3_url = os.environ.get("SUPABASE_S3_URL")
s3_bucket = os.environ.get("SUPABASE_S3_BUCKET")
s3_prfolder = "/projects/project_id"
s3_imfolder = "/images/"


def user_card_horizontal(user)-> rx.Component:

    return rx.container(
        rx.card(
            rx.link(
                rx.flex(
                    rx.avatar(src=user["profile_image"],
                             radius="large",
                            width="100px",
                            height="100px"),
                    rx.heading(user["first_name"]+" "+ user["last_name1"],align="center"),
                    rx.text("@"+user["username"]),
                    rx.badge(user["member_type"]),
                    direction="column",
                    padding ="0",
                    align="center"
                ),
                # href=f"/{urls.INDIVIDUAL_PROJECT_URL}{project_id}",
                # on_click=ProjectState.select_project(project_id),
                align="start"
            ),
            # as_child=True,
            size="5",
            height='220px',
            width='180px',
            padding ="1%",
            align="start",
        ),
        height = 'auto',
        align='start',
        width = '250px',

    )

def users_grid_horizontal(users)-> rx.Component:
    return rx.scroll_area(
        rx.hstack(
            rx.cond(
                users != [],
                rx.foreach(users, lambda value, i: 
                            user_card_horizontal(value)),
                rx.text("No users available")
            ),   
            # spacing_y="1",
            #width="100%",
            align ="start",
            justify = "start"
        ),
        align ="start",
        justify = "start",
        type="hover",
        scrollbars="horizontal",
        style={"height": '250px'},
)
    