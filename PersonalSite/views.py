from flask import abort, render_template, Blueprint, current_app
from markdown import markdown
from mongoengine import connect

from PersonalSite.models import Content
from PersonalSite.models import ContentNavigationOrder

bp = Blueprint('views', __name__)


@bp.before_request
def before_request():
    connect(current_app.config['DATABASE'])


@bp.route('/<route>')
def view(route):
    content = Content.objects(route=route).first()
    if content is None:
        abort(404)
    return render_template('content.html',
                           title=content.title,
                           description=content.short_description,
                           body=markdown(content.content),
                           navigables=ContentNavigationOrder.get_navigables_in_order())


@bp.route('/')
def index():
    return view('/')