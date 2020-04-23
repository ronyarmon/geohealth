#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

def detect_indices (df,header):

    '''
    Use the interquartile range to identify outliers (Q1 − 1.5 IQR or above Q3 + 1.5 IQR)
    in the values of the dataframe column provided (header) and produce the list of
    indices for the rows containing these values in the source dataframe.
    '''

    header_values=list(df[header])
    desc_stats=df[header].describe()

    # capture quartile values data from the descriptive stats
    first_q,third_q = desc_stats.loc ['25%'],desc_stats.loc ['75%']
    IQR = float (third_q-first_q)
    lowest,highest = first_q-1.5*IQR, third_q+1.5*IQR
    outliers = [v for v in header_values if ((v<lowest) or (v>highest))]
    perc_outliers = round(100 * (len (outliers)/len (header_values)),2)
    outliers_df = df[df[header].isin(outliers)]
    outliers_df_indices = list(outliers_df.index)

    if perc_outliers > 0:
        print ('{p}% of {n} values for {h} are outliers which will be removed'.\
        format(p=perc_outliers,h=header, n=len (header_values)))

    return outliers_df_indices
