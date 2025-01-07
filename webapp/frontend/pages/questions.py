import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..components.question_card import question_grid_vertical
from ..components.forms_popover import add_new_popover
from ..states.question_state import QuestionState
from ..states.auth_state import AuthState

@rx.page(route=urls.QUESTIONS_URL, on_load= QuestionState.get_list_questions)
def platform_questions() -> rx.Component:
    my_child = rx.vstack(
        rx.hstack(
            rx.heading('Questions', size="9"),
            add_new_popover("project"),
            align="end",
            spacing="5"
        ),
        rx.text(
            'Discover the different questions',
        ),
        question_grid_vertical(),
        align = "start",
        justify="start",
        width ="100%"
    )
    return platform_base(my_child)
    