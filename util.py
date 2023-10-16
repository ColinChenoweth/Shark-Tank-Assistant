import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    #features: industry, pitchers gender, pitchers city, pitchers state, pitchers average age, US Viewwership, Original Ask Amount, Original Offered Equity, Valuation Requested
    #classification: got deal
    #return x_train, y_train, x_test, y_test
    #make sure to set random seed and shuffle (so shuffles the same everytime
    df = pd.read_csv("Data/SharkTankUSdataset.csv")
    
    feature_columns = ['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State',
                        'Pitchers Average Age', 'US Viewership', 'Original Ask Amount',
                        'Original Offered Equity', 'Valuation Requested', 'Got Deal']
    
    df_filtered = df[feature_columns]
    df_filtered = pd.get_dummies(df_filtered, columns=['Industry','Pitchers Gender','Pitchers City','Pitchers State','Pitchers Average Age'], prefix=['Industry','Pitchers Gender','Pitchers City','Pitchers State','Pitchers Average Age'])
    X = df_filtered.drop('Got Deal', axis=1)
    y = df_filtered['Got Deal']
    

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    
    return x_train, y_train, x_test, y_test