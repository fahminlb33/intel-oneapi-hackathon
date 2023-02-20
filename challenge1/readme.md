# Challenge 1 - Machine Learning Challenge Track: Predict the quality of freshwater

Welcome to my machine learning submission project! In this repo I used [Intel® Distribution of Modin](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-of-modin.html) to analyze and preprocess the dataset, [Intel® Optimization for XGBoost](https://www.intel.com/content/www/us/en/developer/tools/oneapi/optimization-for-xgboost.html) to create the classification model, and [daal4py from Intel® oneAPI Data Analytics Library (oneDAL)](https://intelpython.github.io/daal4py/) to export and perform inference on the XGBoost model.

## Environment Setup

Before running the training process, you will need to create a new Python environment. I recommend using Mamba to create the environment.

```bash
$ mamba create -n oneapi -c intel daal4py xgboost modin-all scikit-learn scikit-learn-intelex mlflow optuna

$ mamba activate oneapi
```

After you have the conda environment, next you have to download the dataset CSV and place it somewhere easily accessible.

## Exploratory Data Analysis

> The EDA process is done in Jupyter Notebook, you will need to install `notebook` and `ipykernel` to your environment!

In the EDA process our goal to find out what preprocessing tasks we have to do before the modelling process and also summarize some of the features on the dataset to create a simple dashboard.

For the data summarization, I mostly used the `resample` method to do window aggregation and then saving it to JSON file so it can be loaded later on from the web app.

### Data Preprocessing

Based on the gathered information from the EDA process, the data processing itself is not complicated, there are just two process involved,

1. Label encoding the categorical features (color, source, month)
2. Fill null values

You can find out more about the data preprocessing in the `preprocess.py` about how to map the categorical features to numbers and the strategy to fill the missing values.

## Running Training Process

Before running the training process, make sure you have the CSV dataset file. Activate your conda environment and `cd` into `challenge1` directory, then run the `train.py` script.

```bash
$ git clone --recurse-submodules https://github.com/fahminlb33/intel-oneapi-hackathon

$ cd intel-oneapi-hackathon/challenge1

$ python train.py --model-format daal4py --dataset ./dataset/freshwater.csv --output ./models
```

After a while you should get your `.pkl` model in the `models` directory.

### Hyperparamter Optimization

Congratulations! You have successfully created your first classification model. But keep in mind this model might not be the best one yet in terms of classification accuracy.

In this section you can run another script, `optimize.py` to optimize the hyperparameters of the base model. Using the same data, this script will try various parameters to the XGBoost model in hope that it will increase the classification accuracy and F1-score. You'll need `optuna` to run the script and also `mlflow` to monitor the model performance for every iteration.

```bash
$ mlflow ui # start the MLflow

$ python optimize.py # open a new terminal and run this
```

By default this script will run for 50 iterations and it will save the metrics to MLflow.

Now you have the best parameters stored in MLflow, you can copy it into the `parameters.py` file and then run the training again using the `train.py`, but now with one more switch, `--best-params`. This will instruct the script to use the best parameters defined in the `parameters.py`.

**Performance metrics**

| Task            | Precision | Recall | F1-score | Accurracy |
|-----------------|-----------|--------|----------|-----------|
| Before optimize | 0.87      | 0.86   | 0.86     | 0.86      |
| After optimize  | 0.89      | 0.87   | 0.87     | 0.87      |

Note: precision, recall, f1-score are weighted average (see [scikit-learn's classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html))

We now have a slightly better overall classification performance. If you want to try optimize the model further, you can try to increase the optimize iteration or do some more preprocessing before running the training process.

## Web App

See [Web App](./web-app.md).
