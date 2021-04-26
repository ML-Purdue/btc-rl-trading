from trading_bot.agent import Agent
from trading_bot.methods import evaluate_model
from trading_bot.utils import (get_stock_data, format_currency, format_position, show_eval_result, switch_k_backend_device)
import threading #https://www.tutorialspoint.com/python/python_multithreading.htm

class TradeBot(threading.Thread):

    def __init__(self, threadID, name, api_key, api_secret, gui_refresh_fcn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        # TODO

    def panick_sell():
        # TODO

    def run():
        # TODO



