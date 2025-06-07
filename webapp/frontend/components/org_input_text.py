import reflex as rx
import typing as Callable
from ..states.org_state import OrgState

class OrgEditableText(rx.ComponentState):
    text: str = ""
    original_text: str
    editing: bool = False
    key: str = None


    def start_editing(self, original_text: str):
        self.original_text = original_text
        self.editing = True

    def stop_editing(self):
        self.editing = False
        self.original_text = ""
        

    @classmethod
    def get_component(cls, **props):
        # Pop component-specific props with defaults before passing **props
        value = props.pop("value", cls.text)
        on_change = props.pop("on_change", cls.set_text)
        cursor = props.pop("cursor", "pointer")
        key = props.pop("key", cls.key)

        # Form elements for editing, saving and reverting the text.
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
            rx.icon_button(rx.icon("check"),
                on_click=[
                    on_change(cls.text),
                    cls.stop_editing,
                    ],
                type="submit",
                ),
            align="center",
            width="100%",
        ),
        

        # Return the text or the form based on the editing Var.
        return rx.cond(
            cls.editing,
            rx.form(
                edit_controls,
                on_submit=lambda _: [on_change(cls.text),
                                     cls.stop_editing(),
                                     OrgState.update_org(key,cls.text)]
            ),
            rx.hstack(
                rx.text(
                    value,
                    cursor=cursor,
                    **props,
                ),
                rx.icon_button("pencil",
                    variant="soft",
                    on_click=cls.start_editing(value),
                )
            )
        )
        
        

class OrgEditableTextArea(rx.ComponentState):
    text: str = "Click to edit"
    original_text: str
    editing: bool = False
    key: str = None


    def start_editing(self, original_text: str):
        self.original_text = original_text
        self.editing = True

    def stop_editing(self):
        self.editing = False
        self.original_text = ""
        

    @classmethod
    def get_component(cls, **props):
        # Pop component-specific props with defaults before passing **props
        value = props.pop("value", cls.text)
        on_change = props.pop("on_change", cls.set_text)
        cursor = props.pop("cursor", "pointer")
        key = props.pop("key", cls.key)

        # Form elements for editing, saving and reverting the text.
        edit_controls = rx.hstack(
            rx.text_area(
                value=value,
                on_change=on_change,
                **props,
                width="40vw",
                min_height="10em"
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
            rx.icon_button(rx.icon("check"),
                on_click=[
                    on_change(cls.text),
                    cls.stop_editing,
                    ],
                type="submit",
                ),
            align="center",
            width="100%",
        ),
        

        # Return the text or the form based on the editing Var.
        return rx.cond(
            cls.editing,
            rx.form(
                edit_controls,
                on_submit=lambda _: [on_change(cls.text),
                                     cls.stop_editing(),
                                     OrgState.update_org(key,cls.text)]
            ),
            rx.hstack(
                rx.text(
                    value,
                    cursor=cursor,
                    **props,
                ),
                rx.icon_button("pencil",
                    variant="soft",
                    on_click=cls.start_editing(value),
                )
            )
        )
