# coding=utf-8
# Copyright (c) 2011 Redomino srl (http://redomino.com)
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

from plone.app.testing import PloneSandboxLayer 
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from zope.configuration import xmlconfig

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

class RedominoPolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import redomino.tokenrole
        xmlconfig.file('configure.zcml',
                       redomino.tokenrole,
                       context=configurationContext
                      )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redomino.tokenrole:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # do something here!

        setRoles(portal, TEST_USER_ID, ['Member'])


REDOMINO_TOKENROLE_FIXTURE = RedominoPolicy()
REDOMINO_TOKENROLE_INTEGRATION_TESTING = IntegrationTesting(
                  bases=(REDOMINO_TOKENROLE_FIXTURE,), 
                  name="RedominoTokenrole:Integration")
REDOMINO_TOKENROLE_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(REDOMINO_TOKENROLE_FIXTURE,), name="RedominoTokenrole:Functional")

