PROMPT_VERSION = "v1"

DAILY_SCHEDULE_PROMPT = """
            ### **Task: Categorize Activities from a Daily Schedule** ###

            #### **Instructions:**
            You are given a list of daily activities with time slots. Your goal is to classify each activity into a predefined category and format the output in structured JSON.

            ---

            ### **Categories & Definitions:**
            - **wellness-physical** → Activities involving movement (e.g., stretching, workout, shower).
            - **wellness-mental** → Activities for mental well-being (e.g., meditation, journaling).
            - **work** → Professional tasks, job-related activities, or study.
            - **chores** → Household or routine tasks (e.g., cleaning, organizing).
            - **recreation** → Leisure activities (e.g., reading, watching TV, hobbies).
            - **food** → Activities related to eating or meal preparation.
            - **sleep** → Time allocated for sleeping or resting.
            - **others** → Activities that do not fit into the above categories.

            ---

            ### **Input Schedule:**
            {input}

            ---

            ### **Expected Output Format:**
            For each activity, return a JSON object in the following format:

            ```json
                {{
                    "output": {{
                        "activity": {{
                            "time": {{
                                "from": "<start_time>",
                                "to": "<end_time>"
                            }},
                            "ampm": "<AM/PM>",
                            "category": "<category>"
                        }}
                    }}
                }}
        """