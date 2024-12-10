from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mysql%40123@10.0.0.5/parking'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_no = db.Column(db.String(255), unique=True, nullable=False)
    owner_name = db.Column(db.String(255), unique=True, nullable=False)
    owner_address = db.Column(db.String(255), unique=False, nullable=False)
    owner_dob = db.Column(db.String(255), unique=False, nullable=False)
    owner_license_type = db.Column(db.String(255), unique=False, nullable=False)
    owner_license_no = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, primary_key=False)

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(500), unique=True, nullable=False)
    latitude = db.Column(db.String(500), unique=True, nullable=False)
    longitude = db.Column(db.String(500), unique=True, nullable=False)

class FreeParking(db.Model):
    __tablename__ = 'free_parking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    vehicle_id = db.Column(db.Integer, unique=False, nullable=False)
    location_id = db.Column(db.Integer, unique=False, nullable=False)
    parking_date = db.Column(db.String(255), unique=False, nullable=False)
    parking_time = db.Column(db.String(255), unique=False, nullable=False)

class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    card_number = db.Column(db.String(255), unique=False, nullable=False)
    expiry = db.Column(db.String(255), unique=False, nullable=False)
    cvv = db.Column(db.String(255), unique=False, nullable=False)
    cardholder_name = db.Column(db.String(255), unique=False, nullable=False)
    txn_id = db.Column(db.String(255), unique=False, nullable=False)
    startdatetime = db.Column(db.String(255), unique=False, nullable=False)
    enddatetime = db.Column(db.String(255), unique=False, nullable=False)

class PaidParking(db.Model):
    __tablename__ = 'paid_parking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    vehicle_id = db.Column(db.Integer, unique=False, nullable=False)
    location_id = db.Column(db.Integer, unique=False, nullable=False)
    parking_date = db.Column(db.String(255), unique=False, nullable=False)
    parking_time = db.Column(db.String(255), unique=False, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Input validation
        if not name or not email or not password :
            return render_template('index.html', msg='All fields are required.')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check for existing username or email
        existing_user = User.query.filter_by(name=name).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template('index.html', msg='Username already exists. Please choose a different one.')
        elif existing_email:
            return render_template('index.html', msg='Email already exists. Please use a different one.')

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)

        try:
            db.session.commit()
            print("Database commit successful!")
            return render_template('index.html', msg='Signup successful. Now you can login.')
        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", str(e))
            return render_template('index.html', msg='An error occurred during signup.')

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve user based on the provided email
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # User exists and password matches
            session['user_id'] = user.id
            session['user_email'] = user.email
            return redirect(url_for('dashboard'))  
        else:
            # User doesn't exist or password is incorrect
            return render_template('index.html', msg='Invalid email or password. Please try again.')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))
        
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session.get('user_id'):
        msg = request.args.get('msg')
        if msg:
            return render_template('dashboard.html', msg=msg)
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))
    
def vehicle_exists(vehicle_no, user_id):
    existing_vehicle = Vehicle.query.filter_by(vehicle_no=vehicle_no, user_id=user_id).first()
    return existing_vehicle is not None

def insert_vehicle(vhno, oname, oaddress, odob, oltype, olnum, user_id):
    new_vehicle = Vehicle(vehicle_no=vhno, owner_name=oname, owner_address=oaddress, owner_dob=odob,
                          owner_license_type=oltype, owner_license_no=olnum, user_id=user_id)
    db.session.add(new_vehicle)
    try:
        db.session.commit()
        return True  # Insertion successful
    except Exception as e:
        db.session.rollback()
        return False  # Insertion failed
    
