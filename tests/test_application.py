
from flask import Flask
import pytest
from app import app,db
from models import User,Staff,Center

# def test_base_route():
#     client = app.test_client()
#     url="/"
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 
# #    app.run(debug=True)

@pytest.fixture
def client():
    # Prepare before your test
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests/test_db.db"

    # with app.test_client() as client:
    #     # Give control to your test
    #     yield client
    # # Cleanup after the test run.
    # # ... nothing here, for this simple example

    client = app.test_client()
    # with app.app_context():
    #     create_and_seed_db()
        
    yield client


def create_and_seed_db():
    db.create_all()
    new_user=User(first_name="author",
                        last_name="author",
                        aadhar_no=9999,
                        mobile_no=9874568596,
                        birth_year=1993,
                        email="author@gmail.com",
                        password="$2b$12$IGY0p1EaRPhxFugqUxJzu.05ZaWaH8hfR9RRE8gYGbCKW7svVvHAC",
                        dose=0)
    db.session.add(new_user)
    user1=User(first_name='Gaurav',
            last_name='Pingale',
            aadhar_no='100',
            mobile_no=9767916589,
            birth_year=1999,
            email="gaurav@gmail.com",
            password="$2b$12$IGY0p1EaRPhxFugqUxJzu.05ZaWaH8hfR9RRE8gYGbCKW7svVvHAC",
            dose=0  )
    db.session.add(user1)

    hashed_password = "$2b$12$IGY0p1EaRPhxFugqUxJzu.05ZaWaH8hfR9RRE8gYGbCKW7svVvHAC"
    staff1=Staff(name="staff1",center_id=1,password=hashed_password)
    staff2=Staff(name="staff4",center_id=1,password=hashed_password)
    db.session.add(staff1)
    db.session.add(staff2)

    center1= Center(center_name="Center C1",
        city="pune",
        district="Pune",
        pin_code=411007,
        capacity=180,
        allocated_slots=180,
        available_slots=120,
        vaccine_type="covaxine",
        type="free")
    
    center2= Center(center_name="Center C2",
        city="pune",
        district="Pune",
        pin_code=412208,
        capacity=180,
        allocated_slots=180,
        available_slots=120,
        vaccine_type="covaxine",
        type="free")
    db.session.add(center1)
    db.session.add(center2)
    db.session.commit()


def user_login(client, aadhar_no, password):
    return client.post('/login', data=dict(
        aadhar_no=aadhar_no,
        password=password
    ), follow_redirects=True)

def staff_login(client, staff_id, password):
    return client.post('/staff_login', data=dict(
        staff_id=staff_id,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_base_url(client):
    response = client.get("/")
    assert b"login" in response.data 
    assert response.status_code == 200

def test_login(client):
    aadhar_no="9999"
    password="123"
    response = user_login(client,aadhar_no="9999",password="123")
    print(response)
    assert b'user_home' in response.data

    response = user_login(client, f"{aadhar_no}x", password)
    assert b'Login failed... Enter valid credentials' in response.data

    response = user_login(client, aadhar_no, f'{password}x')
    assert b'Login failed... Enter valid credentials' in response.data

def test_logout(client):
    response = logout(client)
    assert b"Login" in response.data

def test_signup(client):
    response = client.post("/signup",data = dict(
            fname = "tester",
            lname = "tester",
            mobile_no = 4564445552,
            aadhar_no = 8888,
            password = "123",
            birth_year = 2000,
            email = 'tester@gmail.com'))
    
    assert response.status_code == 200


def test_user_home(client):
    user_login(client,aadhar_no="9999",password="123")
    response = client.get("/user_home")
    # title
    assert b'Home -Vaccine' in response.data
    assert response.status_code == 200


def test_center_dashboard(client):
    staff_login(client,staff_id=1,password="123")
    response = client.get("/center_dashboard")
    # title
    assert b'Center Dashboard' in response.data
    assert response.status_code == 200

    logout(client)
    response = client.get("/center_dashboard")
    assert not b'Center Dashboard' in response.data
    assert response.status_code == 302

