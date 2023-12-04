import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from word_analysis import get_top_words, create_tf_matrix
from sklearn.linear_model import LogisticRegression 


def get_data(return_pitches = False):
    # Read the original dataset
    df = pd.read_csv("Data/SharkTankUSdataset.csv")
    
    # Read profitability metrics
    new_metrics_df = pd.read_csv("Data/new_metrics/pitch_data.csv")

    # Read/get top words
    industries = ["Health_Wellness", "Food_Beverage", "Business_Services", "Lifestyle_Home",
                  "Software_Tech", "Children_Education", "Automative", "Fashion_Beauty",
                  "Media_Entertainment", "Fitness_Sports_Outdoors", "Pet_Products",
                  "Electronics", "Green_Clean_Tech", "Travel", "Liquor_Alcohol", "Uncertain_Other"]
    tfs, pitches_used, words = create_tf_matrix()
    industry_dfs = []
    top_words_df = -1
    top_words = []
    for idx, industry in enumerate(industries):
        temp_df = pd.read_csv("Data/Word_Frequency/" + industry + ".csv")
        top_n_words, n = get_top_words(tfs[idx], pitches_used[idx], words[idx])
        top_words = top_words + top_n_words
        top_words = np.unique(np.array(top_words)).tolist()
        if type(top_words_df) is int:
            top_words_df = temp_df.copy()
        else:
            top_words_df = pd.concat([top_words_df, temp_df], ignore_index=True)
            try:
                top_words_df = top_words_df[top_words]
            except:
                pass
    
    top_words_df = top_words_df[top_words]
    top_words_df.fillna(0, inplace=True)        

    df = pd.merge(df, new_metrics_df, on='Pitch Number')

    # Define the feature columns including the new ones
    feature_columns = ['Pitch Number', 'Industry', 'Pitchers Gender', 'Pitchers State', 'Pitchers Average Age', 'Original Ask Amount',
                       'Original Offered Equity', 'Valuation Requested', 'Total Sales/Revenue', 'Profitable', 'Got Deal']
    # feature_columns = ['Pitch Number', 'Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State',
    #                    'Pitchers Average Age', 'US Viewership', 'Original Ask Amount',
    #                    'Original Offered Equity', 'Valuation Requested', 'Total Sales/Revenue', 'Profitable', 'Got Deal']
    

    df_filtered = df[feature_columns]

    df_filtered = pd.merge(df_filtered, top_words_df, left_on='Pitch Number', right_index=True)
    pitches_used_flat = df_filtered['Pitch Number'].tolist()
    df_filtered = df_filtered.drop('Pitch Number', axis=1)
    df_filtered = pd.get_dummies(df_filtered, columns=['Industry', 'Pitchers Gender', 'Pitchers State', 'Pitchers Average Age'], 
                                 prefix=['Industry', 'Pitchers Gender', 'Pitchers State', 'Pitchers Average Age'])
    # df_filtered = pd.get_dummies(df_filtered, columns=['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State', 'Pitchers Average Age'], 
                                #  prefix=['Industry', 'Pitchers Gender', 'Pitchers City', 'Pitchers State', 'Pitchers Average Age'])

    X = df_filtered.drop('Got Deal', axis=1)
    y = df_filtered['Got Deal']

    if return_pitches: 
        return X, y, pitches_used_flat

    return X, y

def get_train_test():
    X, y = get_data()
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    return x_train, y_train, x_test, y_test

def log_reg_model():
    x, y = get_data()
    clf = LogisticRegression()
    clf = clf.fit(x, y)
    return clf

def print_metrics(y_pred, y_true, return_metrics=False):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    print("Accuracy: ", acc)
    print("Precision: ", prec)
    print("F1 Score: ", f1)
    if return_metrics: 
        return acc, prec, f1
