from flask import Flask,request,redirect,render_template,session
from flask.helpers import url_for
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt 

from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config['SECRET_KEY']="AHSDKHADK68468ASDASD"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        aadhar_no = request.form["aadhar_no"]
        password = request.form["password"]
        user = User.query.filter_by(aadhar_no=aadhar_no).first()
        print(user_schema.dump(user))
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            print(f"User {current_user.first_name} logged in")
            return redirect(url_for('book_slot'))
        else:
            return render_template('login.html',msg="Login failed")
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("user logged out")
    return render_template('login.html')


@app.route("/signup",methods=['GET','POST'])
def signup():

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile_no = int(request.form["mobile_no"])
        aadhar_no = int(request.form["aadhar_no"])
        password = request.form["password"]
        birth_year = int(request.form["birth-year"])
        email = request.form["email"]
        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
        new_user=User(first_name=fname,
                    last_name=lname,
                    aadhar_no=aadhar_no,
                    mobile_no=mobile_no,
                    birth_year=birth_year,
                    email=email,
                    password=hashed_password,
                    dose=0  )
        db.session.add(new_user)
        db.session.commit()
        print("User added")
        return render_template("login.html",msg="Signup successful...please login")

    else:    
        return render_template('signup.html')


def get_aval_center_by_pincode(pincode):
    result = Center.query.filter_by(pin_code=pincode)
    centers = centers_schema.dump(result)
    return centers


@app.route("/book_slot",methods=["GET","POST"])
@login_required
def book_slot(msg=None):
    if request.method == "POST":
        pincode = int(request.form['pincode'])
        centers = get_aval_center_by_pincode(pincode)
        session["pincode"]= pincode
        # return jsonify(centers)
        return render_template("user_home.html",centers=centers,msg=None)
    else:
        return render_template("user_home.html")
 
@app.route("/book_slot/<int:center_id>",methods=["GET"])
@login_required
def book_my_slot(center_id):
    result = Center.query.filter_by(center_id=center_id).first()
    if  result.available_slots > 0:
        result.available_slots= int(result.available_slots)-1
        db.session.commit()
        pincode = session.get("pincode")
        centers = get_aval_center_by_pincode(int(pincode))
        
        return render_template("user_home.html",centers=centers,msg="Slot booked")
    else:
        return "oops....Slots full"

    
#model

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt()


class User(db.Model,UserMixin):
    __tablename__= 'users'
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100), nullable=False)
    last_name=db.Column(db.String(100), nullable=False)
    aadhar_no=db.Column(db.Integer(), nullable=False)
    birth_year=db.Column(db.Integer(), nullable=False)
    email=db.Column(db.String(100),nullable=False)
    mobile_no=db.Column(db.Integer(), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    dose = db.Column(db.Integer(), nullable=True)

    # does1_date=db.Column(db.String(20))
    # does2_date=db.Column(db.Integer(20))


class Staff(db.Model):
    __tablename__= 'staff'
    staff_id=db.Column(db.Integer, primary_key=True)
    center_id=db.Column(db.Integer(), db.ForeignKey('centers.center_id'))
    name=db.Column(db.String(100), nullable=False)

    
class Center(db.Model):
    __tablename__= 'centers'
    center_id=db.Column(db.Integer, primary_key=True)
    center_name=db.Column(db.String(100), nullable=False)
    city=db.Column(db.String(100), nullable=False)
    district=db.Column(db.String(100), nullable=False)
    pin_code=db.Column(db.String(100), nullable=False)
    capacity=db.Column(db.String(100),nullable=False)
    allocated_slots=db.Column(db.Integer, nullable=False)
    available_slots=db.Column(db.Integer, nullable=False)
    vaccine_type=db.Column(db.String(100),nullable=False)
    type=db.Column(db.String, nullable=False)

    # staff = db.relationship("Staff", backref="centers")
    
class UserSchema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","aadhar_no","birth_year","mobile_no","dose","email","password")

class StaffSchema(ma.Schema):
    class Meta:
        fields=("staff_id","center_id","name")

class CenterSchema(ma.Schema):
    class Meta:
        fields=("center_id","center_name","city","district","pin_code","capacity","allocated_slots","available_slots","vaccine_type","type")
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)

staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

center_schema = CenterSchema()
centers_schema = CenterSchema(many=True)

@app.cli.command("db_seed")
def db_seed():
    hashed_password = bcrypt.generate_password_hash("123").decode("UTF-8")
    user1=User(first_name='Gaurav',
                last_name='Gaurav',
                aadhar_no='Sun',
                mobile_no=9767916589,
                birth_year=1999,
                email="gaurav@gmail.com",
                password=hashed_password,
                dose=0  )
    db.session.add(user1)
    db.session.commit()
    print("User added")
    
    staff_user=Staff(name="staff1",center_id=1)
    db.session.add(staff_user)
    db.session.commit()
    print("staff added")

    center1= Center(center_name="C1",
            city="pune",
            district="Pune",
            pin_code=411007,
            capacity=180,
            allocated_slots=180,
            available_slots=180,
            vaccine_type="covaxine",
            type="free")
    center2= Center(center_name="C2",
            city="pune",
            district="Pune",
            pin_code=411007,
            capacity=180,
            allocated_slots=180,
            available_slots=180,
            vaccine_type="covishield",
            type="free")
    db.session.add(center1)
    db.session.add(center2)
    db.session.commit()
    print("center1 added")

if __name__ == "__main__":
    app.run(debug=True)