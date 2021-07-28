from flask import request,redirect,render_template,url_for,session,jsonify,json,flash,abort
from flask_sqlalchemy import model
import datetime
import traceback
import logging
from app import app
from flask_login import login_required,current_user
from models import User,Center,Bookings,get_user_vaccination_data,user_and_appo_data,db_create,UserVaccination,user_and_appo_data_sroted
from models import db,bcrypt,get_center_appo,get_user_data,get_user_appo,get_staff_data,get_center,get_aval_center_by_pincode
from auth import is_authorized_staff
from error_logging import logger

logger=logging.getLogger(__name__)

@app.route("/signup",methods=['GET','POST'])
def signup():
     
    if request.method == "POST":
        try:
            fname = request.form["fname"]
            lname = request.form["lname"]
            mobile_no = int(request.form["mobile_no"])
            aadhar_no = int(request.form["aadhar_no"])
            password = request.form["password"]
            birth_year = int(request.form["birth-year"])
            email = request.form["email"]
            if ( fname.strip()=="") or (lname.strip()=="") or (not mobile_no) or (not aadhar_no) or (password.strip()=="") or (birth_year> datetime.datetime.now().year) or (email.strip == ""):
                # msg = "Enter all field or enter valid details"
                flash("Enter all field or enter valid details","danger")
                return render_template('signup.html')

            if  User.query.filter_by(aadhar_no=aadhar_no).first():
                flash("User with same adhar no alredy exists","danger")
                return render_template('signup.html')

            hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
            new_user=User(first_name=fname,
                        last_name=lname,
                        aadhar_no=aadhar_no,
                        mobile_no=mobile_no,
                        birth_year=birth_year,
                        email=email,
                        password=hashed_password,
                        dose=0)
            db.session.add(new_user)
            db.session.commit()
            print("User added")
            flash("Signup successful...please login","success")
            return redirect(url_for("login"))
        except Exception as e:
            logger.exception(e)
            flash("Something went wrong...try again","danger")
            return render_template('signup.html')

    else:    
        return render_template('signup.html')


@app.route("/user_home")
@login_required
def user_home():
    try:
        user_profile_data = get_user_data(current_user.id)
        # print("user_profile_data")
        # print(user_profile_data)

        center_data={}
        user_appo_data=get_user_appo(current_user.id)
        print("user_appo_data")
        print(user_appo_data)
        user_vaccination_data=get_user_vaccination_data(current_user.id)
        # print("--------------------------user_vaccination_data---------------")
        # print(user_vaccination_data)

        book_btn=None
        if user_vaccination_data:
            d1_date = user_vaccination_data['d1_date']
            # d1_date = datetime.datetime.fromisoformat(d1_date)
            # day_diff = (datetime.datetime.now()-d1_date).days
            if (user_vaccination_data['day_diff']) < 84 :
                book_btn = "disabled"
                next_does_after= 84-user_vaccination_data['day_diff']
                user_vaccination_data['next_does_after']=next_does_after
            
        if user_appo_data:
            book_btn = "disabled"

        user_profile_data['book_btn']=book_btn

        if user_appo_data:
            center_data = get_center(user_appo_data['center_id'])

        msg = session.get("msg")
        # session["msg"]=None
        # flash(msg,"danger")
        return render_template('user_home.html',user_profile_data=user_profile_data,user_appo_data=user_appo_data,center_data=center_data,user_vaccination_data=user_vaccination_data)
    except Exception as e:
        traceback.print_exc()
        logger.exception(e)
        flash("Some error occured while loading user home, Try again later...","danger")
        return redirect(url_for('login'))

        

@app.route("/staff_home")
@login_required
def staff_home():
   
    try:
        staff_profile_data = get_staff_data(current_user.staff_id)
        # print("staff_profile_data")
        # print(staff_profile_data)
        return staff_profile_data
    except Exception as e:
        logger.exception(e)
        
    # return "Hi i am staff "
    # center_data={}
    # user_appo_data=get_user_appo(current_user.staff_id)
    # if user_appo_data:
    #     center_data = get_center(user_appo_data['center_id'])

    # msg = session.get("msg")
    # session["msg"]=None
    # return render_template('user_home.html',user_profile_data=staff_profile_data,user_appo_data=user_appo_data,center_data=center_data,msg=msg)

@app.route("/center_dashboard")
@login_required
def center_dashboard():
    if is_authorized_staff():
        try:
            center_data =get_center(current_user.center_id) 
            # user_appo_data=user_and_appo_data(current_user.center_id)
            show_only = request.args.get("show")
            order = request.args.get("order")
            sort_by = request.args.get("sort_by")
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            page=request.args.get('page',1,type=int)
            user_appo_data= user_and_appo_data_sroted(current_user.center_id,show_only=show_only,sort_by=sort_by, order=order,start_date=start_date,end_date=end_date,page=page)
            logged_in_staff_data = get_staff_data(current_user.staff_id)
            # print("******************************************************")
            # print(logged_in_staff_data)
            # print('user_appo_data')
            # print(user_appo_data)              
            errmsg=""
            if session.get("errmsg"):
                errmsg = session.get("errmsg")
                flash(errmsg,"danger")
            return render_template('center_dashboard.html', center=center_data,data=user_appo_data,logged_in_staff_data=logged_in_staff_data)
        except Exception as e:
            traceback.print_exc()
            logger.exception(e)
            flash("Some error occured, Try again later...","danger")
            return render_template('staff_login.html')
    else :
        flash("You are not a authorised staff to access this page","warning")
        abort(403)
        # return redirect(url_for("staff_login")),403

