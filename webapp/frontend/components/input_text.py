import reflex as rx

class EditableText(rx.ComponentState):
    text: str = ""
    original_text: str = ""
    editing: bool = False

    def set_text(self, value: str):
        self.text = value

    def start_editing(self, original_text: str):
        self.original_text = original_text
        self.editing = True

    def stop_editing(self):
        self.editing = False
        self.original_text = ""

    @classmethod
    def get_component(cls, **props):
        value = props.pop("value", cls.text)
        on_change = props.pop("on_change", cls.set_text)
        on_save = props.pop("on_save", lambda: None)  # <-- injectable save handler
        cursor = props.pop("cursor", "pointer")

        edit_controls = rx.hstack(
            rx.input(
                value=value,
                on_change=on_change,
                **props,
            ),
            rx.icon_button(
                rx.icon("x"),
                on_click=[
                    on_change(cls.original_text),
                    cls.stop_editing,
                ],
                type="button",
                color_scheme="red",
            ),
            rx.icon_button(
                rx.icon("check"),
                on_click=[
                    cls.stop_editing,
                ],
                type="submit",
            ),
            align="center",
            width="100%",
        )

        return rx.cond(
            cls.editing,
            rx.form(
                edit_controls,
                on_submit=lambda _: [
                    on_change(cls.text),
                    cls.stop_editing(),
                    on_save(cls.text),  # <-- calls whatever you passed in
                ],
            ),
            rx.hstack(
                rx.text(value, cursor=cursor, **props),
                rx.icon_button(
                    "pencil",
                    variant="soft",
                    on_click=cls.start_editing(value),
                ),
            ),
        )

class EditableTextArea(rx.ComponentState):
    text: str = ""
    original_text: str = ""
    editing: bool = False

    def set_text(self, value: str):
        # Replace single newlines with double newlines for markdown
        self.text = value.replace("\n", "  \n")

    def start_editing(self, original_text: str):
        self.original_text = original_text
        self.editing = True

    def stop_editing(self):
        self.editing = False
        self.original_text = ""

    @classmethod
    def get_component(cls, **props):
        value = props.pop("value", cls.text)
        on_change = props.pop("on_change", cls.set_text)
        on_save = props.pop("on_save", lambda: None)
        cursor = props.pop("cursor", "pointer")

        edit_controls = rx.vstack(
            rx.text_area(
                value=value,
                on_change=on_change,
                width="40vw",
                min_height="10em",
                font_family="monospace",  # helps when typing markdown
                placeholder="Supports markdown: **bold**, *italic*, newlines...",
            ),
            rx.hstack(
                rx.text("Supports **markdown** syntax", font_size="0.75em", color="gray"),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x"),
                    on_click=[
                        on_change(cls.original_text),
                        cls.stop_editing,
                    ],
                    type="button",
                    color_scheme="red",
                ),
                rx.icon_button(
                    rx.icon("check"),
                    on_click=[cls.stop_editing],
                    type="submit",
                ),
                width="100%",
                align="center",
            ),
            width="100%",
        )

        return rx.cond(
            cls.editing,
            rx.form(
                edit_controls,
                on_submit=lambda _: [
                    on_change(cls.text),
                    cls.stop_editing(),
                    on_save(cls.text),
                ],
            ),
            rx.hstack(
                # Renders markdown properly: **bold**, *italic*, \n, etc.
                rx.markdown(value, **props),
                rx.icon_button(
                    "pencil",
                    variant="soft",
                    on_click=cls.start_editing(value),
                ),
                cursor=cursor,
                align="start",
                width="100%",
            ),
        )