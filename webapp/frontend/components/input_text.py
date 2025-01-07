import reflex as rx
import typing as Callable
from ..states.user_state import UserState

class EditableText(rx.ComponentState):
    text: str = "Click to edit"
    original_text: str
    editing: bool = False

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

        # Set the initial value of the State var.
        initial_value = props.pop("initial_value", cls.text)
        # if initial_value is not None:
        # # Update the pydantic model to use the initial value as default.
        #     cls.__fields__["text"].default = initial_value

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
                ],),
            align="center",
            width="100%",
        )

        # Return the text or the form based on the editing Var.
        return rx.cond(
            cls.editing,
            rx.form(
                edit_controls,
                on_submit=lambda _: cls.stop_editing(),
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

# New component: SimpleTextInput

class SimpleTextInput(rx.ComponentState):
    input_value: str = ""

    @classmethod
    def get_component(cls, **props):
        # Extract the title (label) from props if provided, default to an empty string
        title = props.pop("title", "")
        value = props.pop("value", cls.input_value)
        on_change = props.pop("on_change", cls.set_input_value)

        # Create a title (label) component if the title prop is provided
        #title_component = rx.text(title, font_weight="bold") if title else None

        # Return a vertical stack (vstack) to render the title above the input field
        return rx.vstack(
            rx.text(title, font_weight="bold"),  # Only renders if title_component is not None
            rx.input(
                value=value,
                on_change=on_change,
                **props,  # Pass additional props like placeholder, style, etc.
                width="100%",
            ),
            align="start",  # Align the items to the start (left)
            width="100%",   # Ensure the input takes full width
        )

    @classmethod
    def set_input_value(cls, value: str):
        cls.input_value = value