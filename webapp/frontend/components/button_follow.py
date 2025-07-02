import reflex as rx

class FollowButton(rx.ComponentState):
    following: bool = False

    @rx.event
    def toggle(self, value: bool):
        self.following = value

    @classmethod
    def get_component(cls, **props):
        def menu_item(icon: str, text: str) -> rx.Component:
            return rx.tooltip(
                rx.icon_button(
                    rx.icon(icon, padding="2px"),
                    variant="soft",
                    color_scheme="gray",
                    size="3",
                    cursor="pointer",
                    radius="full",
                ),
                side="left",
                content=text,
            )

        def menu() -> rx.Component:
            return rx.vstack(
                menu_item("copy", "Copy"),
                menu_item("download", "Download"),
                menu_item("share-2", "Share"),
                position="absolute",
                bottom="100%",
                spacing="2",
                padding_bottom="10px",
                left="0",
                direction="column-reverse",
                align_items="center",
            )

        return rx.box(
                rx.button(
                    rx.cond(cls.following,
                            "Following",
                            "Follow"),
                    style={
                            "transform": rx.cond(
                                cls.following,
                                "rotate(45deg)",
                                "rotate(0)",
                            ),
                            "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
                        },
                        variant="solid",
                        color_scheme="blue",
                        size="3",
                        cursor="pointer",
                        radius="full",
                        position="relative",
                        on_mouse_enter=cls.toggle(True),
                        on_mouse_leave=cls.toggle(False),
                        on_click=cls.toggle(~cls.following),
                        )
        
        
            **props,
        )


follow_button = FollowButton.create


def render_vertical():
    return rx.box(
        follow_button(),
        height="250px",
        position="relative",
        width="100%",
    )

