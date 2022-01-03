from typing import Type
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, HiddenField, StringField,  FloatField, BooleanField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, ValidationError

from datetime import datetime, timedelta
from random import randint
from logging.config import dictConfig

import sys

#Configuration for logging in production mode
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})



app = Flask(__name__)

# Flask-WTF enryption key 
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)

# ++++++++++++++
# Business logic
# ++++++++++++++

def calculate_base_insurance_charge(item_value, recipient_country): 
    #1. If package is being sent to the UK, insurance charge is 1% of the item
    if recipient_country == 'United Kingdom':
        print('country = UK')
        base_insurance_charge = (item_value / 100) * 1  
    #2. If package is being sent to France, Germany, Netherlands or Belgium, insurance charge is 1.5% value of item
    elif recipient_country == 'France' or recipient_country == 'Germany' or recipient_country == 'Netherlands' or recipient_country == 'Belgium':
        print('country = F, G, N, B')
        base_insurance_charge = (item_value / 100) * 1.5  
    #3. If package is being sent anywhere else, insurance charge is 4% of the value of the item
    else: 
        print('country = other')
        base_insurance_charge = (item_value / 100) * 4  
    #4. If insurance charge is less than £9, insurance charge - £9 
    if base_insurance_charge < 9.00:
        base_insurance_charge = 9
    return base_insurance_charge

    #5. Insurance premium tax calculate & round to two decimal places 
    # insurance_premium_tax = (insurance_charge / 100) * 12.5
    # final_insurance_charge = insurance_charge + insurance_premium_tax
    #6. Insurance charge is rounded to the nearest 0.01
    # return round(final_insurance_charge,2)

#5. Insurance premium tax calculate & round to two decimal places 
def calculate_insurance_premium_tax(base_insurance_charge): 
    insurance_premium_tax = (base_insurance_charge / 100) * 12.5
    print(insurance_premium_tax)
    return insurance_premium_tax

#6. Insurance charge is rounded to the nearest 0.01
def calculate_final_insurance_charge(base_insurance_charge, insurance_premium_tax ):
   final_insurance_charge = base_insurance_charge + insurance_premium_tax
   return round(final_insurance_charge)

# def generate_tracking_reference(n): 
#     range_start = 10**(n-1)
#     range_end = (10**n)-1
#     return randint(range_start, range_end)



# ++++++++++++++++++++++
# Create DB and DB model
# ++++++++++++++++++++++

# the name of the database; add path if necessary
db_name = 'orders.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String)
    sender_address = db.Column(db.String)
    sender_city = db.Column(db.String)
    sender_country = db.Column(db.String)

    recipient_name = db.Column(db.String)
    recipient_address = db.Column(db.String)
    recipient_city = db.Column(db.String)
    recipient_country = db.Column(db.String)

    package_value = db.Column(db.Float)
    contents_declaration = db.Column(db.String)
    despatch_date = db.Column(db.String)
    final_insurance_charge = db.Column(db.Float)
    insurance_premium_tax = db.Column(db.Float)
    insurance = db.Column(db.String)
    tracking_reference = db.Column(db.String)
    updated = db.Column(db.String)

    def __init__(self, 
                 sender_name, sender_address, sender_city, sender_country, 
                 recipient_name, recipient_address, recipient_city, recipient_country,
                 package_value, contents_declaration, despatch_date, final_insurance_charge, insurance_premium_tax,
                 insurance, tracking_reference, updated
                ):

        self.sender_name = sender_name
        self.sender_address = sender_address
        self.sender_city = sender_city
        self.sender_country = sender_country

        self.recipient_name = recipient_name
        self.recipient_address = recipient_address
        self.recipient_city = recipient_city
        self.recipient_country = recipient_country

        self.package_value = package_value
        self.contents_declaration = contents_declaration
        self.despatch_date = despatch_date
        self.final_insurance_charge = final_insurance_charge
        self.insurance_premium_tax = insurance_premium_tax
        self.insurance = insurance
        self.tracking_reference = tracking_reference
        self.updated = updated

# ++++++++++++++++++++++++++++++++++++
# Create Flask-WTF Form and Validation
# ++++++++++++++++++++++++++++++++++++

class AddRecord(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()

    #  Sender information
    sender_name = StringField('Sender Name', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Sender Name"),
        Length(min=3, max=25, message="Invalid Sender name length")
        ])
    sender_address = StringField('Sender Address', [ InputRequired(),
        # Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Sender Address"),
        Length(min=3, max=250, message="Invalid Sender Address length")
        ])
    sender_city = StringField('Sender City', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Sender City"),
        Length(min=3, max=25, message="Invalid Sender City length")
        ])
    sender_country = StringField('Sender Country', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Sender Country"),
        Length(min=3, max=25, message="Invalid Sender Country length")
        ])

    #  Recipient Information 
    recipient_name = StringField('Recipient Name', [ InputRequired(),
        # Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Recipient Name"),
        Length(min=3, max=25, message="Invalid Recipient name length")
        ])
    recipient_address = StringField('Recipient Address', [ InputRequired(),
        # Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Recipient Address"),
        Length(min=3, max=250, message="Invalid Recipient Address length")
        ])
    recipient_city = StringField('Recipient City', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Recipient City"),
        Length(min=3, max=25, message="Invalid Recipient City length")
        ])
    recipient_country = StringField('Recipient Country', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Recipient Country"),
        Length(min=3, max=25, message="Invalid Recipient Country length")
        ])

    #  Other Information
    package_value = FloatField('Package Value', [ InputRequired(),
        NumberRange(min=1.00, max=1000000, message="Invalid range")
        ]) 
    # def validate_value(FlaskForm, field): # This is not actually doing anything since the validation in the lines above covers the below consitions
        #Check that value is a positive number 
        # if type(field.data) != float or int:
        #     raise ValidationError('Error: package value is not a number')
        # elif field.data < 0.01:
        #     raise ValidationError('Error: package value must be a positive number')

    contents_declaration = StringField('Contents Declaration', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Contents Declaration"),
        Length(min=3, max=250, message="Invalid Contents Declaration length")
        ])

    despatch_date = DateField('Despatch Date') #  If date != today or tomorrow && insurance = true then... Error
    def validate_despatch_date(FlaskForm, field):
        #The despatch date must be today or tomorrow
        today = datetime.now().date()
        tomorrow = datetime.now().date() + timedelta(1)
        applicable_dates = []
        applicable_dates.append(today)
        applicable_dates.append(tomorrow)
        if field.data not in applicable_dates:
            raise ValidationError('Error: despatch date must be today or tomorrow')


    insurance = BooleanField('I would like insurance') 
    def validate_insurance(FlaskForm, field):
        #Packages with a value of over £10,000 cannot be insured
        try:
            if field.data == True and FlaskForm.package_value.data > 10000:
                raise ValidationError('Error: package value too high')
        except TypeError: # If package_value is not a number
            raise ValidationError('Error: Package Value must be a number')

    tracking_reference = HiddenField() 

    updated = HiddenField()  # updated = date - handled in the route function

    submit = SubmitField('Submit Order')

class SearchRecord(FlaskForm):
    #  Search by order reference number
    tracking_reference = StringField('Tracking Reference', [ InputRequired(),
        # Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid Sender Name"), # Should change regex so it only accepts numbers
        Length(min=3, max=25, message="Invalid Tracking Reference")
        ])
    submit = SubmitField('Search')

# +++++++++++++
# Create Routes
# +++++++++++++

#  View home page
@app.route("/")
def index():
    return render_template('index.html')

#  Add a new order to the database
@app.route('/orders', methods=['GET', 'PUT'])
def orders():
    form1 = AddRecord()
    if form1.validate_on_submit():
        #1. Collect data
        json_data = request.json
        #Sender
        sender_name = json_data['sender_name']
        sender_address = json_data['sender_address']
        sender_city = json_data['sender_city']
        sender_country = json_data['sender_country']
        #Recipiant
        recipiant_name = json_data['recipient_name']
        recipiant_address = json_data['recipient_address']
        recipiant_city = json_data['recipient_city']
        recipiant_country = json_data['recipient_country']
        #Other
        package_value = json_data['package_value']
        contents_declaration = json_data['contents_declaration']
        despatch_date = json_data['despatch_date']
        tracking_reference = json_data['tracking_reference']
        insurance = (json_data['insurance'][0])
        updated = datetime.now() # Get today's date and time 

        req = request.get_json() 
        print('API received an order - tracking reference:',tracking_reference)

        #2. Run functions to calculate insurance charges
        if insurance == 'y':
            base_insurance_charge = calculate_base_insurance_charge(float(package_value), recipiant_country)
            print('Base Insurance Charge:', base_insurance_charge) 
            insurance_premium_tax = calculate_insurance_premium_tax(base_insurance_charge)
            print('Insurance Premium Tax:', insurance_premium_tax)
            final_insurance_charge = calculate_final_insurance_charge(base_insurance_charge, insurance_premium_tax)
            print('Final Insurance Charge:', final_insurance_charge)
        else: 
            print('Insurance Status:',insurance)
            insurance_charge = 0 
            print('Insurance Charge: 0')

        #3. Save to DB 

        # The data to be inserted into Order model
        record = Order(sender_name, sender_address, sender_city, sender_country, 
                       recipiant_name, recipiant_address, recipiant_city, recipiant_country,
                       package_value, contents_declaration, despatch_date, final_insurance_charge, insurance_premium_tax,
                       insurance, tracking_reference, updated 
                      ) 
                
        # Flask-SQLAlchemy adds record to database
        db.session.add(record)
        db.session.commit()

        # Create a message to send to the template - this is not currently operational
        message = f"The data for your order to {recipiant_address} has been submitted. The Insurance charge for this order will be {final_insurance_charge}. The tracking reference for this order is {tracking_reference}"
        return render_template('order.html', message=message)
    else: #  If form does not pass validation
        # Show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        print('Form request not valid')
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
                print(error)
        return render_template('order.html', form1=form1)

#Search for orders 
@app.route("/search", methods=["GET", "POST"])
def search():
    form1 = SearchRecord()
    if request.method == "POST":
        tracking_reference = request.form['tracking_reference']
        print(tracking_reference) #Order 15 = 47433635 
        order = Order.query.filter_by(tracking_reference=tracking_reference).first_or_404()
        return render_template('order_details.html', tracking_reference=tracking_reference, order=order)
    else:
        return render_template('search_order.html', form1=form1)


# +++++++++++++++++++++++

if __name__ == '__main__':
    app.run(debug=False)