@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    msg = request.args.get('msg')
    if msg:
        vehicles = Vehicle.query.filter_by(user_id=session['user_id']).all()
        if vehicles:
            return render_template('vehicles.html', vehicles=vehicles, v_flag=1, msg=msg)
    if session.get('user_id'):
        if request.method == 'POST':
            vhno = request.form['vhno']
            oname = request.form['oname']
            oaddress = request.form['oaddress']
            odob = request.form['odob']
            oltype = request.form['oltype']
            olnum = request.form['olnum']

            if not vehicle_exists(vhno, session['user_id']):
                if insert_vehicle(vhno, oname, oaddress, odob, oltype, olnum, session['user_id']):
                    # Insertion successful
                    vehicles = Vehicle.query.filter_by(user_id=session['user_id']).all()
                    return render_template('vehicles.html',vehicles=vehicles, v_flag=1)
                else:
                    # Insertion failed
                    return render_template('vehicles.html', msg='Failed to insert vehicle data.')
            else:
                # Vehicle already exists
                return render_template('vehicles.html', msg='Vehicle with this number already exists.')
        
        vehicles = Vehicle.query.filter_by(user_id=session['user_id']).all()
        if vehicles:
            return render_template('vehicles.html', vehicles=vehicles, v_flag=1)
        else:
            return render_template('vehicles.html', vehicles=vehicles, v_flag=2)
    else:
        return redirect(url_for('index'))
    
def getAllLocations():
    locations = Location.query.all()
    if locations:
        return locations
    else:
        return 'not found'
app.jinja_env.globals.update(getAllLocations=getAllLocations) 

def getvehicledata(vid):
    vehicle = Vehicle.query.filter_by(id=vid).first()
    return vehicle
app.jinja_env.globals.update(getvehicledata=getvehicledata) 

def getlocationdata(lid):
    location = Location.query.filter_by(id=lid).first()
    return location
app.jinja_env.globals.update(getlocationdata=getlocationdata) 

@app.route('/park/vehicle', methods=['GET', 'POST'])
def parkvehicle():
    if request.method == 'POST':
        location_id = request.form['location_id']
        parking_date = request.form['parking_date']
        parking_time = request.form['parking_time']
        vehicle_id = request.form['vhid']

        # Check if the user has 5 or fewer parking records in FreeParking table
        parking_count = FreeParking.query.filter_by(user_id=session['user_id']).count()

        if parking_count < 5:
            # Check if the same row exists for the same time and date in FreeParking table
            existing_record = FreeParking.query.filter_by(
                user_id=session['user_id'],
                location_id=location_id,
                parking_date=parking_date,
                parking_time=parking_time
            ).first()

            if existing_record:
                return redirect(url_for('vehicles', msg='Parking record for the same time and date already exists'))
            else:
                # Insert a new parking record in FreeParking table
                new_parking = FreeParking(
                    user_id=session['user_id'],
                    vehicle_id=vehicle_id,
                    location_id=location_id,
                    parking_date=parking_date,
                    parking_time=parking_time
                )

                try:
                    db.session.add(new_parking)
                    db.session.commit()
                    return redirect(url_for('vehicles', msg='Parking has been added successfully!'))
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding record to FreeParking: {str(e)}")
                    return redirect(url_for('vehicles', msg='Unable to process parking!'))
        else:
            # Check if the user has an active subscription for the current period in Subscription table
            current_datetime = datetime.now()
            active_subscription = Subscription.query.filter(
                Subscription.user_id == session['user_id'],
                Subscription.startdatetime <= current_datetime,
                Subscription.enddatetime >= current_datetime
            ).first()

            print(f"Active Subscription: {active_subscription}")

            if active_subscription:
                # Insert a new parking record in PaidParking table
                new_paid_parking = PaidParking(
                    user_id=session['user_id'],
                    vehicle_id=vehicle_id,
                    location_id=location_id,
                    parking_date=parking_date,
                    parking_time=parking_time
                )

                try:
                    db.session.add(new_paid_parking)
                    db.session.commit()
                    return redirect(url_for('vehicles', msg='Parking has been added successfully!'))
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding record to PaidParking: {str(e)}")
                    return redirect(url_for('vehicles', msg='Unable to process parking!'))
            else:
                print("No active subscription found.")
                return redirect(url_for('buyplan'))

    return render_template('buy.html')

