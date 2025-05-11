import reflex as rx
from .platform_base import platform_base
from ..constants import urls
from ..components.project_card import project_scroll_horizontal
from ..components.user_card import users_scroll_horizontal
from ..components.org_card import org_scroll_horizontal
from ..states.project_state import ProjectState
from ..states.question_state import QuestionState
from ..states.org_state import OrgState
from ..states.user_state import UserState

def section_title(section_icon:str,section_title:str, section_link:str): # type: ignore
    return rx.hstack(
        rx.icon(section_icon,color = "teal"),
        rx.heading(section_title,size="5", color = "teal"),
        rx.link(f"Go to {section_title}",href=section_link),
        spacing = "5",
        color = "accent",
    )

@rx.page(route=urls.PLATFORM_URL)
def platform_home() -> rx.Component:
    home = rx.vstack(
                rx.heading('Most recent', size="5"),
                section_title("square-library",'Projects', urls.PROJECTS_URL),
                project_scroll_horizontal(ProjectState.projects),
                # section_title("square-play",'Videos', urls.VIDEOS_URL),
                # section_title("store",'Market', urls.PLATFORM_URL),
                section_title("users",'Users', urls.COMMUNITY_PLATFORM),
                users_scroll_horizontal(UserState.users),
                section_title("building-2",'Organizations/Institutions', urls.COMMUNITY_PLATFORM),
                org_scroll_horizontal(OrgState.orgs),
                align = "start",
                justify="start",
                # width ="80vw",
                spacing="2",
                on_mount=[ProjectState.get_list_projects,UserState.get_users,OrgState.get_orgs]
    )
    return platform_base(home)