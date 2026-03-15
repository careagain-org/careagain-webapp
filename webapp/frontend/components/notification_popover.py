import reflex as rx
from ..states.action_state import ActionState
from ..constants import urls

def notification_popover()->rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.icon("bell",color="teal"),
        ),
        rx.popover.content(
            # notification_content(),
            rx.flex(
                rx.text("There are no notifications yet"),
                direction="column",
                spacing="3",
            ),
        ),
        on_click=ActionState.get_my_actions()
    )
    
def notification_content() ->rx.Component:
    return  rx.flex(
        rx.scroll_area(
            action_grid_vertical(ActionState.my_notifications),
            direction="column",
            spacing="3",
        ),
    ),
    
    
def action_card(action)-> rx.Component:
    return rx.card(
            rx.link(
                rx.vstack(
                    rx.heading(str(action["action_date"]),size="2"),
                    rx.text(action["description"]),
                    spacing="1",
                ),
                href=f"/{action['receiver_type']}_view/{action['received_by']}",
                align="start"
            ),
            # width = "100%",
            size="3",
            _hover={"color": "teal"},
            width="250px",
            height= "50px",
        )
    

def action_grid_vertical(actions)-> rx.Component:

    return rx.vstack(
        rx.cond(
            actions != [],
            rx.foreach(actions, lambda action, i: 
                        action_card(action),),
            rx.text("There are no notifications yet"),#rx.spinner(),#rx.text("No action available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )