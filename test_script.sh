
seed=0
output_root="./experiments$1"
exp_name='test'
num_matches=50 # number of matches
num_workers=20 # run 20 matches in parallel
threshold_matches=100 # maximum number of matches, stop criteria for low completion rate, e.g., LLM agents always generate illegal actions.
# suports all the games listed in ./gamingbench/configs/game_configs/*.yaml
game_name='tictactoe'
# supports all the llms defined in ./gamingbench/configs/model_configs/*.yaml
model_config_root='gamingbench/configs/model_configs'
llm_name="doubao-1-5-pro-256k-250115"
opponent_llm_name="doubao-1-5-pro-256k-250115"
# supports all the reasoning methods defined in ./gamingbench/agent_configs/*.yaml
agent_config_root='gamingbench/configs/agent_configs'
agent_name='prompt_agent'
opponent_agent_name='cot_agent'
export OA_BASE_URL="$(cat base-url.txt)"
declare -a api_keys=("$(cat API-key.txt)" "<YOUR_DEEPINFRA_KEY>")

python3 -m gamingbench.main \
    --num-matches ${num_matches} \
    --exp-root ${output_root}/${exp_name}/${llm_name} \
    --seed ${seed} \
    --game-name ${game_name} \
    --agent-configs ${agent_config_root}/${agent_name}.yaml ${agent_config_root}/${opponent_agent_name}.yaml \
    --model-configs ${model_config_root}/${llm_name}.yaml ${model_config_root}/${opponent_llm_name}.yaml \
    --api-keys ${api_keys[@]} \
    --exchange-first-player \
    --num-workers ${num_workers} \
    --threshold-matches ${threshold_matches}
