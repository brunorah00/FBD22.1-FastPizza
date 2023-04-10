from flask import Flask

from model.Borda.controller_borda import app_borda

app = Flask(__name__)

app.register_blueprint(app_borda)

app.run()