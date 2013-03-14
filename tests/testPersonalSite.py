__author__ = 'bradleyscarlett'
import unittest
import PersonalSite
from lxml import etree


class testPersonalSite(unittest.TestCase):
    def setUp(self):
        testdb = 'testdb'
        PersonalSite.app.config['DATABASE'] = testdb
        self.app = PersonalSite.app.test_client()
        self.db = PersonalSite.get_db(testdb)

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
        assert e.find(".//ul[@id='navigation']//a[@href='//']").text == 'Test Title'

    def tearDown(self):
        self.db.Content.delete()
