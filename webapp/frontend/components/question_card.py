import reflex as rx
import httpx
from ..states.question_state import QuestionState

def question_card_vertical(question_title: str, question_author: str, question_description: str,)-> rx.Component:

    return rx.card(
            rx.vstack(
                rx.heading(question_title),
                rx.text(f"Created by user {question_author}"),
                rx.divider(),
                rx.text(question_description),
                width="100%",
                spacing="5",
                align='start',
            ),
            as_child=True,
            width = "60vw",
            size="5",
            align='start',
        )

def question_grid_vertical()-> rx.Component:
    return rx.vstack(
        rx.cond(
            QuestionState.questions != [],
            rx.foreach(QuestionState.questions, lambda value, i: 
                        question_card_vertical(question_title = value["title"],
                                    question_author = value["created_by"],
                                    question_description = value["question"])),
            rx.text("No questions available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )


def question_card_horizontal( question_title: str,
                             question:str)-> rx.Component:

    return rx.container(
        rx.card(
            rx.flex(
                rx.box(
                    rx.link(
                        rx.heading(question_title),
                        href= "/questions"
                    ),
                    rx.text("By:"),
                    rx.divider(),
                    rx.spacer(spacing="5"),
                    rx.scroll_area(
                        rx.text(question, color="gray",size="2"),
                        type="scroll",
                        scrollbars="vertical",
                        # style={"height": '210px'},
                    ),
                    width="100%",
                    spacing="5",
                    padding ="2px",
                    align="center",
                    justify="center",
                ),
                spacing="5",
                direction="column",
                padding ="2px",
                align="center"
            ),
            size="5",
            height='180px',
            padding ="5%",
            align="center"
        ),
        height = 'auto',
        width = '25%',
        align='start',
        padding ="2",

    )

def question_grid_horizontal()-> rx.Component:
    return rx.scroll_area(
        rx.hstack(
        rx.cond(
            QuestionState.questions != [],
            rx.foreach(QuestionState.questions, lambda value, i: 
                       question_card_horizontal(question_title = value["title"],
                                                question = value["question"])),
            rx.text("No questions available")
        ),   
        spacing_y="1",
        #width="100%",
        align ="start",
        justify = "start"
    ),
    type="hover",
    scrollbars="horizontal",
    style={"height": '210px'},
)
