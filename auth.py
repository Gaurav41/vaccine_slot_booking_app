from flask import session,request,render_template,redirect,url_for
from flask_login import LoginManager,login_user,login_required,logout_user,current_user

from models import User,Staff,user_schema,staff_schema,bcrypt

from app import app
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user=session.get('user_cat')
    if user == "Staff":
        print("***************************************************")
        return Staff.query.get(user_id)
    else:
        return User.query.get(user_id)
    # staff_id = int(user_id)
    # return Staff.query.get(staff_id)

@app.route("/",methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
@app.route("/login/<string:msg>",methods=['GET','POST'])
def login(msg=None):
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
        return render_template('login.html',msg=msg)


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
            return redirect(url_for('center_dashboard'))
        else:
            return render_template('staff_login.html',msg="Login failed")
    else:
        return render_template('staff_login.html')


@app.route("/logout")
def logout():
    logout_user()
    print("user logged out")
    return redirect(url_for("login"))
