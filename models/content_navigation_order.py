from models import Content
from models import NavigationOrder


class ContentNavigationOrder(object):
    """Cross model functions between Content and NavigationOrder"""

    @staticmethod
    def get_navigables_in_order():
        return [Content.objects(route=r).first() for r in NavigationOrder.get_routes_in_order()]

    @staticmethod
    def populate_from_content():
        for i, c in enumerate(Content.get_navigables()):
            NavigationOrder(route=c.route, order=i).save()