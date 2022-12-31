RUN TRAIN TIME
==============

## Vanilla Pandas + XGBoost

```
Loading data...
Preprocessing...
Splitting...
Training...
Evaluating...
              precision    recall  f1-score   support

           0       0.97      0.85      0.91    554869
           1       0.73      0.95      0.82    241491

    accuracy                           0.88    796360
   macro avg       0.85      0.90      0.86    796360
weighted avg       0.90      0.88      0.88    796360

             action    elapsed
0      load_dataset  16.587075
1   prepare_dataset   0.740689
2  train_test_split   1.604622
3          training  34.538261
4        evaluation   0.102266

real	0m56,237s
user	6m16,621s
sys	0m2,861s
```

## oneAPI Modin + XGBoost

```
Intel(R) Extension for Scikit-learn* enabled (https://github.com/intel/scikit-learn-intelex)
FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
Loading data...
UserWarning: When using a pre-initialized Ray cluster, please ensure that the runtime env sets environment variable __MODIN_AUTOIMPORT_PANDAS__ to 1
Preprocessing...
Splitting...
FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
Training...
Evaluating...
              precision    recall  f1-score   support

           0       0.97      0.85      0.91    554869
           1       0.73      0.95      0.82    241491

    accuracy                           0.88    796360
   macro avg       0.85      0.90      0.86    796360
weighted avg       0.90      0.88      0.88    796360

UserWarning: `from_dict` is not currently supported by PandasOnRay, defaulting to pandas implementation.
Please refer to https://modin.readthedocs.io/en/stable/supported_apis/defaulting_to_pandas.html for explanation.
             action    elapsed
0      load_dataset   5.732386
1   prepare_dataset   2.681339
2  train_test_split  10.239900
3          training  36.345085
4        evaluation   0.142491
5   evaluation_d4py   0.193799

real	1m5,141s
user	7m23,340s
sys	0m5,280s
```

## Pandas + XGBoost GPU

```
Loading data...
Preprocessing...
Splitting...
Training...
Evaluating...
              precision    recall  f1-score   support

           0       0.96      0.85      0.90    554869
           1       0.73      0.93      0.82    241491

    accuracy                           0.87    796360
   macro avg       0.85      0.89      0.86    796360
weighted avg       0.89      0.87      0.88    796360

             action    elapsed
0      load_dataset  16.777692
1   prepare_dataset   0.871934
2  train_test_split   1.806693
3          training   1.202075
4        evaluation   0.104030

real	0m23,629s
user	0m27,768s
sys	0m3,370s
```
