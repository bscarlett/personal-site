import unittest

from mongoengine import connect
from nose.tools import eq_, raises

from PersonalSite.console import navigation_move, InvalidCommand
from PersonalSite.models import NavigationOrder, Content


class test_navigation_move(unittest.TestCase):
    def setUp(self):
        connect('test')

    def test_navigation_move(self):
        Content(route='a', show_in_navigation=True).save()
        NavigationOrder(route='a', order=0).save()
        navigation_move('a', 1)

        eq_(NavigationOrder.objects(route='a').first().order, 1)

    @raises(InvalidCommand)
    def test_no_content(self):
        NavigationOrder(route='a', order=0).save()
        navigation_move('a', 1)

    @raises(InvalidCommand)
    def test_invisible_content(self):
        Content(route='a', show_in_navigation=False).save()
        NavigationOrder(route='a', order='0').save()
        navigation_move('a', 1)

    def test_no_nav_order(self):
        Content(route='a', show_in_navigation=True).save()
        navigation_move('a', 1)

        eq_(NavigationOrder.objects(route='a').first().order, 1)

    def tearDown(self):
        Content.objects.delete()
        NavigationOrder.objects.delete()