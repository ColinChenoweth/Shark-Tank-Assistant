import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score

def get_data():
    # Read the original dataset
    df = pd.read_csv("Data/SharkTankUSdataset.csv")
    
    new_metrics_df = pd.read_csv("Data/new_metrics/pitch_data.csv")
    df = pd.merge(df, new_metrics_df, on='ID')

    # Define the feature columns including the new ones
    feature_columns = ['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State',
                       'Pitchers Average Age', 'US Viewership', 'Original Ask Amount',
                       'Original Offered Equity', 'Valuation Requested', 'Total Sales/Revenue', 'Profitable', 'Got Deal']

    df_filtered = df[feature_columns]
    df_filtered = pd.get_dummies(df_filtered, columns=['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State', 'Pitchers Average Age', 'Profitable'], 
                                 prefix=['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State', 'Pitchers Average Age', 'Profitable'])

    X = df_filtered.drop('Got Deal', axis=1)
    y = df_filtered['Got Deal']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

    return x_train, y_train, x_test, y_test

def print_metrics(y_pred, y_true, return_metrics=False):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    print("Accuracy: ", acc)
    print("Precision: ", prec)
    print("F1 Score: ", f1)
    if return_metrics: 
        return acc, prec, f1
