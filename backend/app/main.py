from service.tracker_service import TrackerService
from utils.logger import get_logger

logger = get_logger("main")

sample_input = """
Time	Activity
[6:00 - 6:30]	Wake up
[6:30 - 7:00]	Morning stretch / light exercise
[7:00 - 7:30]	Shower & freshen up
[7:30 - 8:00]	Breakfast
[8:00 - 8:30]	Plan the day / Check emails
[8:30 - 12:30]	Work / Study
[12:30 - 1:30]	Lunch break
[1:30 - 4:00]	Resume work / Study
[4:00 - 4:30]	Short break (walk, coffee, etc.)
[4:30 - 6:30]	Continue work / Study
[6:30 - 7:30]	Workout / Physical activity
[7:30 - 8:00]	Shower & relax
[8:00 - 8:30]	Dinner
[8:30 - 10:00]	Leisure (reading, TV, hobby)
[10:00 - 10:30]	Wind down (meditation, journaling)
[10:30 - 6:00]	Sleep
"""

if __name__ == "__main__":
    logger.info("Starting schedule categorization.")
    try:
        results = TrackerService.categorize_and_save_to_db(sample_input)
        logger.info("Categorization successful.")
        print(results)
    except Exception as e:
        logger.exception("Error occurred during categorization.")
