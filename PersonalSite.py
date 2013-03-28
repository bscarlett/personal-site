from flask import Flask
import configuration
from views import bp


app = Flask(__name__)
app.config.from_object(configuration)
app.register_blueprint(bp)
