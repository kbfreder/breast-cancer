import pandas as pd
import datetime as dt

cols_to_include = ['MAR_STAT_MOD',
                   'RACE_MOD',
                   'AGE_DX',
                   'GRADE',
                   'TUMSIZ',
                   'SURG',
                   'SEQ_NUM',
                   'PRIMSITE',
                   'POS_NODES',
                   'HST_STGA',
                   'INVAS']

def convert_to_num_nan(df, col, unk):
    '''Converts col(str) in df(DataFrame) to numeric (integer)
    Then converts values equal to 'unk'(str or int) in col to 'None' '''
    df[col] = pd.to_numeric(df[col], errors='coerce')
    return df[col].apply(lambda x: None if x == unk else x)


def drop_unk(df, col, unk):
    return df[col].apply(lambda x: None if x == unk else x)


def get_one_or_other(row, col1, col2, null_str):
    if row[col1] == null_str:
        return row[col2]
    else:
        return row[col1]

def surg_class(x):
    if x == '0':
        return 1
    elif (x == '8') | (x == '9'):
        return None
    else:
        return 0

def marital_class(x):
    if x == '9':
        return None
    elif (x == '2') | (x == '6'):
        return int(1)
    else:
        return int(0)

def convert_race(x):
    if (x == '01') | (x == '02'):
        return x
    elif x == '99':
        return None
    else:
        return '03'

def convert_stage_dajcc(x):
    if (x == '00'):
        return 0
    elif x == '10':
        return 1
    elif (x == '32') | (x == '33'):
        return 2
    elif (x == '51') | (x == '52') | (x == '53'):
        return 3
    elif x == '70':
        return 4
    else:
        return N

def convert_stage(x):
    if x == '4':
        return 3
    elif x == '9':
        return None
    else:
        return int(x)

def month_plus_year(row):
    return dt.datetime(year = row['YEAR_DX'], month = row['MDXRECMP'], day=1)


def clean_and_dropna(df):

    df3 = clean_only(df)
    df4 = df3[cols_to_include + ['TARGET']]
    df4 = df4.dropna()

    df6 = get_subtype(df3)
    # df5 = df3.drop(df3[(df3['BRST_SUB'] == '9') | (df3['BRST_SUB'] == '5')].index)
    # df6 = df5[cols_to_include + ['BRST_SUB','TARGET']]
    # df6 = df6.dropna()

    return df4, df6


def clean_only_mod(df2):
    df2['SRV_TIME_MON'] = convert_to_num_nan(df2, 'SRV_TIME_MON', 9999)
    df2['YEAR_DX'] = pd.to_numeric(df2['YEAR_DX'])
    # drop
    # df2 = df.drop(df[df['YEAR_DX'] > 2010].index)
     # create target class
    df2['TARGET'] = df2['SRV_TIME_MON'].apply(lambda x: 1 if x >= 60 else 0)
    df2['SRV_TIME_MON_FLAG'] = convert_to_num_nan(df2, 'SRV_TIME_MON_FLAG', 9)
    df2 = df2.drop(df2[(df2['SRV_TIME_MON_FLAG'] == 2) | (df2['SRV_TIME_MON_FLAG'] == 3)].index)
    # remove duplicate patient records
    df3 = df2.drop_duplicates(subset='PUBCSNUM', keep='first')
    df3['SEQ_NUM'] = convert_to_num_nan(df3, 'SEQ_NUM', 99)
    df3['AGE_DX'] = convert_to_num_nan(df3, 'AGE_DX', 999)
    df3['GRADE'] = convert_to_num_nan(df3, 'GRADE', 9)

    # Tumor Size
    ws = df3['EOD10_SZ'].value_counts().index[0]
    df3.loc[:,'TUMSIZ'] = df3.apply(lambda row: get_one_or_other(row, 'EOD10_SZ','CSTUMSIZ', ws), axis=1)
    df3.loc[:,'TUMSIZ'] = convert_to_num_nan(df3, 'TUMSIZ', 999)
    df3.drop(columns = ['EOD10_SZ', 'CSTUMSIZ'], inplace=True)
    df3['TUMSIZ'] = drop_unk(df3, 'TUMSIZ', 888)
    df3['TUMSIZ'] = drop_unk(df3, 'TUMSIZ', 990)
    df3['TUMSIZ'] = drop_unk(df3, 'TUMSIZ', 996)
    df3['TUMSIZ'] = drop_unk(df3, 'TUMSIZ', 997)
    df3['TUMSIZ'] = drop_unk(df3, 'TUMSIZ', 998)
    df3['TUMSIZ'] = df3['TUMSIZ'].apply(lambda x: x-990 if x >= 991 else x)

    df3['EOD10_PN'] = convert_to_num_nan(df3, 'EOD10_PN', 99)
    df3 = df3.drop(df3[df3['EOD10_PN'] > 90].index)
    df3.rename(columns={'EOD10_PN':'POS_NODES'}, inplace=True)

    df3['SURG'] = df3['NO_SURG'].apply(lambda x: surg_class(x))

    df3['MAR_STAT_MOD'] = df3['MAR_STAT'].apply(lambda x: marital_class(x))

    df3['RACE_MOD'] = df3['RACE1V'].apply(lambda x: convert_race(x))

    df3['INVAS'] = df3['BEHO3V'].apply(lambda x: 0 if x == '2' else 1)
    df3['HST_STGA'] = df3['HST_STGA'].apply(lambda x: convert_stage(x))

    # Create DX Date & Censor Time columns:
    df3['MDXRECMP'] = pd.to_numeric(df3['MDXRECMP'])
    df3['DATE_DX'] = df3.apply(lambda row: month_plus_year(row), axis=1)
    df3['CENSOR_TIME_MON'] = (dt.datetime(year=2015, month=12, day=31) - df3['DATE_DX']) / dt.timedelta(days=30)

    # Create 'DEATH' (event/ outcome) column using 'CODPUB' (recode for cause of death)
    df3 = df3.drop(df3[(df3['CODPUB'] == '41000') | (df3['CODPUB'] == '99999')].index)
    df3['DEATH'] = df3['CODPUB'].apply(lambda x: 0 if x == '00000' else 1)

    return df3

def get_subtype(df3):
    df5 = df3.drop(df3[(df3['BRST_SUB'] == '9') | (df3['BRST_SUB'] == '5')].index)
    df6 = df5[cols_to_include + ['BRST_SUB','TARGET']]
    df6 = df6.dropna()

    return df6
