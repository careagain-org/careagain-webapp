import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

vm = os.getenv("VIRTUAL_MACHINE_IP")
BACKEND_PORT = os.getenv("BACKEND_PORT")
FRONTEND_PORT= os.getenv("FRONTEND_PORT")
API_URL = os.getenv("API_URL")

HOME_URL = '/'
ABOUT_URL = '/#home_logo'
PROBLEM_URL = '/#problem_section'
SOLUTION_URL = '/#solution_section'
COMMUNITY_URL = '/#community_section'
CONTACT_URL = '/#contact_section'
LOGIN_URL = '/login'
SIGNUP_URL = '/signup'
LOGOUT_URL = '/logout'
RESET_PASSWORD_URL = '/reset_password'

EMAIL = 'hello@careagain.org'

# platform
PLATFORM_URL = '/platform'
PROJECTS_URL = '/projects'
IND_PROJECT_URL = '/project_view'
IND_ORG_URL = '/org_view'
IND_USER_URL = '/user_view'
IND_EDIT_PROJECT_URL = '/project_edit'
IND_EDIT_ORG_URL = '/org_edit'
PROFILE_URL = '/profile'
PROFILE_ORG_URL = '/profile#my-organizations'
PROFILE_PROJECT_URL = '/profile#my-projects'
VIDEOS_URL = '/videos'
COMMUNITY_PLATFORM = '/community'
QUESTIONS_URL = '/questions'

REPORT_URL = 'https://forms.gle/a1PLLGNF6EqNNCq16'
FEEDBACK_URL = 'https://forms.gle/ioBqakXyaSY4Nz7Y8'

# social media
YOUTUBE_URL = "https://www.youtube.com/@care-again-org"
GITHUB_URL = "https://github.com/careagain-org/careagain-webapp/"
LINKEDIN_URL = "https://linkedin.com/company/care-again"
DISCORD_URL = "https://discord.gg/FJfJWrpZTq" 
PATREON_URL = "https://patreon.com/CareAgain" 


# api
WEB_URL = f"http://localhost:{FRONTEND_PORT}"
STORAGE_URL = 'http://0.0.0.0:9000/'