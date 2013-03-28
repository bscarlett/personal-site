__author__ = 'bradleyscarlett'
import unittest

from lxml import etree
from mongoengine import connect

import PersonalSite
from PersonalSite import Content
from PersonalSite import NavigationOrder


class testPersonalSite(unittest.TestCase):
    def setUp(self):
        db = 'test'
        PersonalSite.app.config['DATABASE'] = db
        self.app = PersonalSite.app.test_client()
        connect(db)

    def testIndexRoute(self):
        content = Content()
        content.route = '/'
        content.title = 'Test Title'
        content.short_description = 'Test Description'
        content.content = 'Test Content'
        content.show_in_navigation = True
        content.save()

        rsp = self.app.get('/')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find('./head/title').text == 'Test Title'
        assert e.find(".//div[@id='content']/p").text == 'Test Content'
        assert e.find(".//ul[@id='navigation']//a[@href='/']").text == 'Test Title'

    def testOtherRoute(self):
        content = Content()
        content.route = 'other'
        content.content = 'other content'
        content.save()

        rsp = self.app.get('/other')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find(".//div[@id='content']/p").text == 'other content'

    def test404(self):
        content = Content()
        content.route = 'there_is_a_route_for_this'
        content.save()

        rsp = self.app.get('/there_is_no_route_for_this')
        assert rsp.status_code == 404

    def testContentIsMarkdown(self):
        content = Content()
        content.route = 'route'
        content.content = '#should be a heading 1#'
        content.save()

        rsp = self.app.get('/route')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find(".//div[@id='content']/h1").text == 'should be a heading 1'

    def testMultipleHits(self):
        content1 = Content()
        content1.route = '/'
        content1.title = 'home'
        content1.content = 'thing'
        content1.show_in_navigation = True
        content1.save()

        content2 = Content()
        content2.route = 'thing'
        content2.title = 'thing'
        content2.content = 'thing2'
        content2.show_in_navigation = True
        content2.save()

        response_1 = self.app.get('/')
        assert response_1.status_code == 200

        response_2 = self.app.get('thing')
        assert response_2.status_code == 200

    def testLiveUpdate(self):
        content1 = Content()
        content1.route = '/'
        content1.title = 'home'
        content1.content = 'thing'
        content1.show_in_navigation = True
        content1.save()

        response_1 = self.app.get('/')
        assert response_1.status_code == 200

        content2 = Content()
        content2.route = 'thing'
        content2.title = 'thing'
        content2.content = 'thing2'
        content2.show_in_navigation = True
        content2.save()

        response_2 = self.app.get('thing')
        assert response_2.status_code == 200

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