import unittest

from mongoengine import connect

from models import Content
from models import NavigationOrder


class testNavigationOrder(unittest.TestCase):
    def setUp(self):
        connect('test')

    def testNavigationOrderPopulate(self):
        Content(route='athing', show_in_navigation=True).save()
        Content(route='bthing', show_in_navigation=True).save()
        Content(route='notathing').save()
        NavigationOrder.populate_from_content()
        assert NavigationOrder.objects(order=0).first().route == 'athing'
        assert NavigationOrder.objects(order=1).first().route == 'bthing'
        assert NavigationOrder.objects(order=2).first() is None

    def testNavigationOrderMoveOverExisting(self):
        NavigationOrder(route='a', order=0).save()
        n = NavigationOrder(route='b', order=1)
        n.save()
        n.move(0)
        assert NavigationOrder.objects(order=0).first().route == 'b'
        assert NavigationOrder.objects(order=1).first().route == 'a'

    def tearDown(self):
        Content.objects.delete()
        NavigationOrder.objects.delete()