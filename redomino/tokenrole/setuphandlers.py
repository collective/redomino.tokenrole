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

from six import StringIO

from Products.CMFCore.utils import getToolByName

try:
    # Plone 5.x
    from Products.PlonePAS.setuphandlers import activatePluginInterfaces
except ImportError:
    # Plone 4.3
    from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from redomino.tokenrole.config import PROJECTNAME
from redomino.tokenrole.config import PLUGINID
from redomino.tokenrole.plugins.tokenrole import addTokenRole


class SetupVarious:

    def __call__(self, context):

        # Ordinarily, GenericSetup handlers check for the existence of XML files.
        # Here, we are not parsing an XML file, but we use this text file as a
        # flag to check that we actually meant for this import step to be run.
        # The file is found in profiles/default.

        if context.readDataFile('%s_various.txt' % PROJECTNAME) is None:
            return

        # Add additional setup code here
        site = context.getSite()
        out = StringIO()

        self.setup_plugin(site, out)

        return out.getvalue()

    def setup_plugin(self, portal, out):
        """ Create the virtual anonymous group """
        uf = getToolByName(portal, 'acl_users')

        existing = uf.objectIds()

        if PLUGINID not in existing:
            addTokenRole(uf, PLUGINID)
            activatePluginInterfaces(portal, PLUGINID, out)
        else:
            print >> out, "%s already installed" % PLUGINID


def setupVarious(context):
    """ setup various step. Handles for steps not handled by a gs profile """
    handler = SetupVarious()
    handler(context)
