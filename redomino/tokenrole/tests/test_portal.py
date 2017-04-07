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

import unittest
from redomino.tokenrole.testing import REDOMINO_TOKENROLE_INTEGRATION_TESTING
from redomino.tokenrole.interfaces import ITokenURL
from redomino.tokenrole.validators import isEmail


class TestPortal(unittest.TestCase):
    """ Maps settings """
    layer = REDOMINO_TOKENROLE_INTEGRATION_TESTING


    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('redomino.tokenrole'))

    def test_acl_users(self):
        """ plugin in acl_users? """
        from redomino.tokenrole.config import PLUGINID
        acl_users = self.portal.acl_users
        self.assertTrue(PLUGINID in acl_users.objectIds())

    def test_portal_actions(self):
        """ Portal actions loaded? """
        self.assertIn('manage_tokenrole', self.portal.portal_actions.object)

    def test_validator_valid_email(self):
        self.assertTrue(isEmail('info@example.org'))

    def test_validator_valid_email(self):
        self.assertFalse(isEmail('info'))

    def test_tokenurl_adapter(self):
        self.assertEqual(
            ITokenURL(self.portal)('secret-id'),
            self.portal.absolute_url() + '?token=secret-id'
        )

# EOF
