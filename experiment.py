import argparse

parser = argparse.ArgumentParser(description="Experiment configuration")
parser.add_argument("--prompt_type", type=str, default="prompt_type", help="one of [framed, neutral, hinted]")

args = parser.parse_args()

if (args.prompt_type == "framed"):
    from config_args import config1, config2, config3, config4, good_model_list
elif (args.prompt_type == "neutral"):
    from config_args_no_horse import config1, config2, config3, config4, good_model_list
elif (args.prompt_type == "hinted"):
    from config_args_hint import config1, config2, config3, config4, good_model_list

import horse_environment
import my_agent
import random
from pydantic_parser import get_last_number
import numpy as np
from logging import log
import pandas as pd

# primitive experment

def extract_last_number(response):
    lines = response.strip().split('\n')
    last_line = lines[-1].strip()
    if last_line.isdigit():
        return int(last_line)
    return None

def get_choices(responses: list[str]):
    return [get_last_number(stri) for stri in responses]
        
def get_strictly_win_prompts(won: bool, total_winner_count: int):
    if (won == False):
        return "You have lost the game!"
    elif (total_winner_count == 1):
        return "You are the sole winner!"
    else:
        return f"You win together with {total_winner_count} players!"

def get_win_prompts(total_rewards: dict[int, float]):
    max_reward = np.max(total_rewards)
    winnities = (max_reward == total_rewards)
    num_players = len(total_rewards)
    if (bool(winnities.all())):
        return ["You reached a draw with your opponents!"] * num_players
    total_winner_count = winnities.sum()
    return [get_strictly_win_prompts(won, total_winner_count) for won in winnities]

def get_rand_values(horses_still_available: list[set]):
    return [int(np.random.choice(list(horses_set)))
             for horses_set in horses_still_available]   

def update_available_horses(horses_still_available: list[set], choices):
    for idx, choice in enumerate(choices):
        horses_still_available[idx] -= {choice}

"""
def get_valid_choices(
        agents: list[my_agent.MyAgent], 
        horses_still_avaliable: list[set])
"""

list_english = ["zero", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
def get_english(number: int):
    return list_english[number]

def experiment(config: dict[str, bool]):
    random.seed(config["random_seed"])
    np.random.seed(config["random_seed"])

    print(config["agent_model_name"], config["timeout_seconds"])
    try:
        agents = [
            my_agent.MyAgent(
                model_name=model_name, 
                timeout_seconds=config["timeout_seconds"],
                temperature=config["temperature"],
                top_p=config["top_p"],
                random_seed=config["random_seed"]
            ) for model_name in config["agent_model_name"]]
        env = horse_environment.HorseRaceGame(players=agents, horses_per_player=config["horses_per_player"])

        system_initial_prompt = config["system_background"].format(
            agent_name="{agent_name}", 
            optional_cot_prompt=config["optional_cot_prompt"],
            player_count=len(agents)    
        )
        current_state_prompt = config["current_state_prompt"]
        resp_round = ["Error: Empty"] * len(agents)

        end_state_prompt = config["end_state_prompt"]



        def get_infostr(observation, idx):
            all_choice = observation["choices"]
            return f"Opponents\' last moves: {all_choice[:idx] + all_choice[(idx + 1):]}"
        def reset_horses_still_avaliable():
            return [set(range(config["horses_per_player"])) for _ in range(len(agents))]
        
        history = []


        horses_still_available = reset_horses_still_avaliable()
        print(horses_still_available)
        rand_values = get_rand_values(horses_still_available)
        for idx, agent in enumerate(agents):
            strin = system_initial_prompt.format(agent_name=f"agent{idx}") \
                            + current_state_prompt.format(
                            horses_still_avaliable=horses_still_available[idx],
                            infos="",
                            random_value=rand_values[idx],
                            round_number=get_english(1)
                        )
            strin2 = strin
            for i in range(3):
                resp_round[idx] = agent.continue_conversation({"system": strin2})
                if (get_last_number(resp_round[idx]) in horses_still_available[idx]):
                    break
                else:
                    strin2 = "Error: Invalid Choice\n" + strin
                    print(" -- Error: Invalid Choice -- ")
            
        choices = get_choices(resp_round)
        history.append({"rand_values": rand_values.copy(), "choices": choices.copy()})
        print({"rand_values": rand_values.copy(), "choices": choices.copy()})


        for trial_count in range(config["total_trials"]):
            
            print(f"trial_count: {trial_count}")

            
            observation = None

            for round_number in range(2, (config["horses_per_player"] + 10)):
                
                observation, reward, terminated, truncated, info = env.step(choices)
                if terminated:
                    break
                
                update_available_horses(horses_still_available, choices)
                rand_values = get_rand_values(horses_still_available)
                for idx, agent in enumerate(agents):
                    infostr=get_infostr(observation=observation, idx=idx)
                    strin = current_state_prompt.format(
                        horses_still_avaliable=horses_still_available[idx],
                        infos=infostr,
                        random_value=rand_values[idx],
                        round_number=get_english(round_number)
                    )
                    strin2 = strin
                    for i in range(3):
                        resp_round[idx] = agent.continue_conversation({"system": strin2})
                        if (get_last_number(resp_round[idx]) in horses_still_available[idx]):
                            break
                        else:
                            strin2 = "Error: Invalid Choice\n" + strin
                            print(" -- Error: Invalid Choice -- ")
                choices = get_choices(resp_round)
                history.append({"rand_values": rand_values.copy(), "choices": choices.copy()})
                print({"rand_values": rand_values.copy(), "choices": choices.copy()})

            
            win_prompts = get_win_prompts(env.get_total_rewards())
            env = horse_environment.HorseRaceGame(players=agents, horses_per_player=config["horses_per_player"])
            horses_still_available = reset_horses_still_avaliable()
            rand_values = get_rand_values(horses_still_available)
            for idx, agent in enumerate(agents):
                infostr=get_infostr(observation=observation, idx=idx)
                strin = end_state_prompt.format(
                    infos=infostr,
                    win_str=win_prompts[idx]
                ) + current_state_prompt.format(
                    horses_still_avaliable=horses_still_available[idx],
                    infos="",
                    random_value=rand_values[idx],
                    round_number=get_english(1)
                )
                strin2 = strin
                for i in range(3):
                    resp_round[idx] = agent.continue_conversation({"system": strin2})
                    if (get_last_number(resp_round[idx]) in horses_still_available[idx]):
                        break
                    else:
                        strin2 = "Error: Invalid Choice\n" + strin
                        print(" -- Error: Invalid Choice -- ")
            choices = get_choices(resp_round)
            
            history.append({"rand_values": rand_values.copy(), "choices": choices.copy()})
            print({"rand_values": rand_values.copy(), "choices": choices.copy()})
            

        print(history)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        return agents, history

from itertools import combinations
import os
if __name__ == "__main__":
    base_config = config3
    generator1 = list(combinations(good_model_list, 2))  + [[namer] * 2 for namer in good_model_list]
    for combinator in generator1:
        base_config["agent_model_name"] = combinator
        agents, histories = experiment(config=base_config)
        histories = pd.DataFrame(histories)
        namer = " ".join(base_config["agent_model_name"]) + ".csv"
        histories.to_csv(os.path.join(f"logs_{args.prompt_type}", namer))
        [agent.close() for agent in agents]
