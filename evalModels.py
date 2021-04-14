"""
Script for evaluating Stock Trading Bot.

Usage:
  evalModels.py <eval-stock> [--window-size=<window-size>] [--model1=<model-name>] [--model2=<model-name>] [--debug]

Options:
  --window-size=<window-size>   Size of the n-day window stock data representation used as the feature vector. [default: 10]
  --model1=<model-name>     Name of the pretrained model to use (will eval all models in `models/` if unspecified).
  --model2=<model-name>
  --debug                       Specifies whether to use verbose logs during eval operation.
"""

import os
import coloredlogs

from docopt import docopt

from trading_bot.agent import Agent
from trading_bot.methods import evaluate_models
from trading_bot.utils import (
    get_stock_data,
    format_currency,
    format_position,
    show_multi_eval_result,
    switch_k_backend_device
)


def main(eval_stock, window_size, model1, model2, debug):
    """ Evaluates the stock trading bot.
    Please see https://arxiv.org/abs/1312.5602 for more details.

    Args: [python eval.py --help]
    """    
    data = get_stock_data(eval_stock)
    initial_offset = data[1] - data[0]

    # Single Model Evaluation
    if model1 is not None and model2 is not None:
        agent1 = Agent(window_size, pretrained=True, model_name=model1)
        agent2 = Agent(window_size, pretrained=True, model_name=model2)
        profit, _ = evaluate_models(agent1, agent2, data, window_size, debug)
        show_multi_eval_result(model1, model2, profit, initial_offset)


if __name__ == "__main__":
    args = docopt(__doc__)

    eval_stock = args["<eval-stock>"]
    window_size = int(args["--window-size"])
    model1 = args["--model1"]
    model2 = args["--model2"]
    debug = args["--debug"]

    coloredlogs.install(level="DEBUG")
    switch_k_backend_device()

    try:
        main(eval_stock, window_size, model1, model2, debug)
    except KeyboardInterrupt:
        print("Aborted")
