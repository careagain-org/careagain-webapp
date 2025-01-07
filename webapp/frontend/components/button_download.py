import reflex as rx

def button_download(url_path:str,filename:str)-> rx.Component:
    rx.button(
        "Download",
        on_click=rx.download(
            url=url_path,
            filename=filename,
        ),
        id="download_button",
    )