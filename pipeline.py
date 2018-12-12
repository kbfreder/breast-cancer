import pickle
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import roc_curve, auc, confusion_matrix

seed = 19
cut = np.linspace(0,1,100)

def pkl_this(filename, df):
    '''Saves df as filename. Must include .pkl extension'''
    with open(filename, 'wb') as picklefile:
        pickle.dump(df, picklefile)

def open_pkl(filename):
    '''Must include .pkl extension. Returns object that can be saved to a df.
    '''
    with open(filename,'rb') as picklefile:
        return pickle.load(picklefile)

def log_this(s):
    with open("log.txt", "a") as f:
        f.write("\n" + s + "\n")

def convert_to_num_nan(df, col, unk):
    '''df = DataFrame
    col (str) = column filename
    unk (int, str) = value for which to conver to 'None'
    '''
    df[col] = pd.to_numeric(df[col], downcast='integer')
    return df[col].apply(lambda x: None if x == unk else x)

def vcs(df, col):
    '''Returns value counts of col from df'''
    return df[col].value_counts()
