import reflex as rx
from ..constants import urls

class NavState(rx.State):
    def to_home(self):
        return rx.redirect(urls.HOME_URL)

    def to_about_us(self):
        return rx.redirect(urls.ABOUT_URL)

    def to_problem(self):
        return rx.redirect(urls.PROBLEM_URL)

    def to_solution(self):
        return rx.redirect(urls.SOLUTION_URL)

    def to_community(self):
        return rx.redirect(urls.COMMUNITY_URL)

    def to_contact(self):
        return rx.redirect(urls.CONTACT_URL)
    
    def to_login(self):
        return rx.redirect(urls.LOGIN_URL)
    
    def to_signup(self):
        return rx.redirect(urls.SIGNUP_URL)
    
    def to_platfom(self):
        return rx.redirect(urls.PLATFORM_URL)
    
    def to_profile(self):
        return rx.redirect(urls.PROFILE_URL)
    