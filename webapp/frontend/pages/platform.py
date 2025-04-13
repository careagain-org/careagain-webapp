import reflex as rx
from .platform_base import platform_base
from ..constants import urls
from ..components.project_card import project_grid_horizontal
from ..components.user_card import users_grid_horizontal
from ..components.org_card import org_grid_horizontal
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
                project_grid_horizontal(ProjectState.projects,cols=6,rows=1),
                # section_title("square-play",'Videos', urls.VIDEOS_URL),
                # section_title("store",'Market', urls.PLATFORM_URL),
                section_title("users",'Community', urls.COMMUNITY_PLATFORM),
                users_grid_horizontal(UserState.users,cols=6,rows=1),
                # org_grid_horizontal(OrgState.orgs,cols=6,rows=1),
                align = "start",
                justify="start",
                width ="80vw",
                spacing="2",
                on_mount=[ProjectState.get_list_projects,UserState.get_users,OrgState.get_orgs]
    )
    return platform_base(home)