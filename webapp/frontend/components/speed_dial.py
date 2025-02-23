import reflex as rx
from ..constants import urls

class SpeedDialMenu(rx.ComponentState):
    is_open: bool = False

    @rx.event
    def toggle(self, value: bool):
        self.is_open = value

    @classmethod
    def get_component(cls, **props):
        def menu_item(icon: str, text: str, link: str) -> rx.Component:
            return rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon(icon, padding="2px"),
                        rx.text(text, weight="medium"),
                    ),
                    href=link,
                    align="center",
                    opacity="0.75",
                    cursor="pointer",
                    position="relative",
                    _hover={
                        "opacity": "1",
                    },
                    width="100%",
                    align_items="center",
                )
            )

        def menu() -> rx.Component:
            return rx.box(
                rx.card(
                    rx.vstack(
                        menu_item("bug", "Report issue", urls.REPORT_URL),
                        rx.divider(margin="0"),
                        menu_item("repeat-2", "Feedback", urls.FEEDBACK_URL),
                        direction="column-reverse",
                        align_items="end",
                        justify_content="end",
                    ),
                    box_shadow="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
                ),
                position="absolute",
                bottom="100%",
                right="0",
                padding_bottom="10px",
            )

        return rx.box(
            rx.box(
                rx.icon_button(
                    rx.icon(
                        "plus",
                        style={
                            "transform": rx.cond(
                                cls.is_open,
                                "rotate(45deg)",
                                "rotate(0)",
                            ),
                            "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
                        },
                        class_name="dial",
                    ),
                    variant="solid",
                    color_scheme="teal",
                    size="3",
                    cursor="pointer",
                    radius="full",
                    position="relative",
                ),
                rx.cond(
                    cls.is_open,
                    menu(),
                ),
                position="relative",
            ),
            # on_mouse_enter=cls.toggle(True),
            # on_mouse_leave=cls.toggle(False),
            on_click=cls.toggle(~cls.is_open),
            style={"bottom": "15px", "right": "15px"},
            position="fixed",
            # z_index="50",
            **props,
        )


speed_dial_menu = SpeedDialMenu.create


def render_menu():
    return rx.box(
        speed_dial_menu(),
        height="250px",
        position="relative",
        width="100%",
    )