import reflex as rx

def create_stylesheet_link(stylesheet_url):
    """Create a link element for a stylesheet."""
    return rx.el.link(href=stylesheet_url, rel="stylesheet")


def create_hover_link(link_url, link_text):
    """Create a link element with hover effect."""
    return rx.el.a(
        link_text,
        href=link_url,
        _hover={"color": "#3B82F6"},
        color="#4B5563",
    )


def create_section_heading(heading_text):
    """Create a section heading with specific styling."""
    return rx.heading(
        heading_text,
        font_weight="600",
        margin_bottom="0.5rem",
        text_align="center",
        font_size="1.25rem",
        line_height="1.75rem",
        as_="h3",
    )


def create_main_heading(heading_text):
    """Create a main heading with specific styling."""
    return rx.heading(
        heading_text,
        font_weight="700",
        margin_bottom="2rem",
        font_size="1.875rem",
        line_height="2.25rem",
        text_align="center",
        as_="h2",
    )


def create_styled_image(image_alt, image_src):
    """Create an image element with specific styling."""
    return rx.image(
        src=image_src,
        alt=image_alt,
        border_radius="0.5rem",
        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    )


def create_responsive_image_box(image_alt, image_src):
    """Create a responsive box containing a styled image."""
    return rx.box(
        create_styled_image(
            image_alt=image_alt, image_src=image_src
        ),
        margin_bottom=rx.breakpoints(
            {"0px": "2rem", "768px": "0"}
        ),
        width=rx.breakpoints({"768px": "50%"}),
    )


def create_styled_text(
    font_size, margin_bottom, text_content
):
    """Create a text element with custom styling."""
    return rx.text(
        text_content,
        margin_bottom=margin_bottom,
        color="#374151",
        font_size=font_size,
        line_height="1.75rem",
    )


def create_colored_icon(icon_color, icon_tag):
    """Create a colored icon element."""
    return rx.icon(
        tag=icon_tag,
        height="1.5rem",
        margin_right="0.5rem",
        color=icon_color,
        width="1.5rem",
    )


def create_colored_span(span_text):
    """Create a span element with specific color."""
    return rx.text.span(span_text, color="#374151")


def create_icon_text_flex(text_content):
    """Create a flex container with an icon and text."""
    return rx.flex(
        create_colored_icon(
            icon_color="#10B981", icon_tag="check-circle"
        ),
        create_colored_span(span_text=text_content),
        display="flex",
        align_items="center",
        margin_top="0.5rem",
    )


def create_centered_icon(icon_tag):
    """Create a centered icon with specific styling."""
    return rx.icon(
        tag=icon_tag,
        height="3rem",
        margin_bottom="1rem",
        margin_left="auto",
        margin_right="auto",
        color="#EF4444",
        width="3rem",
    )


def create_centered_text(text_content):
    """Create centered text with specific styling."""
    return rx.text(
        text_content, text_align="center", color="#374151"
    )


