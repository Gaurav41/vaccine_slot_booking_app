from flask import Flask
from models import db,ma
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

import auth
import routes


if __name__ == "__main__":
    app.run(debug=True)