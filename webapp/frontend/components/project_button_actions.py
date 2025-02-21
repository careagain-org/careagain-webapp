import reflex as rx
from ..states.project_state import ProjectState
from ..constants import urls

def button_view(project_id):
    return rx.tooltip(rx.icon_button("eye",
                          variant="soft",
                          on_click=lambda: [ProjectState.to_project_view(project_id)]),
                      content="view")

def button_edit(project_id):
    return rx.tooltip(rx.icon_button("pencil",
                          variant="soft",
                          on_click=lambda: [ProjectState.to_project_edit(project_id)]),
                      content="edit")

def dialog_remove(project_id):

    return rx.alert_dialog.root(
        rx.tooltip(
            rx.alert_dialog.trigger(
                rx.icon_button("trash",variant="soft"),
            ),
            content="remove",
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete project"),
            rx.alert_dialog.description(
                "Are you sure? This project will no longer be accessible and any existing users roles from it.",
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
                rx.alert_dialog.action(
                    rx.button(
                        "Delete project",
                        color_scheme="red",
                        variant="solid",
                        on_click= lambda: ProjectState.delete_project(project_id)
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )


def dialog_leave(project_id):

    return rx.alert_dialog.root(
        rx.tooltip(
            rx.alert_dialog.trigger(
                rx.icon_button("log-out",variant="soft"),
            ),
            content="leave",
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Leave project"),
            rx.alert_dialog.description(
                "Are you sure? This project will be accessible, however you will not have any role in it .",
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
                rx.alert_dialog.action(
                    rx.button(
                        "Leave Project",
                        color_scheme="red",
                        variant="solid",
                        on_click= lambda: ProjectState.leave_project(project_id)
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )