import unittest

from mongoengine import connect
from nose.tools import eq_
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

        eq_(NavigationOrder.objects(order=0).first().route, 'athing')
        eq_(NavigationOrder.objects(order=1).first().route, 'bthing')
        eq_(NavigationOrder.objects(order=2).first(), None)

    def testNavigationOrderMoveOverExisting(self):
        NavigationOrder(route='a', order=0).save()
        n = NavigationOrder(route='b', order=1)
        n.save()
        n.move(0)

        eq_(NavigationOrder.objects(order=0).first().route, 'b')
        eq_(NavigationOrder.objects(order=1).first().route, 'a')

    def testMoveOverSelf(self):
        n = NavigationOrder(route='a', order=0)
        n.save()
        n.move(0)

        eq_(NavigationOrder.objects(order=0).first().route, 'a')

    def testAdd(self):
        NavigationOrder(route='a', order=10).save()
        NavigationOrder.add('b')
        eq_(NavigationOrder.objects(route='b').first().order, 11)

    def testAddToEmpty(self):
        NavigationOrder.add('a')
        eq_(NavigationOrder.objects(route='a').first().order, 0)

    def tearDown(self):
        Content.objects.delete()
        NavigationOrder.objects.delete()