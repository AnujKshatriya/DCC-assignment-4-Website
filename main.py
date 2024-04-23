from flask import Flask,render_template,request
from urllib.parse import unquote_plus
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dcc-dbase"
db = SQLAlchemy(app)

class purchase(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    reference_no = db.Column(db.String(20),nullable = False)
    journal_data = db.Column(db.String(30),  nullable = False)
    purchase_date = db.Column(db.String(30), nullable = False)
    expiry_date = db.Column(db.String(30))
    purchaser_name = db.Column(db.String(120), nullable = False)
    prefix = db.Column(db.String(10), nullable = False)
    bond_no = db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    branch_code = db.Column(db.String(8), nullable = False)
    issue_teller = db.Column(db.String(14), nullable = False)
    status = db.Column(db.String(20), nullable = False)

class redemption(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    encashment_date = db.Column(db.String(40),nullable = False)
    party_name = db.Column(db.String(120),  nullable = False)
    account_no = db.Column(db.String(30), nullable = False)
    prefix = db.Column(db.String(30))
    bond_no= db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    branch_code = db.Column(db.String(8), nullable = False)
    pay_teller = db.Column(db.String(20), nullable = False)


@app.route('/search', methods=['GET'])
def search():
    # Get the search query parameters from the request
    table = request.args.get('table')  # Table to search (purchase or redemption)
    column = request.args.get('column')  # Column to filter
    query = request.args.get('query')  # Search query

    # Determine which table to search based on the 'table' parameter
    if table == 'purchase':
        model = purchase
    elif table == 'redemption':
        model = redemption
    else:
        return "Invalid table specified"

    # Perform the database query based on the provided parameters
    if column:  # If a specific column is provided for filtering
        results = model.query.filter(getattr(model, column).contains(query)).all()
    else:  # If no specific column is provided, search in all relevant columns
        results = model.query.filter(
            db.or_(
                purchase.sno.contains(query),
                purchase.reference_no.contains(query),
                purchase.journal_data.contains(query),
                # Add more columns for 'purchase' table as needed
            )
        ).all()

    # Separate the search results based on the table being searched
    purchase_results = []
    redemption_results = []
    for result in results:
        if isinstance(result, purchase):
            purchase_results.append(result)
        elif isinstance(result, redemption):
            redemption_results.append(result)

    # Render the search results in a template and pass the results as context variables
    return render_template("search_results.html", purchase_results=purchase_results, redemption_results=redemption_results)


@app.route('/company', methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        comp_name = request.form.get('comp_name')  # Retrieve selected company/individual from the form
        purchases = purchase.query.filter_by(purchaser_name=comp_name).all()

        year_totals = {}
        for purchase_item in purchases:  # Rename loop variable to avoid conflict
            year = purchase_item.purchase_date[-4:]
            if year in year_totals:
                year_totals[year]['total_count'] += 1
                year_totals[year]['total_sum'] += int(purchase_item.denominations.replace(',', ''))
            else:
                year_totals[year] = {'total_count': 1, 'total_sum': int(purchase_item.denominations.replace(',', ''))}

        return render_template('company.html', comp_name=comp_name, year_totals=year_totals)
    else:
        # Handle GET request to display the form
        return render_template('index.html')


@app.route('/party', methods=['GET'])
def party():
    selected_party = request.args.get('party')  # Retrieve party from query parameter
    party_data = redemption.query.filter_by(party_name=selected_party).all()

    year_totals = {
        year: {
            'total_sum': 0,
            'total_count': 0
        }
        for year in range(2019, 2025)  # Assuming the timeline ranges from 2019 to 2024
    }
    print(party_data)
    for pars in party_data:
        buys_date = pars.encashment_date
        
        if (buys_date[len(buys_date) - 1] == '9') :
        
            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2019']['total_sum'] += denominations_int
            year_totals['2019']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '0') :

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2020']['total_sum'] += denominations_int
            year_totals['2020']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '1') :

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2021']['total_sum'] += denominations_int
            year_totals['2021']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '2') :

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2022']['total_sum'] += denominations_int
            year_totals['2022']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '3') :

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2023']['total_sum'] += denominations_int
            year_totals['2023']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '4') :
            
            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2024']['total_sum'] += denominations_int
            year_totals['2024']['total_count'] += 1
    
    return render_template('party.html', selected_party=selected_party,year_totals=year_totals)

@app.route('/party_name', methods=['GET'])
def donations():
    party = request.args.get('party_name')
    parties = redemption.query.filter_by(party_name=party).all()
    donations = {}
    sum = 0 

    for pars in parties :
        bondno = pars.bond_no
        compny = purchase.query.filter_by(bond_no = bondno).all()
        for co in compny :
            denominations_str = co.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            sum += denominations_int
            if co.purchaser_name not in donations:
                donations[co.purchaser_name] = denominations_int
            else :
                donations[co.purchaser_name] += denominations_int
        
    return render_template('donations.html' , donations = donations , party = party , sum = sum)


@app.route('/')
def index():
    parties = db.session.query(redemption.party_name).distinct().all()
    companies = purchase.query.with_entities(purchase.purchaser_name).distinct().all()
    return render_template('index.html', companies=companies, parties=parties)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
