from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
# from util import print_metrics
import pandas as pd
import re

def create_tf_matrix():
    # pitches = [health, food, bus, home, tech, child, auto, fash, media, fit, pet, electronics, green, travel, alc, other]
    pitches = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    p_used = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    data = pd.read_csv("Data/SharkTankUSdataset.csv")
    data = data[['Season Number', 'Episode Number', 'Pitch Number', 'Industry']]
    for index, pitch in data.iterrows():
        s = pitch['Season Number']
        ep = pitch['Episode Number']
        p = pitch['Pitch Number']
        industry = pitch['Industry']

        if (s == 11 and ep == 6) or s == 13 or (s == 14 and ep not in [2, 12, 20, 22]): continue

        file_path = 'Data/Pitch_Transcripts/Season_%s/Episode_%s/Pitch_%s.txt' % (s, ep, p)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        pitch_str = ' '.join(lines)
        pitch_str = re.sub(r'\d+', '', pitch_str)
        if industry == "Health/Wellness":
            pitches[0].append(pitch_str)
            p_used[0].append(p)
        elif industry == "Food and Beverage":
            pitches[1].append(pitch_str)
            p_used[1].append(p)
        elif industry == "Business Services":
            pitches[2].append(pitch_str)
            p_used[2].append(p)
        elif industry == "Lifestyle/Home":
            pitches[3].append(pitch_str)
            p_used[3].append(p)
        elif industry == "Software/Tech":
            pitches[4].append(pitch_str)
            p_used[4].append(p)
        elif industry == "Children/Education":
            pitches[5].append(pitch_str)
            p_used[5].append(p)
        elif industry == "Automotive":
            pitches[6].append(pitch_str)
            p_used[6].append(p)
        elif industry == "Fashion/Beauty":
            pitches[7].append(pitch_str)
            p_used[7].append(p)
        elif industry == "Media/Entertainment":
            pitches[8].append(pitch_str)
            p_used[8].append(p)
        elif industry == "Fitness/Sports/Outdoors":
            pitches[9].append(pitch_str)
            p_used[9].append(p)
        elif industry == "Pet Products":
            pitches[10].append(pitch_str)
            p_used[10].append(p)
        elif industry == "Electronics":
            pitches[11].append(pitch_str)
            p_used[11].append(p)
        elif industry == "Green/CleanTech":
            pitches[12].append(pitch_str)
            p_used[12].append(p)
        elif industry == "Travel":
            pitches[13].append(pitch_str)
            p_used[13].append(p)
        elif industry == "Liquor/Alcohol":
            pitches[14].append(pitch_str)
            p_used[14].append(p)
        elif industry == "Uncertain/Other":
            pitches[15].append(pitch_str)
            p_used[15].append(p)
        else:
            print("error, no: " + industry)


    vecs =[]
    tfs = []
    dense_tfs = []
    words = []
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    addt_words = ['like', 'gonna', 'll', 've', 'got', 'just', 'know', 'don', 'um', 'deal', 'ho', 'chuckles', 'laughs', 'phil', 'laughter', 'thank', 'darryl', 'yeah', 'yes', 're', 'oh', 'wow', 'okay', 'one', 'offer', 'get', 'lori', 'mark', 'would',
                  'kevin', 'robert', 'ryan', 'two', 'think', 'make', 'really', 'much', 'going', 'go', 'us', 'let', 'well', 'give', 'right', 'sure', 'love', 'lot', 'uh', 'jim', 'daymond', 'jason', 'jeff', 'annie', 'greiner', 'donny', 'george', 'cuban',
                  'kerry', 'alice', 'mm', 'hmm']
    all_stop_words = stop_words + addt_words
    for i in range(len(pitches)):
        vecs.append(CountVectorizer(stop_words=all_stop_words))
        tfs.append(vecs[i].fit_transform(pitches[i]))
        words.append(vecs[i].get_feature_names_out())
        dense_tfs.append(tfs[i].toarray())

    return dense_tfs, p_used, words


def get_top_words(category, pitch_numbers, words):
    df = pd.read_csv("Data/SharkTankUSdataset.csv")
    tf_df = pd.DataFrame(category, columns=words, index=pitch_numbers)
    
    feature_columns = ['Pitch Number', 'Pitchers Gender', 'Pitchers City', 'Pitchers State',
                        'Pitchers Average Age', 'US Viewership', 'Original Ask Amount',
                        'Original Offered Equity', 'Valuation Requested', 'Got Deal']

    df_filtered = df[feature_columns]
    df_filtered = pd.get_dummies(df_filtered, columns=['Pitchers Gender','Pitchers City','Pitchers State','Pitchers Average Age'], prefix=['Pitchers Gender','Pitchers City','Pitchers State','Pitchers Average Age'])
    df_merged = pd.merge(df_filtered, tf_df, left_on='Pitch Number', right_index=True)
    y = df_merged['Got Deal']
    X = df_merged.drop('Got Deal', axis=1)
    X = X.drop('Pitch Number', axis=1)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

    logreg = LogisticRegression() 
    logreg.fit(x_train, y_train)
    # y_preds = logreg.predict(x_test)
    # print_metrics(y_preds, y_test)

    coefs = logreg.coef_[0][-len(words):]

    word_coef_mapping = dict(zip(X.columns[-len(words):], coefs))
    
    abs_word_coef_mapping = {word: abs(coef) for word, coef in word_coef_mapping.items()}

    significant_words = sorted(abs_word_coef_mapping, key=abs_word_coef_mapping.get, reverse=True)

    n = 10
    top_n_words = significant_words[:n]
    return top_n_words, n
    

def save_as_csv(tfs, p_used, words):
    dfs = []

    for i, dense_ft in enumerate(tfs):
        df = pd.DataFrame(dense_ft, columns=words[i], index=p_used[i])
        dfs.append(df)

    if len(dfs) != 16: print("issue, not 16 categories")

    dfs[0].to_csv('Data/Word_Frequency/Health_Wellness.csv')
    dfs[1].to_csv('Data/Word_Frequency/Food_Beverage.csv')
    dfs[2].to_csv('Data/Word_Frequency/Business_Services.csv')
    dfs[3].to_csv('Data/Word_Frequency/Lifestyle_Home.csv')
    dfs[4].to_csv('Data/Word_Frequency/Software_Tech.csv')
    dfs[5].to_csv('Data/Word_Frequency/Children_Education.csv')
    dfs[6].to_csv('Data/Word_Frequency/Automative.csv')
    dfs[7].to_csv('Data/Word_Frequency/Fashion_Beauty.csv')
    dfs[8].to_csv('Data/Word_Frequency/Media_Entertainment.csv')
    dfs[9].to_csv('Data/Word_Frequency/Fitness_Sports_Outdoors.csv')
    dfs[10].to_csv('Data/Word_Frequency/Pet_Products.csv')
    dfs[11].to_csv('Data/Word_Frequency/Electronics.csv')
    dfs[12].to_csv('Data/Word_Frequency/Green_Clean_Tech.csv')
    dfs[13].to_csv('Data/Word_Frequency/Travel.csv')
    dfs[14].to_csv('Data/Word_Frequency/Liquor_Alcohol.csv')
    dfs[15].to_csv('Data/Word_Frequency/Uncertain_Other.csv')


def main():
    pitches = ["health", "food", "bus", "home", "tech", "child", "auto", "fash", "media", "fit", "pet", "electronics", "green", "travel", "alc", "other"]
    tfs, pitches_used, words = create_tf_matrix()
    # save_as_csv(tfs, pitches_used, words)
    for i in range(len(tfs)):
        print("category: ", pitches[i])
        print("total pitches: ", len(pitches_used[i]))
        top_n_words, n = get_top_words(tfs[i], pitches_used[i], words[i])
        print("Top ", n, " significant words: ", top_n_words)
        print()

if __name__ == "__main__":
    main()