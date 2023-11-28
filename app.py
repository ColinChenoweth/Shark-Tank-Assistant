from flask import Flask, render_template, url_for, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Specify the path to the R script in the 'Shiny' folder
    r_script_path = os.path.join('Shiny', 'my_app.R')
    r_script_path1 = os.path.join('Shiny', 'InvestmentPerSharkapp.R')

    # Run the R script
    subprocess.run(["Rscript", r_script_path])
    subprocess.run(["Rscript", r_script_path1])

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
        pitcher_gender = request.form.get('pitcherGender')
        pitcher_city = request.form.get('pitcherCity')
        pitcher_state = request.form.get('pitcherState')
        pitcher_age = request.form.get('pitcherAge')
        ask_amount = request.form.get('askAmount')
        equity_offered = request.form.get('equityOffered')
        profits_sales = request.form.get('profitsSales')
        description = request.form.get('description')

        return redirect('home')

    return render_template('form.html')


# Add other routes as needed

if __name__ == '__main__':
    app.run(debug=True)