@app.route('/parkings', methods=['GET','POST'])
def parkings():
    if 'user_id' in session:
        # Get current datetime
        current_datetime = datetime.now()

        # Query FreeParking table for non-expired records
        free_parkings = FreeParking.query.filter(
            FreeParking.user_id == session['user_id'],
            FreeParking.parking_date >= current_datetime.strftime('%Y-%m-%d'),
            FreeParking.parking_time >= current_datetime.strftime('%H:%M:%S')
        ).all()

        # Query PaidParking table for non-expired records
        paid_parkings = PaidParking.query.filter(
            PaidParking.user_id == session['user_id'],
            PaidParking.parking_date >= current_datetime.strftime('%Y-%m-%d'),
            PaidParking.parking_time >= current_datetime.strftime('%H:%M:%S')
        ).all()

        # Combine the results from both tables
        all_parkings = free_parkings + paid_parkings

        return render_template('parkings.html', parkings=all_parkings)
    else:
        return redirect(url_for('index'))

@app.route('/buy', methods=['GET','POST'])
def buyplan():
    msg = request.args.get('msg')
    if msg:
        return render_template('buy.html', msg=msg)
    if 'user_id' in session:
        if request.method == 'POST':
            cardno = request.form['cardno']
            expiry = request.form['expiry']
            cvv = request.form['cvv']
            holder = request.form['holder']
            user_id = session['user_id']
            transaction_id = secrets.token_hex(6).upper()
            startdatetime = datetime.now()
            enddatetime = startdatetime + timedelta(days=30)

            # Check if a record already exists with the same startdatetime and enddatetime
            existing_record = Subscription.query.filter_by(
                user_id=user_id,
                startdatetime=startdatetime,
                enddatetime=enddatetime
            ).first()

            if existing_record:
                return render_template('buy.html', msg='Subscription with the same start and end dates already exists.')
            else:
                # Insert a new subscription record
                new_subscription = Subscription(
                    user_id=user_id,
                    card_number = cardno,
                    expiry = expiry,
                    cvv = cvv,
                    cardholder_name = holder,
                    txn_id = transaction_id,
                    startdatetime=startdatetime,
                    enddatetime=enddatetime
                )

                try:
                    db.session.add(new_subscription)
                    db.session.commit()
                    return redirect(url_for('dashboard', msg='Subscription added successfully'))
                except Exception as e:
                    db.session.rollback()
                    return render_template('buy.html', msg='An error occurred while adding the subscription')

        return render_template('buy.html')
    else:
        return redirect(url_for('index'))

@app.route('/admin')
@app.route('/admin/login', methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Retrieve user based on the provided email
        admin = Admin.query.filter_by(email=email).first()

        if admin and password == admin.password:
            # Admin exists and password matches
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            return redirect(url_for('admindashboard'))  
        else:
            # Admin doesn't exist or password is incorrect
            return render_template('admin_login.html', msg='Invalid email or password. Please try again.')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admindashboard():
    if 'admin_id' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('adminlogin'))

@app.route('/admin/add/location', methods=['GET', 'POST'])
def adminaddlocation():
    if 'admin_id' in session:
       if request.method == 'POST':
            place_name = request.form['plname']
            latitude = request.form['latname']
            longitude = request.form['longname']
            new_location = Location(place_name=place_name, latitude=latitude, longitude=longitude)
            db.session.add(new_location)
            try:
                db.session.commit()
                return render_template('add_location.html', msg='Location has been added successfully!')
            except Exception as e:
                db.session.rollback()
                return render_template('add_location.html', msg='Location has been failed to add!')
       return render_template('add_location.html')
    return redirect(url_for('adminlogin'))

@app.route('/admin/location/list')
def adminlocationlist():
    if 'admin_id' in session:
        locations = Location.query.all()
        if locations:
            return render_template('locations_list.html', locations=locations)
        else:
            return render_template('locations_list.html')
    return redirect(url_for('adminlogin'))

@app.route('/admin/location/delete', methods=['GET','POST'])
def admindeletelocation():
    if request.method == 'POST':
        lid = request.form['lid']
        location = Location.query.get(lid)
        if location:
            try:
                db.session.delete(location)
                db.session.commit()
                return redirect(url_for('adminlocationlist'))
            except Exception as e:
                db.session.rollback()
                return redirect(url_for('adminlocationlist'))
    
    
@app.route('/admin/logout')
def adminlogout():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    return redirect(url_for('adminlogin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
