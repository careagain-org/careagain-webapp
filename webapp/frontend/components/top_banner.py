import reflex as rx

class TopBannerSignup(rx.ComponentState):
    hide: bool = False

    def toggle(self):
        self.hide = not self.hide

    @classmethod
    def get_component(cls, **props):
        return rx.cond(
            ~cls.hide,
            rx.flex(
                rx.image(
                    src="/logo1.png",
                    width="2em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.text(
                    "Start being part of a global communtiy to make healthcare available to everyone.",
                    weight="medium",
                ),
                rx.flex(
                    rx.button(
                        "Sign up",
                        cursor="pointer",
                        radius="large",
                    ),
                    rx.icon(
                        "x",
                        cursor="pointer",
                        justify="end",
                        flex_shrink=0,
                        on_click=cls.toggle,
                    ),
                    spacing="4",
                    align="center",
                ),
                wrap="nowrap",
                # position="fixed",
                flex_direction=["column", "column", "row"],
                justify_content=["start", "space-between"],
                width="100%",
                # top="0",
                spacing="2",
                align_items=["start", "start", "center"],
                left="0",
                # z_index="50",
                padding="1rem",
                background=rx.color("accent", 4),
                **props,
            ),
            # Remove this in production
            rx.icon_button(
                rx.icon("eye"),
                cursor="pointer",
                on_click=cls.toggle,
            ),
        )


top_banner_signup = TopBannerSignup.create