import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def habit_tracker(input):
    
    try:
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("DEEPSEEK_MODEL_API"),
            )

        completion = client.chat.completions.create(
        model="mistralai/mistral-small-24b-instruct-2501:free",
        messages=[
            {
            "role": "user",
            "content": input
            }
        ]
        )
        print(completion)
        print("--------------------------")
        print(completion.choices[0].message.content)
    except Exception as e:
        raise(e)


input = """
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

category = ['wellness-physical', 'wellness-mental', 'work', 'chores', 'recreation', 'food', 'sleep', 'others']

prompt = f"""
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



habit_tracker(prompt)