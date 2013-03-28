from mongoengine import Document, StringField, BooleanField


class Content(Document):
    route = StringField(primary_key=True)
    show_in_navigation = BooleanField(default=False)
    title = StringField()
    content = StringField()
    short_description = StringField()

    @staticmethod
    def get_navigables():
        return Content.objects(show_in_navigation=True).order_by('route')