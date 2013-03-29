from mongoengine import Document
from mongoengine import StringField
from mongoengine import BooleanField


class Content(Document):
    route = StringField(primary_key=True)
    show_in_navigation = BooleanField(default=False)
    title = StringField()
    content = StringField()
    short_description = StringField()

    @classmethod
    def get_navigables(cls):
        return cls.objects(show_in_navigation=True).order_by('route')

