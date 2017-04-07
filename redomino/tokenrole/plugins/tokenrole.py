# -*- coding: utf-8 -*-
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

from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin


manage_addTokenRoleForm = PageTemplateFile(
    'www/tokenRoleAdd', globals(), __name__='manage_addTokenRoleForm')


def addTokenRole(dispatcher, id, title=None, REQUEST=None):
    """ Add an TokenRole plugin to a Pluggable Auth Service. """
    sp = TokenRole(id, title)
    dispatcher._setObject(sp.getId(), sp)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
                                     '?manage_tabs_message='
                                     'TokenRole+added.'
                                     % dispatcher.absolute_url())


class TokenRole(BasePlugin):
    """ Multi-plugin for assigning auto roles from IP. """

    meta_type = 'TokenRole'
    security = ClassSecurityInfo()

    _properties = (
        dict(id='title', label='Title', type='string', mode='w'),
    )

    manage_options = BasePlugin.manage_options[:1]

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    #
    # IExtractionPlugin
    #
    security.declarePrivate('extractCredentials')

    def extractCredentials(self, request):
        # Avoid creating anon user if this is a regular user
        # We actually have to poke request ourselves to avoid users from
        # root becoming anonymous...
        if getattr(request, 'token', None):
            set_anon_user = True
            if getattr(request, '_auth', None):
                set_anon_user = False
            else:
                try:
                    credentials_cookie_auth = self.aq_parent.plugins.credentials_cookie_auth
                    cookie_auth = credentials_cookie_auth.extractCredentials(request)
                    if cookie_auth:
                        set_anon_user = False
                except:
                    pass

            return dict(TokenRole=True, SetAnonymousUser=set_anon_user)

        return {}

    #
    # IAuthenticationPlugin
    #
    security.declarePrivate('authenticateCredentials')

    def authenticateCredentials(self, credentials):
        if credentials.get('login'):
            return None
        tokenrole = credentials.get('TokenRole', None)
        if not tokenrole:
            return None
        if credentials.get('SetAnonymousUser', None):
            return ('Anonymous User', 'Anonymous User')

        return None


classImplements(TokenRole, IExtractionPlugin, IAuthenticationPlugin)
InitializeClass(TokenRole)
