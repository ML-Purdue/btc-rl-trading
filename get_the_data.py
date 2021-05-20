"""
Script for getting the new data with the option of normalize the data.

Usage:
  get_the_data.py [--link=<link>] [--normalize=<normalize>] [--file-path=<filepath>] 

Options:
  --link=<link>                 link to the csv data [default:Gemini]
  --normalize=<normalize>       Choose the specific way to normalize the data, especially the 'Close' [default: MinMaxScaler]
                                options are 'minmax', 'zscore' or 'none'
  --file-path=<file-path>       The directory that will contain the data [default:~/scratch/btc-rl-trading/data]
"""

import os
import pandas as pd
from scipy.stats import zscore
from docopt import docopt
import ssl

def get_data(link, normalize, path):
    if link is None:
        link='https://www.cryptodatadownload.com/cdd/gemini_BTCUSD_1hr.csv'
    if path is None:
        path='~/scratch/btc-rl-trading/data'
    if normalize is None:
        normalize='minmax'
    df = pd.read_csv(link, skiprows=1)
    if normalize != 'none':
        df = normalize_method(df, normalize)
    name = link[link.rfind('/') + 1 : link.find('_')]
    split_train_dev_set(df, name, path)
    

def normalize_method(df, normalize):
    if (normalize == 'minmax'):
        df['Close'] = (df['Close'] - df['Close'].min()) / (df['Close'].max() - df['Close'].min())
    else:
        df['Close'] = Zscore(df['Close'])
    return df
def split_train_dev_set(df, name, path):
    train_size = int(0.99 * len(df))
    test_size = int(0.995 * len(df))
    df = df[::-1]
    df_train = df.iloc[:train_size]
    df_val = df.iloc[train_size: test_size]
    df_test = df.iloc[test_size:]
    df_train.to_csv(f'{path}/{name}_train_set.csv')
    df_val.to_csv(f'{path}/{name}_val_set.csv')
    df_test.to_csv(f'{path}/{name}_test_set.csv')



if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    args = docopt(__doc__)

    link = args['--link']
    normalize = args['--normalize']
    path = args['--file-path']

    try:
        get_data(link=link, normalize=normalize, path=path)
    except KeyboardInterrupt:
        print("Aborted")