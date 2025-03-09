import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import pandas as pd  # Import pandas

load_dotenv()


def habit_tracker(prompt_text):
    """
    Sends the schedule prompt to the LLM model and returns the generated JSON output.
    """
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("DEEPSEEK_MODEL_API"),
        )

        completion = client.chat.completions.create(
            model="mistralai/mistral-small-24b-instruct-2501:free",
            messages=[{"role": "user", "content": prompt_text}],
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise e


def parse_output_to_df(llm_output):
    """
    Parses a list of JSON objects from the LLM output and converts them into a pandas DataFrame.
    
    Expected JSON format for each entry:
    {
        "output": {
            "activity": {
                "time": {
                    "from": "<start_time>",
                    "to": "<end_time>"
                },
                "ampm": "<AM/PM>",
                "category": "<category>"
            }
        }
    }
    
    The resulting DataFrame will have four columns: from, to, ampm, category.
    """
    # Remove extra label (e.g., "json" on the first line) if present.
    if llm_output.startswith("json"):
        llm_output = llm_output.split("\n", 1)[1].strip()

    try:
        data = json.loads(llm_output)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

    # Build a list of dictionaries that will be used for the DataFrame.
    rows_list = []
    for entry in data:
        activity = entry.get("output", {}).get("activity", {})
        time_info = activity.get("time", {})
        row = {
            "from": time_info.get("from", ""),
            "to": time_info.get("to", ""),
            "ampm": activity.get("ampm", ""),
            "category": activity.get("category", ""),
        }
        rows_list.append(row)

    # Create a DataFrame from the list of dictionaries.
    df = pd.DataFrame(rows_list)
    return df


if __name__ == "__main__":
    # Define the input schedule.
    input_schedule = """
    Time    Activity
    [6:00 - 6:30]   Wake up
    [6:30 - 7:00]   Morning stretch / light exercise
    [7:00 - 7:30]   Shower & freshen up
    [7:30 - 8:00]   Breakfast
    [8:00 - 8:30]   Plan the day / Check emails
    [8:30 - 12:30]  Work / Study
    [12:30 - 1:30]  Lunch break
    [1:30 - 4:00]   Resume work / Study
    [4:00 - 4:30]   Short break (walk, coffee, etc.)
    [4:30 - 6:30]   Continue work / Study
    [6:30 - 7:30]   Workout / Physical activity
    [7:30 - 8:00]   Shower & relax
    [8:00 - 8:30]   Dinner
    [8:30 - 10:00]  Leisure (reading, TV, hobby)
    [10:00 - 10:30] Wind down (meditation, journaling)
    [10:30 - 6:00]  Sleep
    """
    
    # Although not used directly in this snippet, category_list could serve for validation.
    category_list = ['wellness-physical', 'wellness-mental', 'work', 'chores', 'recreation', 'food', 'sleep', 'others']

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
    {input_schedule}
    
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
    
    # Option 1: To call the API, uncomment the following line:
    # llm_output = habit_tracker(prompt)
    
    # Option 2: For testing purposes, use a simulated output:
    llm_output = """json
[
    {
        "output": {
            "activity": {
                "time": {
                    "from": "6:00",
                    "to": "6:30"
                },
                "ampm": "AM",
                "category": "sleep"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "6:30",
                    "to": "7:00"
                },
                "ampm": "AM",
                "category": "wellness-physical"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "7:00",
                    "to": "7:30"
                },
                "ampm": "AM",
                "category": "wellness-physical"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "7:30",
                    "to": "8:00"
                },
                "ampm": "AM",
                "category": "food"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "8:00",
                    "to": "8:30"
                },
                "ampm": "AM",
                "category": "work"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "8:30",
                    "to": "12:30"
                },
                "ampm": "AM",
                "category": "work"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "12:30",
                    "to": "1:30"
                },
                "ampm": "PM",
                "category": "food"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "1:30",
                    "to": "4:00"
                },
                "ampm": "PM",
                "category": "work"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "4:00",
                    "to": "4:30"
                },
                "ampm": "PM",
                "category": "recreation"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "4:30",
                    "to": "6:30"
                },
                "ampm": "PM",
                "category": "work"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "6:30",
                    "to": "7:30"
                },
                "ampm": "PM",
                "category": "wellness-physical"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "7:30",
                    "to": "8:00"
                },
                "ampm": "PM",
                "category": "wellness-physical"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "8:00",
                    "to": "8:30"
                },
                "ampm": "PM",
                "category": "food"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "8:30",
                    "to": "10:00"
                },
                "ampm": "PM",
                "category": "recreation"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "10:00",
                    "to": "10:30"
                },
                "ampm": "PM",
                "category": "wellness-mental"
            }
        }
    },
    {
        "output": {
            "activity": {
                "time": {
                    "from": "10:30",
                    "to": "6:00"
                },
                "ampm": "next day",
                "category": "sleep"
            }
        }
    }
]
"""

    # Parse the output into a DataFrame using pandas.
    df = parse_output_to_df(llm_output)
    if df is not None:
        print("Resulting DataFrame:")
        print(df)
        # Optionally, save the DataFrame as a CSV file.
        df.to_csv("output_pandas.csv", index=False)
        print("CSV file 'output_pandas.csv' created using pandas.")
