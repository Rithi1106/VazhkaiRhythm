import json
import re
import csv
from utils.logger import get_logger

logger = get_logger(__name__)

def parse_llm_output(llm_output: str):
    try:
        # Extract only the JSON array part using regex
        match = re.search(r"\[\s*{.*?}\s*]", llm_output, re.DOTALL)
        if not match:
            logger.error("No valid JSON array found in LLM output.")
            return []

        json_str = match.group(0)
        parsed_json = json.loads(json_str)

        logger.info("Parsed LLM output successfully.")
        return parsed_json  # This returns list of dicts, as expected

    except Exception as e:
        logger.error(f"Parsing Error: {e}")
        return []
