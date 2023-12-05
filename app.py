from flask import Flask, render_template, url_for, request
from util import log_reg_model
from collections import Counter
import string
import numpy as np
import subprocess
import os

app = Flask(__name__, template_folder='templates')
clf = log_reg_model()

@app.route('/')
def index():
    # Specify the path to the R script in the 'Shiny' folder
    r_script_path = os.path.join('Shiny', 'my_app.R')
    r_script_path1 = os.path.join('Shiny', 'InvestmentPerSharkapp.R')

    # Run the R script
    subprocess.run(["Rscript", r_script_path])
    subprocess.run(["Rscript", r_script_path1])
    # subprocess.run(["C:\\Program Files\\R\\R-4.3.2\\bin\\Rscript.exe", r_script_path])
    # subprocess.run(["C:\\Program Files\\R\\R-4.3.2\\bin\\Rscript.exe", r_script_path1])

    # Render the HTML template that includes the graph
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Process form data here
        industry = request.form.get('industry')
        pitcher_gender = request.form.get('pitcherGender') # "Male", "Female", "Mixed Team"
        pitcher_city = request.form.get('pitcherCity')
        pitcher_state = request.form.get('pitcherState') # 2 letter abreviation all caps or Canada, NOT: ME NM, ND, SD, WV, WY
        pitcher_age = request.form.get('pitcherAge') # "Young", "Middle", "Old"
        ask_amount = int(request.form.get('askAmount'))
        equity_offered = float(request.form.get('equityOffered'))
        profits_sales = int(request.form.get('profitsSales')) # int or 
        description = request.form.get('description')

        if profits_sales == 0:
            profitable = 0
        else:
            profitable = 1

        money_data = [ask_amount, equity_offered, int(ask_amount * 100 / equity_offered), profits_sales, profitable]
        # pd.DataFrame([industry, pitcher_gender, pitcher_state, pitcher_age, ask_amount, equity_offered, (ask_amount * 100 / equity_offered), profits_sales],
        #                     columns=[('Industry_'+industry), ('Pitchers Gender_'+pitcher_gender), ('Pitchers State_'+pitcher_state),
        #                             'Pitchers Average Age','Original Ask Amount',
        #                             'Original Offered Equity', 'Valuation Requested', 'Total Sales/Revenue', 'Profitable'])

        
        description = description.translate(str.maketrans('', '', string.punctuation))
        words = description.lower().split()
        words_dict = dict(Counter(words))
        word_data = []
        top_words = ['actually', 'air', 'app', 'baby',
            'back', 'beer', 'believe', 'book', 'bottle', 'box', 'bulb', 'business', 'car',
            'cat', 'cheers', 'clothes', 'cold', 'come', 'company', 'could', 'dog', 'drew', 'equity',
            'feel', 'filter', 'food', 'funeral', 'good', 'great', 'guy', 'guys',
            'idea', 'job', 'light', 'look', 'luggage', 'made', 'mattress', 'million', 'money', 'need', 'nophone',
            'online', 'people', 'pet', 'phone', 'phones', 'point', 'potato',
            'problem', 'product', 'rack', 'royalty', 'rusty', 'sales', 'santa', 'say', 'see', 'sell', 'shark', 'sharks', 'skin', 'something',
            'take', 'talk', 'tell', 'thing', 'time', 'toy', 'tree', 'truck',
            'valuation', 'vegas', 'wait', 'want', 'way', 'work', 'year', 'yep']
        for w in top_words:
            word_data.append(words_dict.get(w, 0))


        industry_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        industries = ['Automotive', 'Business Services', 'Children/Education',
                    'Electronics', 'Fashion/Beauty', 'Fitness/Sports/Outdoors',
                    'Food and Beverage', 'Green/CleanTech', 'Health/Wellness',
                    'Lifestyle/Home', 'Liquor/Alcohol', 'Media/Entertainment',
                    'Pet Products', 'Software/Tech', 'Travel',
                    'Uncertain/Other']
        i = industries.index(industry)
        industry_data[i] = 1

        gender_data = [0, 0, 0]
        genders = ["Female", "Male", "Mixed Team"]
        i = genders.index(pitcher_gender)
        gender_data[i] = 1

        state_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0]        
        states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'Canada', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA',
                  'MA', 'MD', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'NE', 'NH', 'NJ', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'TN', 'TX',
                  'UT', 'VA','VT', 'WA', 'WI']
        i = states.index(pitcher_state)
        state_data[i] = 1

        age_data = [0, 0, 0]
        ages = ['Middle', 'Old', 'Young']
        i = ages.index(pitcher_age)
        age_data[i] = 1

        data = money_data + word_data + industry_data + gender_data + state_data + age_data

    #     columns = ['Original Ask Amount', 'Original Offered Equity', 'Valuation Requested',
    #    'Total Sales/Revenue', 'Profitable', 'actually', 'air', 'app', 'baby',
    #    'back', 'beer', 'believe', 'book', 'bottle', 'box', 'bulb', 'business', 'car',
    #    'cat', 'cheers', 'clothes', 'cold', 'come', 'company', 'could', 'dog', 'drew', 'equity',
    #    'feel', 'filter', 'food', 'funeral', 'good', 'great', 'guy', 'guys',
    #    'idea', 'job', 'light', 'look', 'luggage', 'made', 'mattress', 'million', 'money', 'need', 'nophone',
    #    'online', 'people', 'pet', 'phone', 'phones', 'point', 'potato',
    #    'problem', 'product', 'rack', 'royalty', 'rusty', 'sales', 'santa', 'say', 'see', 'sell', 'shark', 'sharks', 'skin', 'something',
    #    'take', 'talk', 'tell', 'thing', 'time', 'toy', 'tree', 'truck',
    #    'valuation', 'vegas', 'wait', 'want', 'way', 'work', 'year', 'yep', 'Industry_Automotive',
    #    'Industry_Business Services', 'Industry_Children/Education',
    #    'Industry_Electronics', 'Industry_Fashion/Beauty',
    #    'Industry_Fitness/Sports/Outdoors', 'Industry_Food and Beverage',
    #    'Industry_Green/CleanTech', 'Industry_Health/Wellness',
    #    'Industry_Lifestyle/Home', 'Industry_Liquor/Alcohol',
    #    'Industry_Media/Entertainment', 'Industry_Pet Products',
    #    'Industry_Software/Tech', 'Industry_Travel',
    #    'Industry_Uncertain/Other', 'Pitchers Gender_Female', 'Pitchers Gender_Male',
    #    'Pitchers Gender_Mixed Team', 'Pitchers State_AK', 'Pitchers State_AL',
    #    'Pitchers State_AR', 'Pitchers State_AZ', 'Pitchers State_CA',
    #    'Pitchers State_CO', 'Pitchers State_CT', 'Pitchers State_Canada',
    #    'Pitchers State_DC', 'Pitchers State_DE', 'Pitchers State_FL',
    #    'Pitchers State_GA', 'Pitchers State_HI', 'Pitchers State_IA',
    #    'Pitchers State_ID', 'Pitchers State_IL', 'Pitchers State_IN', 'Pitchers State_KS', 'Pitchers State_KY', 'Pitchers State_LA',
    #    'Pitchers State_MA', 'Pitchers State_MD', 'Pitchers State_MI',
    #    'Pitchers State_MN', 'Pitchers State_MO', 'Pitchers State_MS',
    #    'Pitchers State_MT', 'Pitchers State_NC', 'Pitchers State_NE',
    #    'Pitchers State_NH', 'Pitchers State_NJ', 'Pitchers State_NV',
    #    'Pitchers State_NY', 'Pitchers State_OH', 'Pitchers State_OK',
    #    'Pitchers State_OR', 'Pitchers State_PA', 'Pitchers State_RI', 'Pitchers State_SC', 'Pitchers State_TN',
    #    'Pitchers State_TX', 'Pitchers State_UT', 'Pitchers State_VA',
    #    'Pitchers State_VT', 'Pitchers State_WA', 'Pitchers State_WI',
    #    'Pitchers Average Age_Middle', 'Pitchers Average Age_Old',
    #    'Pitchers Average Age_Young']

        deal_pred = clf.predict_proba(np.array(data).reshape(1,-1))
        if deal_pred[0,0] < 0.5:
            output = ("Congratulations!! According to our model there is a high chance of getting a deal from one of the Sharks. " +
                      "It never hurts to keep imporving sales, however. Keep up the great work!")
        else:
            output = ("Unfortunatly, according to our model there is a low chance of your current deal getting accepted from one of the Sharks. " +
                      "We would suggest imporving your sales and/or asking for less from the sharks. It might even help to try changing up your pitch a little bit. " + 
                      "You got this!")
        # else:
        #     output = (f"This is a close one. According ot our model there is near a 50 precent chance of one of the sharks accepting your deal. " +
        #              "We would suggest imporving your sales and/or decreasing your asking amount for less from the sharks. It might even help to try changing up your pitch a little bit." +
        #               "Just some small changes can go a long way!")

        return render_template('results.html', output=output)

    return render_template('form.html')


# Add other routes as needed

if __name__ == '__main__':
    app.run(port=7000, debug=True)
