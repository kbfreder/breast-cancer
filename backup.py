def clean_only(df):
    df['SRV_TIME_MON'] = convert_to_num_nan(df, 'SRV_TIME_MON', 9999)
    df['YEAR_DX'] = pd.to_numeric(df['YEAR_DX'])
    # drop
    df2 = df.drop(df[df['YEAR_DX'] > 2010].index)
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

    return df3
