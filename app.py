from flask import Flask,session
from flask_login import LoginManager
from models import User,Staff,Center,Bookings,user_schema,staff_schema,center_schema,centers_schema,booking_schema
from models import db,ma
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user=session.get('user_cat')
    if user == "Staff":
        return Staff.query.get(user_id)
    else:
        return User.query.get(user_id)
    # staff_id = int(user_id)
    # return Staff.query.get(staff_id)

import routes


# @app.route("/",methods=['GET','POST'])
# @app.route("/login",methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         aadhar_no = request.form["aadhar_no"]
#         password = request.form["password"]
#         user = User.query.filter_by(aadhar_no=aadhar_no).first()
#         print(user_schema.dump(user))
#         if user and bcrypt.check_password_hash(user.password,password):
#             session["user_cat"]="User"
#             login_user(user)
#             print(f"User {current_user.first_name} logged in")
#             print(current_user.id)
#             return redirect(url_for('user_home'))
#         else:
#             return render_template('login.html',msg="Login failed")
#     else:
#         return render_template('login.html')


# @app.route("/staff_login",methods=['GET','POST'])
# def staff_login():
#     if request.method == 'POST':
#         staff_id = request.form["staff_id"]
#         password = request.form["password"]
#         staff = Staff.query.filter_by(staff_id=staff_id).first()
#         print(staff_schema.dump(staff))
#         if staff and bcrypt.check_password_hash(staff.password,password):
#             session["user_cat"]="Staff"
#             login_user(staff)
#             print(f"User {current_user.name} logged in")
#             print(current_user.staff_id)
#             return redirect(url_for('staff_home'))
#         else:
#             return render_template('staff_login.html',msg="Login failed")
#     else:
#         return render_template('staff_login.html')


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     print("user logged out")
#     return render_template('login.html')


# @app.route("/signup",methods=['GET','POST'])
# def signup():

#     if request.method == "POST":
#         fname = request.form["fname"]
#         lname = request.form["lname"]
#         mobile_no = int(request.form["mobile_no"])
#         aadhar_no = int(request.form["aadhar_no"])
#         password = request.form["password"]
#         birth_year = int(request.form["birth-year"])
#         email = request.form["email"]
#         hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
#         new_user=User(first_name=fname,
#                     last_name=lname,
#                     aadhar_no=aadhar_no,
#                     mobile_no=mobile_no,
#                     birth_year=birth_year,
#                     email=email,
#                     password=hashed_password,
#                     dose=0  )
#         db.session.add(new_user)
#         db.session.commit()
#         print("User added")
#         return render_template("login.html",msg="Signup successful...please login")

#     else:    
#         return render_template('signup.html')


# def get_user_data(user_id):
#     result = User.query.get(user_id)
#     user = user_schema.dump(result)
#     # print("user")
#     # print(user)
#     return user

# def get_staff_data(staff_id):
#     result = Staff.query.get(staff_id)
#     staff = staff_schema.dump(result)
#     # print("user")
#     # print(user)
#     return staff

# def get_user_appo(user_id):
#     result = Bookings.query.filter_by(user_id=user_id).first()
#     appo_data = booking_schema.dump(result)
#     print("appo_data")
#     print(appo_data)
#     return appo_data


# def get_aval_center_by_pincode(pincode):
#     result = Center.query.filter_by(pin_code=pincode)
#     centers = centers_schema.dump(result)
#     return centers

# def get_center(center_id):
#     result = Center.query.get(center_id)
#     center = center_schema.dump(result)
#     return center

# @app.route("/user_home")
# @login_required
# def user_home():
#     user_profile_data = get_user_data(current_user.id)
#     print("user_profile_data")
#     print(user_profile_data)

#     center_data={}
#     user_appo_data=get_user_appo(current_user.id)
#     if user_appo_data:
#         center_data = get_center(user_appo_data['center_id'])

#     msg = session.get("msg")
#     session["msg"]=None
#     return render_template('user_home.html',user_profile_data=user_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)


# @app.route("/staff_home")
# @login_required
# def staff_home():
#     staff_profile_data = get_staff_data(current_user.staff_id)
#     print("staff_profile_data")
#     print(staff_profile_data)
#     return "Hi i am staff "
#     # center_data={}
#     # user_appo_data=get_user_appo(current_user.staff_id)
#     # if user_appo_data:
#     #     center_data = get_center(user_appo_data['center_id'])

#     # msg = session.get("msg")
#     # session["msg"]=None
#     # return render_template('user_home.html',user_profile_data=staff_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)


# @app.route("/book_slot",methods=["GET","POST"])
# @login_required
# def book_slot(msg=None):
#     if request.method == "POST":
#         pincode = int(request.form['pincode'])
#         centers = get_aval_center_by_pincode(pincode)
#         session["pincode"]= pincode
#         # return jsonify(centers)
#         return render_template("book_my_slot.html",centers=centers,msg=None)
#     else:
#         return render_template("book_my_slot.html")
 
# @app.route("/book_slot/<int:center_id>",methods=["GET"])
# @login_required
# def book_my_slot(center_id):
#     result = Center.query.filter_by(center_id=center_id).first()
#     if  result.available_slots > 0:
        
#         # center = get_center(center_id)
#         appoinment = Bookings(user_id=current_user.id,center_id=center_id,booking_date=datetime.datetime.utcnow(),appointment_date=datetime.datetime.utcnow())
#         db.session.add(appoinment)
#         db.session.commit()
#         result.available_slots= int(result.available_slots)-1
#         db.session.commit()
#         pincode = session.get("pincode")
#         centers = get_aval_center_by_pincode(int(pincode))
#         # return render_template("book_my_slot.html",centers=centers,msg="Slot booked")
#         session["msg"]="Slot booked"
#         return redirect(url_for('user_home'))
#     else:
#         return "oops....Slots full"

    
#model

# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# bcrypt = Bcrypt()


# class User(db.Model,UserMixin):
#     __tablename__= 'users'
#     id=db.Column(db.Integer, primary_key=True)
#     first_name=db.Column(db.String(100), nullable=False)
#     last_name=db.Column(db.String(100), nullable=False)
#     aadhar_no=db.Column(db.Integer(), nullable=False)
#     birth_year=db.Column(db.Integer(), nullable=False)
#     email=db.Column(db.String(100),nullable=False)
#     mobile_no=db.Column(db.Integer(), nullable=False)
#     password=db.Column(db.String(100), nullable=False)
#     dose = db.Column(db.Integer(), nullable=True)
#     #vaccine_type=db.Column(db.String(100),nullable=False)
#     # does1_date=db.Column(db.String(20))
#     # does2_date=db.Column(db.Integer(20))


# class Staff(db.Model,UserMixin):
#     __tablename__= 'staff'
#     staff_id=db.Column(db.Integer, primary_key=True)
#     center_id=db.Column(db.Integer(), db.ForeignKey('centers.center_id'))
#     name=db.Column(db.String(100), nullable=False)
#     password=db.Column(db.String(50), nullable=False)

#     def get_id(self):
#         try:
#             return int(self.staff_id)
#         except:
#             raise NotImplementedError("No id")
    
# class Center(db.Model):
#     __tablename__= 'centers'
#     center_id=db.Column(db.Integer, primary_key=True)
#     center_name=db.Column(db.String(100), nullable=False)
#     city=db.Column(db.String(100), nullable=False)
#     district=db.Column(db.String(100), nullable=False)
#     pin_code=db.Column(db.String(100), nullable=False)
#     capacity=db.Column(db.String(100),nullable=False)
#     allocated_slots=db.Column(db.Integer, nullable=False)
#     available_slots=db.Column(db.Integer, nullable=False)
#     vaccine_type=db.Column(db.String(100),nullable=False)
#     type=db.Column(db.String, nullable=False)

#     # staff = db.relationship("Staff", backref="centers")

# class Bookings(db.Model):
#     __tablename__= 'bookings'
#     booking_id=db.Column(db.Integer, primary_key=True)
#     user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
#     center_id=db.Column(db.Integer,db.ForeignKey('centers.center_id'))
#     # vaccine_type=db.Column(db.String(100))
#     # type=db.Column(db.String,default='free')
#     booking_date=db.Column(db.DateTime, default=datetime.datetime.utcnow())
#     appointment_date=db.Column(db.DateTime, default=datetime.datetime.utcnow())

# class UserSchema(ma.Schema):
#     class Meta:
#         fields=("id","first_name","last_name","aadhar_no","birth_year","mobile_no","dose","email")

# class StaffSchema(ma.Schema):
#     class Meta:
#         fields=("staff_id","center_id","name")

# class CenterSchema(ma.Schema):
#     class Meta:
#         fields=("center_id","center_name","city","district","pin_code","capacity","allocated_slots","available_slots","vaccine_type","type")
    
# class BookingsSchema(ma.Schema):
#     class Meta:
#         fields=("booking_id","user_id","center_id","booking_date","appointment_date")

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# staff_schema = StaffSchema()
# staffs_schema = StaffSchema(many=True)

# center_schema = CenterSchema()
# centers_schema = CenterSchema(many=True)

# booking_schema = BookingsSchema()


# @app.cli.command("db_seed")
# def db_seed():
#     hashed_password = bcrypt.generate_password_hash("123").decode("UTF-8")
#     user1=User(first_name='Gaurav',
#                 last_name='Pingale',
#                 aadhar_no='4254',
#                 mobile_no=9767916589,
#                 birth_year=1999,
#                 email="gaurav@gmail.com",
#                 password=hashed_password,
#                 dose=0  )
#     user2=User(first_name='Shubham',
#                 last_name='Hazare',
#                 aadhar_no='4257',
#                 mobile_no=7894561235,
#                 birth_year=2000,
#                 email="shubham@gmail.com",
#                 password=hashed_password,
#                 dose=0  )
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.commit()
#     print("User added")
    
#     staff1=Staff(name="staff1",center_id=1,password=hashed_password)
#     staff2=Staff(name="staff2",center_id=2,password=hashed_password)
#     db.session.add(staff1)
#     db.session.add(staff2)
#     db.session.commit()
#     print("staff added")

#     center1= Center(center_name="C1",
#             city="pune",
#             district="Pune",
#             pin_code=411007,
#             capacity=180,
#             allocated_slots=180,
#             available_slots=120,
#             vaccine_type="covaxine",
#             type="free")
#     center2= Center(center_name="C2",
#             city="pune",
#             district="Pune",
#             pin_code=411007,
#             capacity=180,
#             allocated_slots=180,
#             available_slots=180,
#             vaccine_type="covishield",
#             type="free")

#     center3= Center(center_name="C3",
#             city="pune",
#             district="Pune",
#             pin_code=412208,
#             capacity=180,
#             allocated_slots=180,
#             available_slots=180,
#             vaccine_type="covishield",
#             type="paid")

#     db.session.add(center1)
#     db.session.add(center2)
#     db.session.add(center3)
#     db.session.commit()
#     print("center added")

if __name__ == "__main__":
    app.run(debug=True)