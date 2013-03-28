from models import Content


def navigation_move(route, order, **kwargs):
    if Content.objects(route=route).first() is not None:
        pass
    else:
        raise Exception("route '{0}' does not exist in content collection".format(route))