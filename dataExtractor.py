"""
Functions for getting data to be used in specific use cases.

Usage:
    Import this file into any python script and use the functions
    as necessary!
"""

import pandas as pd
import numpy as np
import random

def reset_my_index(df):
    """
    https://stackoverflow.com/questions/20444087/right-way-to-reverse-pandas-dataframe
    """
    res = df[::-1].reset_index(drop=True)
    return(res)

def getBTCIntervalDays(startTime, endTime):
    """
    Retrieves BITCOIN historical day-wise data from the specified
    interval.
    :return: Pandas DF containing historical data. Returns
    None if interval is invalid or if another error is thrown.
    :parameter startTime: The date in which data retrieval will
    begin. 0 corresponds to 2015-10-08 and 1646 corresponds
    to 2020-04-10
    :parameter endTime: The date in which data retrieval will
    end. 0 corresponds to 2015-10-08 and 1646 corresponds
    to 2020-04-10
    """
    df = pd.read_csv("data/BTCUSD_day_alldates.csv")
    # Data is stored in reverse chronological order, we reverse
    # it using reset_my_index
    df = reset_my_index(df)
    try:
        return df[startTime:endTime]
    finally:
        return None

def getRandomBTCIntervalDays(minDelta = 100):
    """
    Retrieves a random interval from the BTCUSD_day_alldates
    dataframe
    :param minDelta: Indicates the minimum delta between
    start and end date. MAX IS 1646.
    :return: Pandas DF containing historical data from
    the afformentioned random interval. Returns None
    if minLength is greater than the max value
    """
    if minDelta > 1646:
        return None
    df = pd.read_csv("data/BTCUSD_day_alldates.csv")
    # Data is stored in reverse chronological order, we reverse
    # it using reset_my_index
    df = reset_my_index(df)

    lowerBound = random.randint(0, 1646 - minDelta)
    upperBound = random.randint(lowerBound, random.randint(lowerBound + minDelta, 1646))

    return df[int(lowerBound):int(upperBound)]
