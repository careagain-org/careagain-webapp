import reflex as rx

# class Dropdown(rx.ComponentState):
#     verified: str = "All"
#     type_site: str = "All"
#     type_medical_equipment: str = "All"


def dropdown_select(label, items, value, on_change):
    return rx.flex(
        rx.text(label),
        rx.select.root(
            rx.select.trigger(),
            rx.select.content(
                *[
                    rx.select.item(item, value=item)
                    for item in items
                ]
            ),
            value=value,
            on_change=on_change,
        ),
        align="center",
        justify="center",
        direction="column",
    )


# def selectors():
#     return rx.flex(
#         dropdown_select(
#             "Verified sites",
#             ["All", "Verified", "Non-verifies"],
#             SelectorsState.verified,
#             SelectorsState.set_verified,
#         ),
#         dropdown_select(
#             "Type of site",
#             [
#                 "All",
#                 "ONG intermediate",
#                 "Builder/Manufacturer",
#                 "Designer",
#                 "Hospital/Clinic",
#                 "Maintainer",
#                 "Trasnportation",
#             ],
#             SelectorsState.type_site,
#             SelectorsState.set_type_site,
#         ),
#         dropdown_select(
#             "Type of Medical Equipment",
#             [
#                 "All",
#                 "Incubator",
#                 "Respirator",
#                 "CPAP",
#                 "Wheelchair",
#             ],
#             SelectorsState.type_medical_equipment,
#             SelectorsState.set_type_medical_equipment,
#         ),
#         width="100%",
#         spacing="2",
#         justify="between",
#     )
