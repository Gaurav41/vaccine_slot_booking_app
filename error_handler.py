import werkzeug
from flask import render_template
from app import app
@app.errorhandler(404)
def not_found(e):
    print(e)
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "err_msg":"May be you entered wrong url or resource may be deleted"
    }
    return render_template("error.html",response=response),404

@app.errorhandler(401)
def unauthorised(e):
    print(e)
    return render_template("login.html"),401

@app.errorhandler(403)
def forbidden(e):
    print(e)
    return render_template("login.html"),403

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "err_msg":"bad request!"
    }
    return render_template("error.html",response=response),400

    # return 'bad request!', 400

from werkzeug.exceptions import HTTPException, abort

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response