def create_feature_box(
    icon_tag, heading_text, description_text
):
    """Create a feature box with an icon, heading, and description."""
    return rx.box(
        create_centered_icon(icon_tag=icon_tag),
        create_section_heading(heading_text=heading_text),
        create_centered_text(text_content=description_text),
        background_color="#ffffff",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_list_item_with_icon(icon_tag, item_text):
    """Create a list item with an icon and text."""
    return rx.el.li(
        create_colored_icon(
            icon_color="#3B82F6", icon_tag=icon_tag
        ),
        create_colored_span(span_text=item_text),
        display="flex",
        align_items="center",
    )


def create_simple_icon(icon_tag):
    """Create a simple icon element."""
    return rx.icon(
        tag=icon_tag, height="1.5rem", width="1.5rem"
    )


def create_social_link(icon_tag):
    """Create a social media link with an icon."""
    return rx.el.a(
        create_simple_icon(icon_tag=icon_tag),
        href="#",
        _hover={"color": "#3B82F6"},
    )


def create_logo_and_name():
    """Create a flex container with logo and company name."""
    return rx.flex(
        rx.image(
            src="https://replicate.delivery/xezq/MOukO1jd8wKSMxA00ijf87FVF7cTZTLH8Esxoj6yM4KsQz3JA/out-0.webp",
            alt="OpenMed Devices Logo",
            height="2.5rem",
            margin_right="0.75rem",
            width="2.5rem",
        ),
        rx.text.span(
            "OpenMed Devices",
            font_weight="600",
            color="#1F2937",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        display="flex",
        align_items="center",
    )


def create_get_started_button():
    """Create a 'Get Started' button with specific styling."""
    return rx.el.a(
        "Get Started",
        href="#join",
        background_color="#3B82F6",
        transition_duration="300ms",
        _hover={"background-color": "#2563EB"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.5rem",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_header():
    """Create the header section with logo, navigation, and button."""
    return rx.flex(
        create_logo_and_name(),
        rx.box(
            create_hover_link(
                link_url="#about", link_text="About"
            ),
            create_hover_link(
                link_url="#problem", link_text="Problem"
            ),
            create_hover_link(
                link_url="#solution", link_text="Solution"
            ),
            create_hover_link(
                link_url="#join", link_text="Join Us"
            ),
            display=rx.breakpoints(
                {"0px": "none", "768px": "flex"}
            ),
            column_gap="1.5rem",
        ),
        create_get_started_button(),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        display="flex",
        align_items="center",
        justify_content="space-between",
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
    )


def create_join_community_button():
    """Create a 'Join the Community' button with specific styling."""
    return rx.el.a(
        "Join the Community",
        href="#join",
        background_color="#ffffff",
        transition_duration="300ms",
        font_weight="600",
        _hover={"background-color": "#F3F4F6"},
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        color="#3B82F6",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_hero_section():
    """Create the hero section with heading, text, and button."""
    return rx.box(
        rx.heading(
            "Revolutionizing Medical Device Development",
            font_weight="700",
            margin_bottom="1rem",
            font_size=rx.breakpoints(
                {"0px": "2.25rem", "768px": "3rem"}
            ),
            line_height=rx.breakpoints(
                {"0px": "2.5rem", "768px": "1"}
            ),
            as_="h1",
        ),
        rx.text(
            "Join our open source community to create accessible and affordable medical devices for all.",
            margin_bottom="2rem",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        create_join_community_button(),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
        text_align="center",
    )


def create_about_text_section():
    """Create the text section for the About component."""
    return rx.box(
        create_styled_text(
            font_size="1.125rem",
            margin_bottom="1rem",
            text_content="OpenMed Devices is a pioneering platform that brings together innovators, engineers, and healthcare professionals to collaboratively develop open source medical devices.",
        ),
        create_styled_text(
            font_size="1.125rem",
            margin_bottom="1rem",
            text_content="Our mission is to democratize medical technology and make it accessible to everyone, everywhere.",
        ),
        rx.flex(
            create_colored_icon(
                icon_color="#10B981",
                icon_tag="check-circle",
            ),
            create_colored_span(
                span_text="Foster innovation in healthcare"
            ),
            display="flex",
            align_items="center",
        ),
        create_icon_text_flex(
            text_content="Reduce costs of medical devices"
        ),
        create_icon_text_flex(
            text_content="Improve global healthcare access"
        ),
        padding_left=rx.breakpoints({"768px": "3rem"}),
        width=rx.breakpoints({"768px": "50%"}),
    )


def create_about_section():
    """Create the complete About section with image and text."""
    return rx.box(
        create_main_heading(
            heading_text="About OpenMed Devices"
        ),
        rx.flex(
            create_responsive_image_box(
                image_alt="Collaborative team working on medical devices",
                image_src="https://replicate.delivery/xezq/G9RtQiUYwwoeSa2kKYBbhpfeSWuWTa8LeKD8HWfjMlRIL08dC/out-0.webp",
            ),
            create_about_text_section(),
            display="flex",
            flex_direction=rx.breakpoints(
                {"0px": "column", "768px": "row"}
            ),
            align_items="center",
            justify_content="space-between",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
    )


def create_problem_section():
    """Create the Problem section with multiple feature boxes."""
    return rx.box(
        create_main_heading(
            heading_text="The Problem We're Solving"
        ),
        rx.box(
            create_feature_box(
                icon_tag="dollar-sign",
                heading_text="High Costs",
                description_text="Medical devices are often prohibitively expensive, limiting access to essential healthcare technologies.",
            ),
            create_feature_box(
                icon_tag="lock",
                heading_text="Limited Access",
                description_text="Many regions lack access to crucial medical devices, creating disparities in healthcare quality.",
            ),
            create_feature_box(
                icon_tag="frown",
                heading_text="Slow Innovation",
                description_text="Closed development processes hinder rapid innovation and improvement of medical devices.",
            ),
            gap="2rem",
            display="grid",
            grid_template_columns=rx.breakpoints(
                {
                    "0px": "repeat(1, minmax(0, 1fr))",
                    "768px": "repeat(3, minmax(0, 1fr))",
                }
            ),
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
    )


def create_solution_text_section():
    """Create the text section for the Solution component."""
    return rx.box(
        rx.heading(
            "Open Source Collaboration Platform",
            font_weight="600",
            margin_bottom="1rem",
            font_size="1.5rem",
            line_height="2rem",
            as_="h3",
        ),
        create_styled_text(
            font_size="1.125rem",
            margin_bottom="1rem",
            text_content="Our platform empowers a global community to collaboratively develop, improve, and share medical device designs.",
        ),
        rx.list(
            create_list_item_with_icon(
                icon_tag="users",
                item_text="Connect with experts worldwide",
            ),
            create_list_item_with_icon(
                icon_tag="code",
                item_text="Access open source designs and code",
            ),
            create_list_item_with_icon(
                icon_tag="tool",
                item_text="Collaborate on prototypes and testing",
            ),
            create_list_item_with_icon(
                icon_tag="share-2",
                item_text="Share knowledge and resources",
            ),
            display="flex",
            flex_direction="column",
            gap="0.5rem",
        ),
        padding_left=rx.breakpoints({"768px": "3rem"}),
        width=rx.breakpoints({"768px": "50%"}),
    )


def create_solution_section():
    """Create the complete Solution section with image and text."""
    return rx.box(
        create_main_heading(heading_text="Our Solution"),
        rx.flex(
            create_responsive_image_box(
                image_alt="Open source medical device prototypes",
                image_src="https://replicate.delivery/xezq/eBjomg9CQ61sI64cIyfTQUJ2Zfd5BWqf4eMYBnvRMUKFL08dC/out-0.webp",
            ),
            create_solution_text_section(),
            display="flex",
            flex_direction=rx.breakpoints(
                {"0px": "column", "768px": "row"}
            ),
            align_items="center",
            justify_content="space-between",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
    )


def create_email_input():
    """Create an email input field with specific styling."""
    return rx.el.input(
        type="email",
        placeholder="Enter your email",
        border_width="1px",
        border_color="#D1D5DB",
        _focus={
            "outline-style": "none",
            "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
            "--ring-color": "#3B82F6",
        },
        margin_bottom="1rem",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.5rem",
        width="100%",
    )


def create_submit_button():
    """Create a submit button with specific styling."""
    return rx.el.button(
        "Get Started",
        type="submit",
        background_color="#3B82F6",
        transition_duration="300ms",
        font_weight="600",
        _hover={"background-color": "#2563EB"},
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
    )


def create_join_section():
    """Create the Join section with heading, text, and form."""
    return rx.box(
        rx.heading(
            "Join Our Community",
            font_weight="700",
            margin_bottom="2rem",
            font_size="1.875rem",
            line_height="2.25rem",
            as_="h2",
        ),
        create_styled_text(
            font_size="1.25rem",
            margin_bottom="2rem",
            text_content="Be part of the revolution in medical device development. Together, we can make a real impact on global healthcare.",
        ),
        rx.form(
            create_email_input(),
            create_submit_button(),
            max_width="28rem",
            margin_left="auto",
            margin_right="auto",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
        text_align="center",
    )


def create_main_content():
    """Create the main content sections of the page."""
    return rx.box(
        rx.box(
            create_hero_section(),
            id="hero",
            class_name="bg-gradient-to-r from-blue-500 to-purple-600",
            padding_top="5rem",
            padding_bottom="5rem",
            color="#ffffff",
        ),
        rx.box(
            create_about_section(),
            id="about",
            background_color="#ffffff",
            padding_top="4rem",
            padding_bottom="4rem",
        ),
        rx.box(
            create_problem_section(),
            id="problem",
            background_color="#F3F4F6",
            padding_top="4rem",
            padding_bottom="4rem",
        ),
        rx.box(
            create_solution_section(),
            id="solution",
            background_color="#ffffff",
            padding_top="4rem",
            padding_bottom="4rem",
        ),
        rx.box(
            create_join_section(),
            id="join",
            background_color="#F3F4F6",
            padding_top="4rem",
            padding_bottom="4rem",
        ),
    )


def create_footer_logo():
    """Create the logo section for the footer."""
    return rx.box(
        rx.image(
            src="https://replicate.delivery/xezq/MOukO1jd8wKSMxA00ijf87FVF7cTZTLH8Esxoj6yM4KsQz3JA/out-0.webp",
            alt="OpenMed Devices Logo",
            height="2.5rem",
            display="inline-block",
            margin_right="0.5rem",
            width="2.5rem",
        ),
        rx.text.span(
            "OpenMed Devices",
            font_weight="600",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        margin_bottom=rx.breakpoints(
            {"0px": "1.5rem", "768px": "0"}
        ),
        text_align=rx.breakpoints(
            {"0px": "center", "768px": "left"}
        ),
        width=rx.breakpoints(
            {"0px": "100%", "768px": "33.333333%"}
        ),
    )


def create_footer_content():
    """Create the content for the footer including logo, copyright, and social links."""
    return rx.flex(
        create_footer_logo(),
        rx.box(
            rx.text(
                "© 2023 OpenMed Devices. All rights reserved."
            ),
            margin_bottom=rx.breakpoints(
                {"0px": "1.5rem", "768px": "0"}
            ),
            text_align="center",
            width=rx.breakpoints(
                {"0px": "100%", "768px": "33.333333%"}
            ),
        ),
        rx.flex(
            create_social_link(icon_tag="facebook"),
            create_social_link(icon_tag="twitter"),
            create_social_link(icon_tag="linkedin"),
            create_social_link(icon_tag="github"),
            display="flex",
            justify_content=rx.breakpoints(
                {"0px": "center", "768px": "flex-end"}
            ),
            column_gap="1rem",
            width=rx.breakpoints(
                {"0px": "100%", "768px": "33.333333%"}
            ),
        ),
        display="flex",
        flex_wrap="wrap",
        align_items="center",
        justify_content="space-between",
    )


def create_footer():
    """Create the complete footer section."""
    return rx.box(
        rx.box(
            create_footer_content(),
            width="100%",
            style=rx.breakpoints(
                {
                    "640px": {"max-width": "640px"},
                    "768px": {"max-width": "768px"},
                    "1024px": {"max-width": "1024px"},
                    "1280px": {"max-width": "1280px"},
                    "1536px": {"max-width": "1536px"},
                }
            ),
            margin_left="auto",
            margin_right="auto",
            padding_left="1.5rem",
            padding_right="1.5rem",
        ),
        background_color="#1F2937",
        padding_top="2rem",
        padding_bottom="2rem",
        color="#ffffff",
    )


def create_page_layout():
    """Create the overall page layout including styles, header, main content, and footer."""
    return rx.fragment(
        create_stylesheet_link(
            stylesheet_url="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
        ),
        create_stylesheet_link(
            stylesheet_url="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
        ),
        rx.el.style(
            """
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """
        ),
        rx.box(
            rx.box(
                create_header(),
                background_color="#ffffff",
                box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            ),
            create_main_content(),
            create_footer(),
            class_name="font-['Poppins']",
            background_color="#F3F4F6",
        ),
    )