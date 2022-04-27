from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

# from flask_restful import Resource, Api

app = Flask(__name__)
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
        #return '<prod_name %r>' % self.prod_id
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


@app.route('/pricing')
def pricing():
        return render_template('pricing.html')


@app.route('/form', methods = ['POST'])
def form():
    input_item = request.form['item']
    qty = int(request.form['qty'])
    id = request.form['id']
    returned_item = Items.query.get_or_404(id)
    newprice = int(returned_item.price_per_unit)
    tot_price = int(qty * newprice)
    return render_template('form.html', input_item=input_item, qty=qty, tot_price=tot_price)


@app.route('/exchangerate')
def exchange_rate():
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()
    try:
        exchange_rate = data['rates']
        form()
        exchange_amount = round((tot_price * exchange_rate[currency.upper()]), 2)
        return render_template('exchangerate.html')
    except KeyError as err:
        return jsonify({'message': 'Please enter valid currency'})
    #return render_template('exchangerate.html')


@app.route('/exchangerate/<string:currency>')
def exchange_rate_currency():
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()
    try:
        exchange_rate = data['rates']
        form()
        exchange_amount = round((tot_price * exchange_rate[currency.upper()]), 2)
        return render_template('exchangerate.html')
    except KeyError as err:
        return jsonify({'message': 'Please enter valid currency'})
    #return render_template('exchangerate.html')


@app.route('/')
def index():
    return render_template('index.html')



# @app.route('/items/<string:prod_name>/<int:num_prod>/<string:currency>')
# def get_currency_exchange(prod_name=None, num_prod=None, currency=None):
#     url = 'https://api.exchangerate.host/latest'
#     response = requests.get(url)
#     data = response.json()
#     try:
#         exchange_rate = data['rates']
#         pricing(prod_name, num_prod)
#         # if currency.islower() == 'True':
#         #     currency = currency.upper()
#         exchange_amount = round((tot_price * exchange_rate[currency.upper()]), 2)
#         return render_template('exchangerate.html', name=prod_name, currency=currency, exchange_amount=exchange_amount)
#     except KeyError as err:
#         return jsonify({'message': 'Please enter valid currency'})
