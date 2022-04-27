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


@app.route('/pricing', methods=['POST', 'GET'])
def pricing():
        return render_template('pricing.html')


@app.route('/form', methods = ['POST'])
def form():
    try:
        input_item = request.form['item']
        qty = int(request.form['qty'])
        id = request.form['id']
        currency = request.form['currency']
        returned_item = Items.query.get_or_404(id)
        if input_item == returned_item.prod_name:
            newprice = int(returned_item.price_per_unit)
            tot_price = int(qty * newprice)
            exchange_rate()
            exc_amount = (tot_price * exc_rate[currency.upper()])
            return render_template('form.html', input_item=input_item, qty=qty, tot_price=tot_price, currency=currency, exc_amount=exc_amount)
        else:
            return render_template('error.html')
    except KeyError as err1:
        return jsonify({'message': 'Please enter valid currency'})
    except ValueError as err2:
        return jsonify({'message': 'Please enter valid currency'})


@app.route('/error', methods=['POST', 'GET'])
def error():
    input_item = request.form['item']
    qty = int(request.form['qty'])
    id = request.form['id']
    currency = request.form['currency']
    return render_template('error.html', input_item=input_item, qty=qty, id=id, currency=currency)


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



