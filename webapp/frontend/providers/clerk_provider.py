import reflex as rx
import os
import reflex_clerk_api as reclerk

def my_clerk_provider(child:rx.Component) -> rx.Component:
    return reclerk.clerk_provider(
        rx.fragment(
            child
        ),
        sign_in_fallback_redirect_url = '/platform',
        sign_up_fallback_redirect_url = '/platform',
        publishable_key=os.environ["CLERK_PUBLIC_KEY"],
        secret_key=os.environ["CLERK_SECRET_KEY"],
        register_user_state=True,
    )