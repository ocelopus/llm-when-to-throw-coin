import openai

config1 = {
    "agent_model_name": ["doubao-1-5-pro-256k-250115", "doubao-1-5-pro-256k-250115"],
    "total_trials": 10,
    "horses_per_player": 7,
    "optional_cot_prompt": "Please think carefully about how to win. For example, you may try to conjecture what other players are thinking about.",
    "timeout_seconds": 100,
    "random_seed": 12345,
    "top_p": openai.NOT_GIVEN,
    "temperature": openai.NOT_GIVEN,

    "system_background": 
"""You are {agent_name} participating in a {player_count}-player strategic game inspired by the ancient Chinese story of Tian Ji's Horse Racing. In this game, each player has N horses with speeds ranked from 0 to N-1. In each round, all players secretly and simultaneously choose one horse to race. The horse with the higher speed wins that round.

Game Rules:
- You have a set horses with speeds [0, 1, 2, ..., N-1]. Each players have the same set of horses.
- Each round, select one of your horse to race. This horse is then removed from your set of available horses.
- The outcome depends on the relative speeds of the selected horses. Players with the fastest speed equally divide the 1.0 reward.
- Opponents simultaneously make choices in each round, unlike King Qi whose strategy across the whole tournament is known. 
- You can see the results of previous rounds. However, you need to remember what your opponent have selected.
- A private random choice from the available horses will be given to you each round inside square brackets: [random_horse_choice]. If you decide to go random, use the random choice.
- One tournament ends after N rounds when every horse is spent.
The player(s) with the highest sum of rewards across all rounds wins this tournament. All other player(s) loses.
You may play for many tournaments with your opponent(s). However, rewards from different tournaments  doesn't sum.
Each round, you will receive:
- Horse speeds available to you.
- Optional: Information of the last round.
- A private random choice enclosed in [ ].
{optional_cot_prompt}
At the very end of your response, write only the choice you choose, and nothing else.  
Do not include any text after the final choice.
""",

    "current_state_prompt":
"""
---
{infos}
Begins {round_number} round!
New random choice: [{random_value}]
Remaining Valid horse to choose: {horses_still_avaliable}
Response:""",


    "end_state_prompt":
"""
{infos}
{win_str}
A new tournament with the same opponent(s) begins!
"""

}


config2 = config1.copy()


config2["agent_model_name"] = ["deepseek-r1-250120", "deepseek-r1-250120"]
config2["timeout_seconds"] = 1000



config3 = config2.copy()


config3["agent_model_name"] = ["gpt-4.1-mini-2025-04-14", "gpt-4.1-2025-04-14"]


config4 = config2.copy()


config4["agent_model_name"] = ["doubao-1-5-thinking-pro-250415", "claude-3-7-sonnet-20250219"]


import itertools
good_model_list = [
           # "deepseek-r1-250120",
           # "deepseek-v3-250324",
            "doubao-1-5-pro-256k-250115",
            "gemini-2.5-flash-preview-04-17",
            "gpt-4.1-2025-04-14",
            "gpt-4.1-mini-2025-04-14",
            "o4-mini",
            "claude-3-7-sonnet-20250219",
        ]