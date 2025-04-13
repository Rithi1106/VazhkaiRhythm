import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class HabitTrackerLLM:
    def __init__(self):
        try:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("DEEPSEEK_MODEL_API")
            )
            self.model_name = "mistralai/mistral-small-24b-instruct-2501:free"
            logger.info("HabitTrackerLLM initialized successfully.")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise

    def get_categories(self, prompt: str):
        try:
            logger.debug(f"Sending prompt to LLM")  # Log a truncated version
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("Received response from LLM.")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error while calling LLM: {e}")
            raise
