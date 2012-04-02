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

import unittest2 as unittest
from redomino.tokenrole.testing import REDOMINO_TOKENROLE_INTEGRATION_TESTING

class TestPortal(unittest.TestCase):
    """ Maps settings """
    layer = REDOMINO_TOKENROLE_INTEGRATION_TESTING

    def test_installed(self):
        portal = self.layer['portal']
        self.assertTrue(portal.portal_quickinstaller.isProductInstalled('redomino.tokenrole'))

    def test_acl_users(self):
        """ plugin in acl_users? """
        from redomino.tokenrole.config import PLUGINID
        portal = self.layer['portal']
        acl_users = portal.acl_users
        self.assertTrue(PLUGINID in acl_users.objectIds())

