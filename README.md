# Do LLMs Know When to Flip a Coin? Strategic Randomization through Reasoning and Experience
![Reproducibility](https://img.shields.io/badge/Status-Reproducible-brightgreen)

## Environment Setup
```bash
pip install requirements.txt
```

##### Reproducing GTBench
Put your base url in `base-url.txt` and put your api key in `API-key.txt`.

The following is a script for `doubao-1-5-pro-256k-250115 w/ Prompt Agent` vs. `doubao-1-5-pro-256k-250115 w/ CoT Agent`, over `Tic-Tac-Toe`
```shell
bash test_script.sh
```
The results are in `experiments/test/doubao-1-5-pro-256k-250115`, showing CoT's superiority.

# Running Essential Scripts
```
python experiment.py --prompt_type=framed
python experiment.py --prompt_type=neutral
python experiment.py --prompt_type=hinted
```
# Plotting results
modify `base_log_dir` in `plotter.ipynb` and run the notebook to plot and save the results.
