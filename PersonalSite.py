from flask import Flask, render_template, abort, g
from markdown import markdown
from mongokit import Connection, Document
from argparse import ArgumentParser

app = Flask(__name__)
DATABASE = 'personal_site'
DEBUG = True

app.config.from_object(__name__)


class Content(Document):
    __collection__ = 'content'
    use_dot_notation = True
    structure = {
        '_id': unicode,
        'title': unicode,
        'short_description': unicode,
        'content': unicode,
        'show_in_navigation': bool}


def get_db(db):
    connection = Connection()
    connection.register([Content])
    return connection[db]


def get_navigables(db):
    return db.Content.find({'show_in_navigation': True}, {'title': 1})


@app.before_request
def before_request():
    g.db = get_db(app.config['DATABASE'])


@app.route('/<route>')
def view(route):
    content = g.db.Content.one({'_id': route})
    if content is None:
        abort(404)
    return render_template('content.html',
                           title=content.title,
                           description=content.short_description,
                           body=markdown(content.content),
                           navigables=get_navigables(g.db))


@app.route('/')
def index():
    return view('/')


def load_from_file(route, title, short_description, content_filename, show_in_navigation, **kwargs):
    content = get_db(app.config['DATABASE']).Content()
    content._id = unicode(route)
    content.title = unicode(title)
    content.short_description = unicode(short_description)
    content.show_in_navigation = show_in_navigation

    with open(content_filename) as content_file:
        content.content = unicode('\n'.join(content_file.readlines()))

    content.save()


def serve(**kwargs):
    app.run()
    g.db = get_db(app.config['DATABASE'])


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
