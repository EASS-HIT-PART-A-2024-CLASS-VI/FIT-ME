import google.generativeai as genai
from typing import Optional
from .config.settings import settings
from .prompt_templates import PromptTemplates

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
    async def get_response(self, 
                          prompt: str, 
                          context: Optional[str] = None) -> str:
        try:
            chat = self.model.start_chat(history=[])
            system_prompt = PromptTemplates.get_system_prompt()
            
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}" if context else f"{system_prompt}\n\nQuestion: {prompt}"
            
            response = chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
