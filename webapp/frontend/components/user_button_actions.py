import reflex as rx
from ..states.user_state import UserState
from ..states.org_state import OrgState
from ..states.project_state import ProjectState
from ..constants import urls

def button_view(user_id):
    return rx.icon_button("eye",
                          variant="soft",
                          tooltip="view",
                          on_click=lambda: [UserState.to_user_view(user_id)])


def dialog_leave(user_id:str,dettached_field:str):

    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button("log-out",variant="soft"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Remove user"),
            rx.alert_dialog.description(
                "Are you sure? This user will not have any role in this.",
                size="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.match(dettached_field,
                    ("organization",rx.alert_dialog.action(
                        rx.button(
                            "Remove user",
                            color_scheme="red",
                            variant="solid",
                            on_click= lambda: OrgState.user_dettached_org(user_id)
                        ),),),
                    ("project",rx.alert_dialog.action(
                        rx.button(
                            "Remove user",
                            color_scheme="red",
                            variant="solid",
                            on_click= lambda: ProjectState.user_dettached_project(user_id)
                        ),),),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )