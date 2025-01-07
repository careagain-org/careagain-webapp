import reflex as rx
from ..states.upload_state import UploadState

def upload_image(title:str) -> rx.Component():
    return rx.vstack(
        rx.text(
            title,
            as_="div",
            size="2",
            margin_bottom="4px",
            weight="bold",
        ),
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    bg="white",
                    border=f"1px solid",
                ),
                rx.text("Drag and drop files here \n or click to select files"),
                align="center",
                justify="center"),
            radius="full",
            border="1px dotted rgb(0,0,0)",
            padding="5em",
            spacing="2",
            height="100%",
            id="my_upload",
            multiple=False,
            accept = {
                "application/pdf": [".pdf"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/gif": [".gif"],
                "image/webp": [".webp"],
                "text/html": [".html", ".htm"],
            },
            on_click=UploadState.handle_upload(rx.upload_files(upload_id="my_upload")),
            on_drop=UploadState.handle_upload(rx.upload_files(upload_id="my_upload")),
        ),
    )