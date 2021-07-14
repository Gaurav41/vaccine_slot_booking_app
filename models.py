import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt 
from flask_login import UserMixin


db = SQLAlchemy()
ma = Marshmallow()
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
    #vaccine_type=db.Column(db.String(100),nullable=False)
    # does1_date=db.Column(db.String(20))
    # does2_date=db.Column(db.Integer(20))


class Staff(db.Model,UserMixin):
    __tablename__= 'staff'
    staff_id=db.Column(db.Integer, primary_key=True)
    center_id=db.Column(db.Integer(), db.ForeignKey('centers.center_id'))
    name=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(50), nullable=False)

    def get_id(self):
        try:
            return int(self.staff_id)
        except:
            raise NotImplementedError("No id")
    
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

class Bookings(db.Model):
    __tablename__= 'bookings'
    booking_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    center_id=db.Column(db.Integer,db.ForeignKey('centers.center_id'))
    # vaccine_type=db.Column(db.String(100))
    # type=db.Column(db.String,default='free')
    booking_date=db.Column(db.DateTime, default=datetime.datetime.utcnow())
    appointment_date=db.Column(db.DateTime, default=datetime.datetime.utcnow())

class UserSchema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","aadhar_no","birth_year","mobile_no","dose","email")

class StaffSchema(ma.Schema):
    class Meta:
        fields=("staff_id","center_id","name")

class CenterSchema(ma.Schema):
    class Meta:
        fields=("center_id","center_name","city","district","pin_code","capacity","allocated_slots","available_slots","vaccine_type","type")
    
class BookingsSchema(ma.Schema):
    class Meta:
        fields=("booking_id","user_id","center_id","booking_date","appointment_date")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

center_schema = CenterSchema()
centers_schema = CenterSchema(many=True)

booking_schema = BookingsSchema()


# @app.cli.command("db_seed")
def db_seed():
    hashed_password = bcrypt.generate_password_hash("123").decode("UTF-8")
    user1=User(first_name='Gaurav',
                last_name='Pingale',
                aadhar_no='4254',
                mobile_no=9767916589,
                birth_year=1999,
                email="gaurav@gmail.com",
                password=hashed_password,
                dose=0  )
    user2=User(first_name='Shubham',
                last_name='Hazare',
                aadhar_no='4257',
                mobile_no=7894561235,
                birth_year=2000,
                email="shubham@gmail.com",
                password=hashed_password,
                dose=0  )
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("User added")
    
    staff1=Staff(name="staff1",center_id=1,password=hashed_password)
    staff2=Staff(name="staff2",center_id=2,password=hashed_password)
    db.session.add(staff1)
    db.session.add(staff2)
    db.session.commit()
    print("staff added")

    center1= Center(center_name="C1",
            city="pune",
            district="Pune",
            pin_code=411007,
            capacity=180,
            allocated_slots=180,
            available_slots=120,
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

    center3= Center(center_name="C3",
            city="pune",
            district="Pune",
            pin_code=412208,
            capacity=180,
            allocated_slots=180,
            available_slots=180,
            vaccine_type="covishield",
            type="paid")

    db.session.add(center1)
    db.session.add(center2)
    db.session.add(center3)
    db.session.commit()
    print("center added")




def get_user_data(user_id):
    result = User.query.get(user_id)
    user = user_schema.dump(result)
    # print("user")
    # print(user)
    return user

def get_staff_data(staff_id):
    result = Staff.query.get(staff_id)
    staff = staff_schema.dump(result)
    # print("user")
    # print(user)
    return staff

def get_user_appo(user_id):
    result = Bookings.query.filter_by(user_id=user_id).first()
    appo_data = booking_schema.dump(result)
    print("appo_data")
    print(appo_data)
    return appo_data


def get_aval_center_by_pincode(pincode):
    result = Center.query.filter_by(pin_code=pincode)
    centers = centers_schema.dump(result)
    return centers

def get_center(center_id):
    result = Center.query.get(center_id)
    center = center_schema.dump(result)
    return center