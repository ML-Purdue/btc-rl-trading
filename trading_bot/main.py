import numpy as np

import altair as alt
import seaborn as sns

from agent import Agent

model_name = 'model_dqn_GOOG_50'
test_stock = '../data/GOOG_2019.csv'
window_size = 10
debug = True

agent = Agent(window_size, pretrained=True, model_name=model_name)