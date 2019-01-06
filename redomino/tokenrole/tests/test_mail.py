# -*- coding: utf-8 -*-
# Copyright (c) 2010 Redomino srl (http://redomino.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from email import message_from_string
from datetime import datetime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from redomino.tokenrole.testing import REDOMINO_TOKENROLE_INTEGRATION_TESTING
from redomino.tokenrole.interfaces import ITokenInfoSchema
from redomino.tokenrole.browser.send_token import TokenSendForm
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager

import unittest


class TestMailing(unittest.TestCase):
    """ Test mailing """
    layer = REDOMINO_TOKENROLE_INTEGRATION_TESTING


    def setUp(self):
        self.portal = self.layer['portal']
        mails = self.portal.MailHost = MockMailHost('MailHost')
        # configure mailhost
        mails.smtp_host = 'localhost'
        mails.smtp_port = '25'
        if api.env.plone_version() < '5.0':
            mails.email_from_name = u'Portal Owner'
            mails.email_from_address = 'sender@example.org'
        else:
            api.portal.set_registry_record(
                'plone.email_from_name', u'Portal Owner', )
            api.portal.set_registry_record(
                  'plone.email_from_address', 'sender@example.org', )
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mails, IMailHost)
        self.mailhost = api.portal.get_tool('MailHost')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.doc = api.content.create(self.portal, 'Document', id='test-doc')
        self.token = ITokenInfoSchema(self.doc)
        self.token.token_id = '0815'
        self.token.token_end = datetime(2018, 1, 30, 12, 45)

    def test_memberemail(self):
        user = api.user.create(email='foo@example.com', username='foo')
        login(self.portal, 'foo')
        #user = api.user.get(userid=TEST_USER_ID)
        #user.setMemberProperties(mapping={'email': 'foo@example.com', })
        form = TokenSendForm(self.doc, self.layer['request'])
        data = {'email_list': ['bar@example.org'],
                'subject': 'Token send',
                'text': 'Token bla bla ${date}s  ${url}s ',
                'token_id': '0815'}
        self.mailhost.reset()
        form.send_mail(data)
        msg = message_from_string(self.mailhost.messages[0])
        self.assertEqual(msg['To'], 'bar@example.org')
        self.assertEqual(msg['From'], 'foo@example.com')
        self.assertEqual(msg['Subject'], '=?utf-8?q?Token_send?=')
        self.assertIn(
                'Token bla bla Jan 30, 2018  http://nohost/plone/test-doc?token=3D0815=20',
                msg.get_payload())


# EOF
