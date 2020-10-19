#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


# Define a function to explore the missing rate
def explore_missing(data, dropna=True):
    data_na = (data.isnull().sum() / len(data)) * 100
    if dropna == True:
        data_na = data_na.drop(data_na[data_na==0].index).sort_values(ascending=False)
    else:
        data_na = data_na.sort_values(ascending=False)
    missing_info = pd.Dataframe({'Missing Ratio': data_na})
    return missing_info

# fillna with frequenst value if unique value is small
def fill_na_cat(data):
    df_freq = data.describe()
    for col in list(data.columns):
        if len(data[col].unique()) <= 50:
            data[col] = data[col].fillna('None')
    return data


def fillna_num(data):
    for col in list(data.columns):
        if len(data[col].unique()) >= 50:
            data[col] = data[col].fillna(data[col].median())
        else:
            data[col] = data[col].fillna(0) # need more exploration
    return data


def plot_heatmap(df):
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(16, 10))
    # Generate color map
    colormap = sns.diverging_palette(220, 10, as_cmap=True)
    # Generate Heat map
    sns.heatmap(corr, cmap=colormap, annot=True, fmt=".3f")
    # Show plot
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.show()


def clean_corr(df):
    raw_cols = list(df.index)
    to_drop = []
    for col in raw_cols:
        if col not in to_drop:
            correlated_cols = np.where((df.loc[col, :] >=0.60) & (df.loc[col, :] < 1.0))
            to_droppend_col = df.columns[correlated_cols]
            to_drop.extend(to_droppend_col)
        kept_cols = [ c for c in raw_cols if c not in to_drop]
        print("Kept variables length: {}".format(len(kept_cols)))

    return [ c for c in raw_cols if c not in to_drop]


def maximum_ks(str_score, str_resp, df_scored):
    '''

    :param str_score:  a string that specifies score name
    :param str_resp:  a string that specifies response
    :param df_scored:  a dataframe contains group & response columns
    :return:
    '''

    if df_scored is None:
        print("Error, no scored file for maximum_ks()!!!")
    else:
        max_ks_sort = df_scored.sort_values(str_score, ascending=False)
        max_ks_sort['response'] = df_scored[str_resp]
        max_ks_sort.index = range(1, len(max_ks_sort) +1)
        max_ks_sort['cum_good'] = max_ks_sort.response.cumsum()
        max_ks_sort['cum_bad'] = max_ks_sort.index - max_ks_sort.cum_good
        max_ks_sort['cum_good_rate'] = max_ks_sort.cum_good / max_ks_sort.response.sum()
        max_ks_sort['cum_bad_rate'] = max_ks_sort.cum_bad / (max_ks_sort.response.size - max_ks_sort.response.sum())
        max_ks_sort['cum_rand_rate'] = max_ks_sort.index / max_ks_sort.response.size
        max_ks_sort['ks'] = max_ks_sort.cum_good_rate - max_ks_sort.cum_bad_rate

        max_ks_score = max_ks_sort[(max_ks_sort.ks == max_ks_sort.ks.max())]
        max_ks_score = max_ks_score[['cum_good_rate', 'cum_rand_rate', 'ks']]
        max_ks_score.rename(columns={'cum_rand_rate': 'max_ks_pop', 'ks': 'max_ks'}, inplace=True)
        max_ks_score = max_ks_score.reset_index(drop=True)

    return max_ks_score, max_ks_sort


def lorenz_curve(df_kstable, df_maxks):
    lorenz = pd.DataFrame({'cum_good': df_kstable.cum_good_rate.values[list(range(1, len(df_kstable)+1, 100))],
                           'cum_rand': df_kstable.cum_rand_rate.values[list(range(1, len(df_kstable)+1, 100))],
                           'cum_bad': df_kstable.cum_bad_rate.values[list(range(1, len(df_kstable)+1, 100))]})

    t0 = lorenz.cum_rand.values
    t1 = lorenz.cum_good.values
    t2 = lorenz.cum_rand.values
    t3 = lorenz.cum_bad.values

    fig = plt.figure()
    ax = fig.add_subplot(111)

    max_ks_val = df_maxks['max_ks'].values[0]
    max_ks_pop = df_maxks['max_ks_pop'].values[0]
    max_ks_cgr = df_maxks['cum_good_rate'].values[0]

    line1, = ax.plot(t0, t1, ls='solid', color='blue', lw=1.5)
    line2, = ax.plot(t0, t2, ls='dashed', color='green', lw=1.5)
    line3, = ax.plot(np.array([max_ks_pop, max_ks_pop]), np.array([0, max_ks_cgr]), ls='dashdot', color='grey', lw=1.5)
    line4, = ax.plot(np.array([0, max_ks_pop]), np.array([max_ks_cgr, max_ks_cgr]), ls='dashdot', color='grey', lw=1.5)
    mark1, = ax.plot(max_ks_pop, max_ks_cgr, marker='>', markersize=10, color='blue')
    txt = "Max KS: {:.0%}".format(max_ks_val) + " at " +  '{:.0%}'.format(max_ks_pop) + " of Population"
    plt.text(max_ks_pop + 0.03, max_ks_cgr - 0.01, txt, ha='left', rotation=0, wrap=True)

    xtext = ax.set_xlabel('% Cumulative Population')
    ytext = ax.set_ylabel('% Cumulative Good')

    ax.set_xlim(0., 1.)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda t0, _: '{:.0%}'.format(t0)))

    ax.set_ylim(0., 1.)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda t1, _: '{:.0%}'.format(t1)))

    plt.legend((line1, line2), ('Model', 'Random'), loc='lower right', bbox_to_anchor=[0.95, 0.1], shadow=True)
    plt.subtitle('Lorenz Curve', fontsize=14)
    plt.show()


