from models.llm_model import HabitTrackerLLM
from utils.parser import parse_llm_output
from config import DAILY_SCHEDULE_PROMPT
from utils.logger import get_logger


logger = get_logger("tracker_service")

class TrackerService:
    # Takes user input for a day, categorize the tasks using LLM, save the output to DB.
    def __init__(self):
        pass
    

    def categorize_schedule(self, schedule_text: str):
        logger.info("Preparing prompt for LLM.")
        llm = HabitTrackerLLM()
        prompt = DAILY_SCHEDULE_PROMPT.format(input=schedule_text)

        try:
            llm_output = llm.get_categories(prompt)
            logger.debug(f"LLM Raw Output: {llm_output}")
        except Exception as e:
            logger.exception("LLM call failed.")
            raise e

        structured_result = parse_llm_output(llm_output)
        logger.info("Parsed structured output successfully.")
        return structured_result

    def save_category_to_database(self, structured_result):
        """
        input: structured_result
        process: save the structured result in DB
        output: No output
        log: Log success/failure message
        """
        pass

        # activity - small case, check in activity table
        # just get acitivty id
        # if not, create new row in activity table, get category_id with the help of category_name and add category_id to the activity table
        # update user activity table with new daily task
    

    def categorize_and_save_to_db():
        # call categorize_schedule and save_category_to_database
        # get final output
        pass


