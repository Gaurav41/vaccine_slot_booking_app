from flask import request,redirect,render_template,url_for,session
from app import app
from flask_login import login_user,login_required,logout_user,current_user
from models import User,Staff,Center,Bookings,user_schema,staff_schema
from models import datetime,db,bcrypt,get_user_data,get_user_appo,get_staff_data,get_center,get_aval_center_by_pincode



@app.route("/",methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        aadhar_no = request.form["aadhar_no"]
        password = request.form["password"]
        user = User.query.filter_by(aadhar_no=aadhar_no).first()
        print(user_schema.dump(user))
        if user and bcrypt.check_password_hash(user.password,password):
            session["user_cat"]="User"
            login_user(user)
            print(f"User {current_user.first_name} logged in")
            print(current_user.id)
            return redirect(url_for('user_home'))
        else:
            return render_template('login.html',msg="Login failed")
    else:
        return render_template('login.html')


@app.route("/staff_login",methods=['GET','POST'])
def staff_login():
    if request.method == 'POST':
        staff_id = request.form["staff_id"]
        password = request.form["password"]
        staff = Staff.query.filter_by(staff_id=staff_id).first()
        print(staff_schema.dump(staff))
        if staff and bcrypt.check_password_hash(staff.password,password):
            session["user_cat"]="Staff"
            login_user(staff)
            print(f"User {current_user.name} logged in")
            print(current_user.staff_id)
            return redirect(url_for('staff_home'))
        else:
            return render_template('staff_login.html',msg="Login failed")
    else:
        return render_template('staff_login.html')


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


@app.route("/user_home")
@login_required
def user_home():
    user_profile_data = get_user_data(current_user.id)
    print("user_profile_data")
    print(user_profile_data)

    center_data={}
    user_appo_data=get_user_appo(current_user.id)
    if user_appo_data:
        center_data = get_center(user_appo_data['center_id'])

    msg = session.get("msg")
    session["msg"]=None
    return render_template('user_home.html',user_profile_data=user_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)


@app.route("/staff_home")
@login_required
def staff_home():
    staff_profile_data = get_staff_data(current_user.staff_id)
    print("staff_profile_data")
    print(staff_profile_data)
    return "Hi i am staff "
    # center_data={}
    # user_appo_data=get_user_appo(current_user.staff_id)
    # if user_appo_data:
    #     center_data = get_center(user_appo_data['center_id'])

    # msg = session.get("msg")
    # session["msg"]=None
    # return render_template('user_home.html',user_profile_data=staff_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)


@app.route("/book_slot",methods=["GET","POST"])
@login_required
def book_slot(msg=None):
    if request.method == "POST":
        pincode = int(request.form['pincode'])
        centers = get_aval_center_by_pincode(pincode)
        session["pincode"]= pincode
        # return jsonify(centers)
        return render_template("book_my_slot.html",centers=centers,msg=None)
    else:
        return render_template("book_my_slot.html")
 
@app.route("/book_slot/<int:center_id>",methods=["GET"])
@login_required
def book_my_slot(center_id):
    result = Center.query.filter_by(center_id=center_id).first()
    if  result.available_slots > 0:
        
        # center = get_center(center_id)
        appoinment = Bookings(user_id=current_user.id,center_id=center_id,booking_date=datetime.datetime.utcnow(),appointment_date=datetime.datetime.utcnow())
        db.session.add(appoinment)
        db.session.commit()
        result.available_slots= int(result.available_slots)-1
        db.session.commit()
        pincode = session.get("pincode")
        centers = get_aval_center_by_pincode(int(pincode))
        # return render_template("book_my_slot.html",centers=centers,msg="Slot booked")
        session["msg"]="Slot booked"
        return redirect(url_for('user_home'))
    else:
        return "oops....Slots full"