import reflex as rx
import httpx
from ..states.user_state import UserState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
s3_url = os.environ.get("SUPABASE_S3_URL")
s3_bucket = os.environ.get("SUPABASE_S3_BUCKET")


def user_card_horizontal(user)-> rx.Component:

    return rx.container(
        rx.card(
            rx.link(
                rx.flex(
                    rx.avatar(src=user["profile_image"],
                             radius="large",
                            width="100px",
                            height="100px"),
                    rx.heading(user["first_name"]+" "+ user["last_name"],size="4",align="center"),
                    rx.text("@"+user["username"]),
                    rx.text(user["country"]),
                    rx.badge(user["member_type"]),
                    direction="column",
                    padding ="0",
                    align="center"
                ),
                on_click=[UserState.select_user(user["user_id"]),
                          rx.redirect(urls.IND_USER_URL)],
                align="start"
            ),
            # as_child=True,
            size="5",
            height='220px',
            width='180px',
            padding ="2%",
            align="start",
        ),
        height = 'auto',
        align='start',
        width = '250px',
    )
    

def users_scroll_horizontal(users)-> rx.Component:
    return rx.scroll_area(
        rx.flex(
        rx.cond(
            users != [],
            rx.foreach(users, lambda value, i: 
                        user_card_horizontal(value)),
            rx.text("No projects available")
            ), 
        ),   
        spacing="2",
        flex_wrap="nowrap",
        width="100%",
        justify = "start"
    )
    
def users_grid_horizontal(users)-> rx.Component:
    return rx.flex(
        rx.cond(
            users != [],
            rx.foreach(users, lambda value, i: 
                        user_card_horizontal(value)),
            rx.text("No projects available")
            ),  
        spacing="2",
        flex_wrap="wrap",
        width="100%",
        justify = "start"
    )

def user_card_vertical(user)-> rx.Component:

    return rx.box(
        rx.card(
            rx.hstack(
                rx.hstack(
                    rx.avatar(src=f"{user["profile_image"]}",
                            width="50px",
                            height="50px"),
                    rx.vstack(
                        rx.heading(f"{user["first_name"]} {user["last_name"]}"),
                        rx.text(f"@{user["username"]}"),
                        rx.text(user["description"]),
                        spacing="2"
                    ),
                ),
                rx.cond(user["user_id"] == UserState.selected_user_id,
                        rx.button("Select",disabled=True,type="button"),
                        rx.button("Select",disabled=False,
                            on_click = lambda: UserState.select_user(user["user_id"]),
                            type="button"),
                        ),
                align="center",
                justify="between",
            ),
            width = "100%",
            size="2",
        ),
        height = 'auto',
        align='start',
        width = "100%",

    )

def user_grid_vertical(users)-> rx.Component:

    return rx.vstack(
        rx.cond(
            users != [],
            rx.foreach(users, lambda value, i: 
                        user_card_vertical(value)),
            rx.spinner(),#rx.text("No users available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )
    