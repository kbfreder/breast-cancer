 ### Jupyter notebooks

- **01a_DataImport**: importing data from .txt files
  - leverages 'SAS' file to "decode" the data
- **01b_DataPrep**: prepares data for modeling
  - Uses external functions that live in 'cleaning.py' to clean data
  - Creates 2 data frames:
    - 220,000 rows, without sub-type feature
    - 19,600 rows, with sub-type feature
  - Establishes preprocessing pipeline
- **01c_DataExploration**: EDA
- **02a_ModelScreen**: Screening models for top candidates. 
- **02b_AddressingImbalance**: Assesssing over- and under-sampling methods
- **03a_FinalEval**: Figures for presentation; Learning curve



### "Appendix":

- **A01a_DataClean**: Exploration of features & Development of code for 'cleaning.py'

- **A01b_DataClean-Stage**: as above, for Stage feature




### Python files:

- **pipeline.py**: utility code
- **cleaning.py**: code to clean SEER data
- **assess_clf_models**: 




Data files that are generated:

- **breast_df_for_model.pkl**: cleaned & converted dataframe. Shape: 222127, 12
- **breast_df_with_sub_for_model.pkl**: as above, with sub-type. Shape: 19667, 13
- **preprocess_wo_sub.pkl**: prepressor (Scaling, One-Hot-Encoding) for dataset without sub-type
- **preprocess_with_sub.pkl**: preprocesser for dataset with sub-type
