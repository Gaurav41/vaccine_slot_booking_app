from flask import request,redirect,render_template,url_for,session,jsonify
from app import app
from flask_login import login_required,current_user
from models import User,Center,Bookings,get_users_data,user_and_appo_data
from models import datetime,db,bcrypt,get_center_appo,get_user_data,get_user_appo,get_staff_data,get_center,get_aval_center_by_pincode


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
        return redirect(url_for("login",msg="Signup successful...please login"))

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
    return "Hi"
    # return "Hi i am staff "
    # center_data={}
    # user_appo_data=get_user_appo(current_user.staff_id)
    # if user_appo_data:
    #     center_data = get_center(user_appo_data['center_id'])

    # msg = session.get("msg")
    # session["msg"]=None
    # return render_template('user_home.html',user_profile_data=staff_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)
@app.route("/center_dashboard")
def center_dashboard():
    center =get_center(current_user.center_id) 
    data=user_and_appo_data()
    return render_template('center_dashboard.html',center=center,data=data)


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
        appoinment = Bookings(user_id=current_user.id,center_id=center_id,booking_date=datetime.datetime.utcnow(),appointment_date=datetime.date.today())
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

@app.route("/shot_done/<int:user_id>",methods=["GET"])
@login_required
def shot_done(user_id):
    result = User.query.filter_by(id=user_id).first()
    result.dose = result.dose + 1
    Bookings.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return redirect(url_for("center_dashboard"))



@app.route("/test")
def test():
   data=user_and_appo_data()
   print(data)
   return "joins"