@app.route("/book_slot",methods=["GET","POST"])
@login_required
def book_slot(msg=None):
    try:
        if request.args.get('pincode'):
            pincode = int(request.args.get('pincode'))
            page=request.args.get('page',1,type=int)
            centers = get_aval_center_by_pincode(pincode,page)
            session["pincode"]= pincode
            # return jsonify(centers)
            print(centers)
            return render_template("book_my_slot.html",centers=centers)
        else:
            user_vaccination_data=get_user_vaccination_data(current_user.id)
            if user_vaccination_data:
                d1_date = user_vaccination_data['d1_date']
                d1_date = datetime.datetime.fromisoformat(d1_date)
                day_diff = (datetime.datetime.now()-d1_date).days
                if (day_diff) < 84 :
                    # session['msg']="You cannot book slot before 84 days"
                    flash("You cannot book slot before 84 days","warning")
                    return redirect(url_for('user_home'))
            return render_template("book_my_slot.html")
    except Exception as e:
        logger.exception(e)
        traceback.print_exc()
        flash("Some error occured, Try again later...","danger")
        return render_template("book_my_slot.html",centers=None)
 

@app.route("/book_slot/<int:center_id>",methods=["GET"])
@login_required
def book_my_slot(center_id):
    result = Center.query.filter_by(center_id=center_id).first()
    try:
        if  result.available_slots > 0:
            # datetime.fromisoformat("2021-04-15T00:00:00")
            # center = get_center(center_id)
            appoinment = Bookings(user_id=current_user.id,center_id=center_id,vaccine=result.vaccine_type,booking_date=datetime.datetime.utcnow(),appointment_date=datetime.date.today())
            db.session.add(appoinment)
            db.session.commit()
            result.available_slots= int(result.available_slots)-1
            db.session.commit()            
            session["msg"]="Slot booked"
            flash("Your Slot booked successfully","success")
            return redirect(url_for('user_home'))
        else:
            flash("Oops....Slots full","danger")
            return redirect(url_for('user_home'))
        
    # except AttributeError as e:
    #     print(e)
    #     # session["msg"]="Something went wrong..try again"
    #     flash("Some error occured, Try again later...","danger")
    #     return redirect(url_for('user_home'))
    
    except Exception as e:
        logger.exception(e)
        traceback.print_exc()
        flash("Some error occured while booking an appointment, Try again later...","danger")
        return redirect(url_for('user_home'))


@app.route("/shot_done/<int:user_id>",methods=["GET"])
@login_required
def shot_done(user_id):
    try:
        result = User.query.filter_by(id=user_id).first()
        # result.dose = result.dose + 1
        user_booking = Bookings.query.filter_by(user_id=user_id).first()
        # db.session.commit()
        
        if(result.dose==0):
            result.dose = 1
        # vaccine=user_booking.vaccine,
            user_vaccination=UserVaccination(user_id=user_id,
                                            d1_status="done",
                                            vaccine=user_booking.vaccine,
                                            d1_date=datetime.date.today(),
                                            d1_center_id=current_user.center_id,
                                            d1_staff_id=current_user.staff_id,
                                            d2_status="not done",
                                            d2_date=None,
                                            d2_center_id=None,
                                            d2_staff_id=None)
            db.session.add(user_vaccination)
            db.session.commit()
            # print("*****user_vaccination data added")

        elif(result.dose ==1):
            rows_changed = UserVaccination.query.filter_by(user_id=user_id).update(dict(d2_status="done",d2_date=datetime.date.today(),d2_center_id=current_user.center_id,d2_staff_id=current_user.staff_id))
            result.dose = 2
            db.session.commit()
            # print("****user_vaccination data updated")

        # Bookings.query.filter_by(user_id=user_id).delete()
        user_booking.status='Done'
        db.session.commit()
        flash(f"{result.first_name}\'s Vaccination done","success")
        return redirect(url_for("center_dashboard"))
        
    except Exception as e:
        logger.exception(e)
        traceback.print_exc()
        errmsg = f"Something went wrong while updating vaccination shot done of user {result.first_name}"
        # session["errmsg"]=errmsg
        flash(errmsg)
        return redirect(url_for("center_dashboard"))


# from models import add_centers,get_the_centers

@app.route("/test")
def test():
    # db_create()
    # return json.dumps(models_test())
    # data = user_and_appo_data_sroted(1) 
    # print(data)
    # return(json.dumps(data))
#    data=user_and_appo_data()
#    print(data)
#    return "joins"
    # add_centers()
    
    return "test"


