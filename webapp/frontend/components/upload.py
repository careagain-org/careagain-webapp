import reflex as rx
import base64


class ImageUpload(rx.ComponentState):
    """Per-instance state for an image upload square."""

    image_data: str = ""
    image_name: str = ""
    is_uploading: bool = False
    error_message: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.error_message = ""
        self.is_uploading = True
        yield

        if not files:
            self.error_message = "No file selected."
            self.is_uploading = False
            return

        file = files[0]
        file_name = file.filename
        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        content_type = getattr(file, "content_type", "") or ""

        if not content_type:
            ext = file_name.rsplit(".", 1)[-1].lower()
            ext_map = {
                "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "png": "image/png", "gif": "image/gif", "webp": "image/webp",
            }
            content_type = ext_map.get(ext, "")

        if content_type not in allowed_types:
            self.error_message = "Please upload a valid image (JPEG, PNG, GIF, WEBP)."
            self.is_uploading = False
            return

        data = await file.read()
        encoded = base64.b64encode(data).decode("utf-8")
        self.image_data = f"data:{content_type};base64,{encoded}"
        self.image_name = file_name
        self.is_uploading = False
        
        # Save to disk via rx.get_upload_dir()
        outfile = rx.get_upload_dir() / file_name
        with outfile.open("wb") as f:
            f.write(data)
        
        self.is_uploading = False
        

    def clear_image(self):
        self.image_data = ""
        self.image_name = ""
        self.error_message = ""
        

    @classmethod
    def get_component(cls, *args, **kwargs) -> rx.Component:
        # Each call to ImageUpload.create() gets its own upload_id
        upload_id = f"upload_{cls.get_name()}"

        return rx.vstack(
            # ── Square ───────────────────────────────────────────────
            rx.upload(
                rx.cond(
                    cls.image_data == "",
                    # Empty state
                    rx.vstack(
                        rx.cond(
                            cls.is_uploading,
                            rx.spinner(size="3", color="teal"),
                            rx.vstack(
                                rx.icon("image", size=40, color="teal"),
                                rx.text(
                                    "Drop image here",
                                    font_size="0.9rem",
                                    font_weight="600",
                                    color="teal",
                                    letter_spacing="0.05em",
                                ),
                                rx.text(
                                    "or click to browse",
                                    font_size="0.75rem",
                                    color="#94a3b8",
                                ),
                                spacing="1",
                                align="center",
                            ),
                        ),
                        align="center",
                        justify="center",
                        width="100%",
                        height="100%",
                    ),
                    # Filled state
                    rx.image( src=cls.image_data,
                             width="100%",
                             align="center",
                        justify="center",
                        ),
                ),
                id=upload_id,
                accept={
                    "image/png": [".png"],
                    "image/jpeg": [".jpg", ".jpeg"],
                    "image/gif": [".gif"],
                    "image/webp": [".webp"],
                },
                max_files=1,
                on_drop=cls.handle_upload(rx.upload_files(upload_id=upload_id)),
                padding="0",
                margin="0",
                line_height="0",
                font_size="0",      # ← this is often the hidden culprit for inline spacing
                display="block",    # ← makes the upload div behave as block, not inline
                width="17rem",
                height=rx.cond(
                    cls.image_data == "",
                    "16rem",
                    "100%",
                ),
                border=rx.cond(
                    cls.image_data == "",
                    "2px dashed #008080",
                    "2px solid #008080",
                ),
                border_radius="12px",
                cursor="pointer",
                background="transparent",
                overflow="hidden",
                transition="all 0.2s ease",
                _hover={
                    "border_color": "teal",
                    "background": rx.cond(
                        cls.image_data == "",
                        "#b2d8d8",
                        "transparent",
                    ),
                    "opacity": 0.5,
                },
            ),
            # ── Error ─────────────────────────────────────────────────
            rx.cond(
                cls.error_message != "",
                rx.callout(
                    cls.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="16rem",
                ),
            ),
            # ── Filename + clear ──────────────────────────────────────
            rx.cond(
                cls.image_name != "",
                rx.hstack(
                    rx.text(
                        cls.image_name,
                        color="#475569",
                        font_size="0.8rem",
                        max_width="12rem",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    rx.button(
                        "Remove",
                        on_click=cls.clear_image,
                        size="1",
                        variant="soft",
                        color_scheme="red",
                        cursor="pointer",
                        type="button",
                    ),
                    align="center",
                    spacing="3",
                    width="100%",
                    height="100%",
                    justify="center",
                ),
            ),
            spacing="1",
            align="center",
            **kwargs,
            
        )
