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

from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redomino.tokenrole.testing import REDOMINO_TOKENROLE_INTEGRATION_TESTING
from redomino.tokenrole.tokenroleprovider import TokenRolesLocalRolesProviderAdapter

import unittest


class TestToken(unittest.TestCase):
    """ Test token """

    layer = REDOMINO_TOKENROLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.doc = api.content.create(self.portal, 'Document', id='test-doc')

    def test_TokenRolesLocalRolesProviderAdapter_getRoles(self):
        api.user.create(email='foo@example.com', username='foo')
        adapter = TokenRolesLocalRolesProviderAdapter(self.doc)
        self.assertEqual(adapter.getRoles('foo'), ())

    def test_TokenRolesLocalRolesProviderAdapter_getAllRoles(self):
        adapter = TokenRolesLocalRolesProviderAdapter(self.doc)
        self.assertEqual(adapter.getAllRoles(), ())


# EOF
