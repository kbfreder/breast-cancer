import pickle

def pkl_this(filename, df):
    '''Saves df as filename. Must include .pkl extension'''
    with open(filename, 'wb') as picklefile:
        pickle.dump(df, picklefile)

def open_pkl(filename):
    '''Must include .pkl extension. Returns object that can be saved to a df.
    '''
    with open(filename,'rb') as picklefile:
        return pickle.load(picklefile)
