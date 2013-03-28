from mongoengine import connect
import configuration
from models import Content
from models import NavigationOrder


def load_from_file(route, title, short_description, content_filename, show_in_navigation, **kwargs):
    connect(configuration.DATABASE)
    content = Content()
    content.route = route
    content.title = title
    content.short_description = short_description
    content.show_in_navigation = show_in_navigation
    if show_in_navigation and (NavigationOrder.objects(route=route).first() is None):
        NavigationOrder.add(route=route)

    with open(content_filename) as content_file:
        content.content = '\n'.join(content_file.readlines())

    content.save()