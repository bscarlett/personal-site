from flask import Flask
import configuration
from views import bp
from console import parse_arguments


app = Flask(__name__)
app.config.from_object(configuration)
app.register_blueprint(bp)


def main():
    arguments = parse_arguments()
    arguments.function(**vars(arguments))