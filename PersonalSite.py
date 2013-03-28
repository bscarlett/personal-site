from argparse import ArgumentParser

from flask import Flask, render_template, abort
from markdown import markdown
from mongoengine import connect
from mongoengine import Document
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import IntField


app = Flask(__name__)
DATABASE = 'personal_site'
DEBUG = True

app.config.from_object(__name__)


class Content(Document):
    route = StringField(primary_key=True)
    show_in_navigation = BooleanField(default=False)
    title = StringField()
    content = StringField()
    short_description = StringField()

    @staticmethod
    def get_navigables():
        return Content.objects(show_in_navigation=True).order_by('route')


class NavigationOrder(Document):
    route = StringField(unique=True)
    order = IntField(unique=True)

    @staticmethod
    def populate_from_content():
        for i, c in enumerate(Content.get_navigables()):
            NavigationOrder(route=c.route, order=i).save()

    def move(self, order):
        current_order = self.order
        existing_target = NavigationOrder.objects(order=order).first()
        if existing_target is not None:
            existing_target.move(-1)  # Can't guarantee that -1 doesn't have a thing in it, so possible fail here
            self.order = order
            self.save()
            existing_target.move(current_order)
        else:
            self.order = order
            self.save()


@app.before_request
def before_request():
    connect(app.config['DATABASE'])


@app.route('/<route>')
def view(route):
    content = Content.objects(route=route).first()
    if content is None:
        abort(404)
    return render_template('content.html',
                           title=content.title,
                           description=content.short_description,
                           body=markdown(content.content),
                           navigables=Content.get_navigables())


@app.route('/')
def index():
    return view('/')


def load_from_file(route, title, short_description, content_filename, show_in_navigation, **kwargs):
    connect(app.config['DATABASE'])
    content = Content()
    content.route = route
    content.title = title
    content.short_description = short_description
    content.show_in_navigation = show_in_navigation

    with open(content_filename) as content_file:
        content.content = '\n'.join(content_file.readlines())

    content.save()


def serve(**kwargs):
    app.run()


def parse_arguments():
    argument_parser = ArgumentParser()
    subparsers = argument_parser.add_subparsers()
    serve_argument_parser = subparsers.add_parser('serve')
    serve_argument_parser.set_defaults(function=serve)
    load_argument_parser = subparsers.add_parser('load')
    load_argument_parser.add_argument('--content-filename')
    load_argument_parser.add_argument('--title')
    load_argument_parser.add_argument('--route')
    load_argument_parser.add_argument('--show-in-navigation', action='store_true', default=False)
    load_argument_parser.add_argument('--short-description')
    load_argument_parser.set_defaults(function=load_from_file)

    return argument_parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    arguments.function(**vars(arguments))
