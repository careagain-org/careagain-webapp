import reflex as rx

def notification_popover()->rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.icon("bell",color="teal"),
        ),
        rx.popover.content(
            rx.flex(
                rx.text("There are no notifications yet"),
                direction="column",
                spacing="3",
            ),
        ),
    )