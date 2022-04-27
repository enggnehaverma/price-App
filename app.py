from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
from forex_python.converter import CurrencyRates, CurrencyCodes

app = Flask(__name__)   # Creating our Flask Instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)

global tot_price

# Create db model
class Items(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(50))
    price_per_unit = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a function to return string when we add something
    def __repr__(self):
        return f'<Items {self.prod_name}'

@app.route('/productlist', methods=['POST', 'GET'])
def product_list():
    if request.method == "POST":
        prod_name = request.form['name']
        price_per_unit = int(request.form['price'])
        items = Items(prod_name=prod_name, price_per_unit=price_per_unit)
        db.session.add(items)
        db.session.commit()
        return redirect('/productlist')
    else:
        new_list = Items.query.order_by(Items.date_created)
        return render_template('productlist.html', new_list=new_list)


@app.route('/pricing', methods=['POST', 'GET'])
def pricing():
        return render_template('pricing.html')


@app.route('/form', methods = ['POST'])
def form():
    try:
        tot_price = 0
        exc_amount = 0
        input_item = request.form['item']
        qty = int(request.form['qty'])
        currency = request.form['currency']
        new_list = Items.query.order_by(Items.date_created)
        for each in new_list:
            print(each)
            if each.prod_name == input_item:
                newprice_per_unit = int(each.price_per_unit)
                tot_price = int(qty * newprice_per_unit)
                exchange_rate()
                if currency.upper() not in exc_rate:
                    error_statement = "Please enter valid currency"
                    return render_template('form.html', error_statement=error_statement)
                exc_amount = round((tot_price * exc_rate[currency.upper()]),2)
                return render_template('form.html', input_item=input_item, qty=qty, tot_price=tot_price,
                                       currency=currency, exc_amount=exc_amount, new_list=new_list)
        return render_template('error.html')
    except KeyError as err1:
        return jsonify({'message': 'Please enter valid currency'})
    except ValueError as err2:
        return jsonify({'message': 'Please enter valid currency'})


@app.route('/error', methods=['POST', 'GET'])
def error():
    return render_template('error.html')


@app.route('/exchangerate')
def exchange_rate():
    global exc_rate
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()
    exc_rate = data['rates']
    return exc_rate


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete/<int:prod_id>')
def delete(prod_id):
    item_to_delete = Items.query.get_or_404(prod_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect('/productlist')


@app.route('/excrate', methods=['POST', 'GET'])
def exc_rate():
    from_curr = ''
    to_curr = ''
    amount = 0
    result = 0
    try:
        if request.method == "POST":
            rates = CurrencyRates()
            codes = CurrencyCodes()
            symbol = codes.get_symbol(to_curr)
            from_curr = request.form['from_curr'].upper()
            amount = float(request.form['amount'])
            to_curr = request.form['to_curr'].upper()
            result = round(rates.convert(from_curr, to_curr, amount), 2)
            return render_template('excratemessage.html', amount=amount, from_curr=from_curr, to_curr=to_curr, result=result, symbol=symbol)
        else:
            return render_template('excrate.html')
    except RatesNotAvailableError as err1:
        return redirect('excrate.html', err1=err1)