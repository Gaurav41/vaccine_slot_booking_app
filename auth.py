from functools import wraps
from logging import Logger
import traceback
import logging
from flask import session,request,render_template,redirect,url_for,abort
from flask.helpers import flash
from flask_login import LoginManager,login_user,login_required,logout_user,current_user

from models import User,Staff,user_schema,staff_schema,bcrypt

from error_logging import logger

logger=logging.getLogger(__name__)

from app import app
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user=session.get('user_cat')
    if user == "Staff":
        return Staff.query.get(user_id)
    else:
        return User.query.get(user_id)


@app.route("/",methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
@app.route("/login/<string:msg>",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try: 
            aadhar_no = request.form["aadhar_no"]
            password = request.form["password"]
            if (not aadhar_no) or (not password) :
                return render_template('login.html',msg="Enter all details")
            user = User.query.filter_by(aadhar_no=aadhar_no).first()
            print(user_schema.dump(user))
            if user and bcrypt.check_password_hash(user.password,password):
                session["user_cat"]="User"
                login_user(user)
                # print(f"User {current_user.first_name} logged in")
                # print(current_user.id)
                return redirect(url_for('user_home'))
            else:
                flash("Login failed... Enter valid credentials","danger")
                return render_template('login.html')
        except Exception as e:
            traceback.print_exc()
            logger.exception(e)
            flash("Something went wrong...try again","danger")
            return render_template('login.html')
                  
    else:
        return render_template('login.html')


@app.route("/staff_login",methods=['GET','POST'])
def staff_login():
    if request.method == 'POST':
        try:
            staff_id = request.form["staff_id"]
            password = request.form["password"]
            staff = Staff.query.filter_by(staff_id=staff_id).first()
            print(staff_schema.dump(staff))
            if staff and bcrypt.check_password_hash(staff.password,password):
                session["user_cat"]="Staff"
                login_user(staff)
                # print(f"User {current_user.name} logged in")
                # print(current_user.staff_id)
                return redirect(url_for('center_dashboard'))
            else:
                flash("Login failed","danger")
                return render_template('staff_login.html')
        except Exception as e:
            traceback.print_exc()
            logger.exception(e)
            flash("Something went wrong...try again","danger")
            return render_template('staff_login.html')
    else:
        return render_template('staff_login.html')


@app.route("/logout")
@login_required
def logout():
    
    logout_user()
    flash("You'r logged out")
    return redirect(url_for("login"))


def is_authorized_staff():

    if not(session["user_cat"]=="Staff"):
        return False
        # return redirect(url_for("staff_login")),403 
    else:
        return True


def is_authorized_user():

    if not(session["user_cat"]=="User"):
        return False
        # return redirect(url_for("staff_login")),403 
    else:
        return True

@login_manager.unauthorized_handler    
def unauthorized_callback():   
    # print("++++++-------------++++++++++++++--------------")         
    return redirect(url_for('login'))