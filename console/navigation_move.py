from models import Content
from models import NavigationOrder
from console.InvalidCommand import InvalidCommand


def navigation_move(route, order, **kwargs):
    if Content.objects(route=route).first() is None:
        raise InvalidCommand("route '{0}' does not exist in content collection".format(route))
    if Content.objects(route=route, show_in_navigation=True).first() is None:
        raise InvalidCommand("route '{0}' is not visible in navigation".format(route))
    nav_order = NavigationOrder.objects(route=route).first()
    if nav_order is None:  # This probably shouldn't happen.
        nav_order = NavigationOrder.add(route=route)
    nav_order.move(order)