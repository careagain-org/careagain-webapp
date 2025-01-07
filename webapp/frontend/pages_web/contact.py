import reflex as rx 

from .base import base_page
from ..constants import urls
from ..states import nav_state as state

class ContactState(rx.State):
    title_text: str = "Contacta con nosotros"
    my_email_text: str = "Email: " + urls.EMAIL
    name_text: str = "Nombre"
    your_email_text: str = "Email"
    message_text: str = ""
    submitted: bool = False

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        self.submitted = True


@rx.page(route=urls.CONTACT_URL)
def contact_page() -> rx.Component:
    my_form = rx.form(
        rx.vstack(
            rx.text(ContactState.my_email_text),
            rx.hstack(
                rx.input(
                        placeholder="First Name",
                        required =True,
                        type='text',
                        name="first_name",
                        width='100%'
                    ),
                rx.input(
                        placeholder="Last Name",
                        required =True,
                        type='text',
                        name="last_name",
                        width='100%'
                    ),
                    width='100%'
            ),
            rx.input(
                    placeholder="Email",
                    required =True,
                    type='email',
                    name="email",
                    width='100%'
                ),
            rx.text_area(
                placeholder="Message",
                required =True,
                type='text',
                name="message",
                width='100%'
            ),
            rx.button("Submit", type="submit",align="center"),
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=False,
    )

    my_child = rx.vstack(
            rx.desktop_only(
                rx.flex(
                    rx.image('/cor_nobackground.png'),
                    rx.box(
                        rx.cond(ContactState.submitted,
                        rx.heading("Thanks for contacting us!", size="9"),
                        rx.heading("Contact Us", size="9")
                        ),
                        my_form,
                        width='25vw'
                    ),
                    spacing="5",
                    width="100%",
                    justify="between",
                )
            
            ),
            rx.mobile_and_tablet(
                rx.cond(ContactState.submitted,
                    rx.heading("Thanks for contacting us!", size="9"),
                    rx.heading("Contact Us", size="9")
                    ),
                my_form,
                width='75vw'
                ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
            id='my-child'
        )


    
    return base_page(my_child)