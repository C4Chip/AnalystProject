import os

from datetime import datetime
from datetime import timedelta
from TZmyApp import models
#import datetime
import matplotlib.pyplot as plt
#%matplotlib inline
import pandas as pd
import numpy as np

def LoadDataFrame(filename):
    df = pd.DataFrame()

    if os.path.isfile(filename):
        df = pd.read_csv(filepath_or_buffer=filename)
        df['<date>'] = df['<date>'].astype(str)

    return df


def ReIndex(df):
    tuples = list(zip(df['<ticker>'], df['<date>']))
    hier_index = pd.MultiIndex.from_tuples(tuples)

    # Reset the Index
    df.reset_index()
    df.index = hier_index

    # Drop unwanted columns
    df.pop('<ticker>')
    df.pop('<date>')

    df.index.names = ['Ticker', 'Date']

    return df



def LoadAllDataFrames(start, end):
    dfs = pd.DataFrame()

    dt_range = end - start

    for i in range(0, dt_range.days + 1):

        dt = start + timedelta(i)

        filename = "./FOREX_2011/FOREX_" + dt.strftime('%Y%m%d') + ".txt"

        df = LoadDataFrame(filename)

        if not df.empty:
            dfs = pd.concat([dfs, df])

    dfs = ReIndex(dfs)

    return dfs


def Strat1(df, start, end, short, long, upperth, lowerth):
    df_Res = pd.DataFrame()

    short_term = df['<close>'].ewm(span=short).mean()
    long_term = df['<close>'].ewm(span=long).mean()
    df_Res['short_term'] = np.round(short_term, 2)
    df_Res['long_term'] = np.round(long_term, 2)

    # Store the difference between the short term and the long term
    df_Res['Diff'] = df_Res['short_term'] - df_Res['long_term']

    # set the regime
    df_Res['Regime'] = np.where(df_Res['Diff'] / df_Res['long_term'] > upperth, 1, 0)
    df_Res['Regime'] = np.where(df_Res['Diff'] / df_Res['long_term'] < -lowerth, -1, df_Res['Regime'])

    df_Res['Market'] = np.log(df['<close>'] / df['<close>'].shift(1))
    df_Res['Strategy'] = df_Res['Regime'].shift(1) * df_Res['Market']

    return df_Res


def BackTest(symbol, start, end):
    all_data = LoadAllDataFrames(start, end)

    df = all_data.xs(symbol).copy()
    df.index = pd.to_datetime(df.index)

    short_term = 10
    long_term = 60
    upper_threshold = 0.001
    lower_thresdhold = 0.01
    df_res = Strat1(df, start, end, short_term, long_term, upper_threshold, lower_thresdhold)

    return df_res

