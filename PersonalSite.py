from flask import Flask, render_template
from markdown import markdown
from mongokit import Connection, Document
from argparse import ArgumentParser


class Content(Document):

    use_dot_notation = True
    structure = {
        '_id': unicode,
        'route': unicode,
        'title': unicode,
        'short_description': unicode,
        'content': unicode,
        'show_in_navigation': bool}


app = Flask(__name__)
connection = Connection()
connection.register([Content])
collection = connection['test'].content


def make_route(route, title, short_description, content, show_in_navigation):
    @app.route(route)
    def route_function():
        return render_template('content.html', title=title, description=short_description, body=markdown(content))
    return route_function


for content in collection.Content.find():
    exec "{0} = make_route(content.route, content.title, content.short_description, content.content, content.show_in_navigation)".format(content.title)


def load_from_file(route, title, short_description, content_filename, show_in_navigation, **kwargs):
    content = collection.Content()
    content.route = unicode(route)
    content.title = unicode(title)
    content._id = u':'.join((content.title, content.route))
    content.short_description = unicode(short_description)
    content.show_in_navigation = show_in_navigation

    with open(content_filename) as content_file:
        content.content = unicode('\n'.join(content_file.readlines()))

    content.save()


def serve(**kwargs):
    app.debug = True
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

    print argument_parser.parse_args()
    print vars(argument_parser.parse_args())

    return argument_parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    arguments.function(**vars(arguments))
