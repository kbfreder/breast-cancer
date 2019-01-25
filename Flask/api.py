# import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.exceptions import DataConversionWarning
import warnings

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=DeprecationWarning)

# print ("api running")

pipeline = joblib.load('./model/model_grad_boost_02.joblib')

race_dict = {'White':'1', 'Black':'2', 'Other':'3'}

def prediction(inputs):
    if inputs['SEQ_NUM'] == '1':
        seq_num = 0
    else:
        seq_num = int(inputs['SEQ_NUM'])

    X = np.array([int(inputs['MAR_STAT_MOD']),
                race_dict[inputs['RACE_MOD']],
                int(inputs['AGE_DX']),
                int(inputs['GRADE']),
                int(inputs['TUMSIZ']),
                int(inputs['SURG']),
                seq_num,
                int(inputs['POS_NODES']),
                int(inputs['INVAS'])]).reshape(1,-1)
    # print(X)
    prob_survived = int(pipeline.predict_proba(X)[0,1] * 100)
    prob_surv_ftd = f"{prob_survived}%"

    if prob_survived >= 0.85:
        prob_surv_words = 'Excellent'
    elif prob_survived >= 0.5 and prob_survived < 0.85:
        prob_surv_words = 'Good'
    elif prob_survived >= 0.3 and prob_survived < 0.5:
        prob_surv_words = 'Fair'
    else:
        prob_surv_words = 'Poor'

    result = {
            'prediction': int(prob_survived > 0.66),
            'prob_survived': prob_surv_ftd
    }
    return result


example = {
        'MAR_STAT_MOD':1,
        'RACE_MOD':'Other',
        'AGE_DX':50,
        'GRADE':1,
        'TUMSIZ':1,
        'SURG':1,
       'SEQ_NUM':0,
       'POS_NODES':0,
       'INVAS':0
}


if __name__ == '__main__':
    print(prediction(example))
