import re
from pydantic import BaseModel, validator
from typing import Optional

class DecisionOutput(BaseModel):
    reasoning: str
    decision: int

    @validator('decision', pre=True, always=True)
    def extract_last_number(cls, v, values):
        reasoning = values.get('reasoning', '')
        # Match the last integer in the entire reasoning string
        match = re.search(r'\b\d+\b', reasoning[::-1])
        if match:
            return int(match.group(0)[::-1])
        raise ValueError("No valid integer found in the response.")
    

import re

def get_last_number(text: str) -> Optional[int]:
    """
    Extracts the last standalone integer from the given text.
    
    Args:
        text (str): The raw output from the LLM.

    Returns:
        Optional[int]: The last number found, or None if none found.
    """
    # Find all numbers in the text
    matches = re.findall(r'\b\d+\b', text)
    if matches:
        try:
            return int(matches[-1])
        except (ValueError, IndexError):
            return None
    return None


if __name__ == "__main__":
    response = """
    I received a random value of [3]. Since I want to follow a randomized strategy,
    and 3 is less than half of 6, I will pick 5 as my choice.

    Final Decision: 5pp
    """

    # Or this variant:
    response2 = "Based on the RNG, I choose 6 now. 6 asdf"

    print(get_last_number(response))
    print(get_last_number(response2))