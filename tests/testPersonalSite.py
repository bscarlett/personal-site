__author__ = 'bradleyscarlett'
import unittest
import PersonalSite
from lxml import etree


class testPersonalSite(unittest.TestCase):
    def setUp(self):
        db = 'test'
        PersonalSite.app.config['DATABASE'] = db
        self.app = PersonalSite.app.test_client()
        self.db = PersonalSite.get_db(db)

    def testIndexRoute(self):
        content = self.db.Content()
        content._id = u'/'
        content.title = u'Test Title'
        content.description = u'Test Description'
        content.content = u'Test Content'
        content.show_in_navigation = True
        content.save()

        rsp = self.app.get('/')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find('./head/title').text == 'Test Title'
        assert e.find(".//div[@id='content']/p").text == 'Test Content'
        assert e.find(".//ul[@id='navigation']//a[@href='/']").text == 'Test Title'

    def testOtherRoute(self):
        content = self.db.Content()
        content._id = u'other'
        content.content = u'other content'
        content.save()

        rsp = self.app.get('/other')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find(".//div[@id='content']/p").text == 'other content'

    def test404(self):
        content = self.db.Content()
        self._id = u'there_is_a_route_for_this'
        content.save()

        rsp = self.app.get('/there_is_no_route_for_this')
        assert rsp.status_code == 404

    def testContentIsMarkdown(self):
        content = self.db.Content()
        content._id = u'route'
        content.content = u'#should be a heading 1#'
        content.save()

        rsp = self.app.get('/route')
        assert rsp.status_code == 200

        e = etree.HTML(rsp.data)
        assert e.find(".//div[@id='content']/h1").text == 'should be a heading 1'

    def testBrowsing(self):
        content1 = self.db.Content()
        content1._id = u'/'
        content1.title = u'home'
        content1.content = u'thing'
        content1.show_in_navigation = True
        content1.save()

        content2 = self.db.Content()
        content2._id = u'thing'
        content2.title = u'thing'
        content2.title = u'thing2'
        content2.show_in_navigation = True
        content2.save()

        rsp = self.app.get('/')
        assert rsp.status_code == 200
        #to be continued..

    def tearDown(self):
        self.db.Content.delete()
