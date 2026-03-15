import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict , Optional

class QuestionState(rx.State):
    questions: List[Dict[str, str]] = []
    token:Optional[str]=rx.Cookie(
                name="__session",
                max_age =60,
            ) 

    async def get_list_questions(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/questions/",
            )
        
        if response.status_code == 200:
            self.questions = response.json()

        
    
