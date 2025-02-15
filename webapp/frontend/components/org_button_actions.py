import reflex as rx
from ..states.org_state import OrgState
from ..constants import urls

def button_view(org_id):
    return rx.icon_button("eye",
                          variant="soft",
                          tooltip="view",
                          on_click=lambda: [OrgState.to_org_view(org_id),OrgState.find_members_org(org_id)])

def button_edit(org_id):
    return rx.icon_button("pencil",
                          variant="soft",
                          tooltip="view",
                          on_click=lambda: [OrgState.to_org_edit(org_id),OrgState.find_members_org(org_id)])

def dialog_remove(org_id):

    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button("trash",variant="soft"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete organization"),
            rx.alert_dialog.description(
                "Are you sure? This organization will no longer be accessible and any existing users roles from it.",
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
                        "Delete Organization",
                        color_scheme="red",
                        variant="solid",
                        on_click= lambda: OrgState.delete_my_org(org_id)
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )


def dialog_leave(org_id):

    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button("log-out",variant="soft"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Leave organization"),
            rx.alert_dialog.description(
                "Are you sure? This organization will be accessible, however you will not have any role in it .",
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
                        "Leave Organization",
                        color_scheme="red",
                        variant="solid",
                        on_click= lambda: OrgState.leave_my_org(org_id)
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )