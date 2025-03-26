import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict 

class QuestionState(rx.State):
    questions: List[Dict[str, str]] = []

    async def get_list_questions(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/questions/",
            )
        
        if response.status_code == 200:
            self.questions = response.json()

        
    
