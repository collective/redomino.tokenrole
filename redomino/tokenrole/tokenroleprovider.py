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

from apply import apply
from borg.localrole.interfaces import ILocalRoleProvider
from datetime import datetime
from DateTime import DateTime
from persistent.dict import PersistentDict
from redomino.tokenrole.interfaces import ITokenRolesAnnotate
from redomino.tokenrole.interfaces import ITokenInfoSchema
from redomino.tokenrole.interfaces import ITokenRolesProviding
from six.moves import urllib
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer

try:  # pragma: no cover
    from plone.protect.utils import safeWrite
except ImportError:  # pragma: no cover
    def safeWrite(context, request=None):
        return


ANNOTATIONS_KEY = 'redomino.tokenrole.tokenrole_annotations'


@implementer(ITokenRolesAnnotate)
class TokenRolesAnnotateAdapter(object):

    def __init__(self, context):
        self.annotations = IAnnotations(context).setdefault(ANNOTATIONS_KEY,
                                                            PersistentDict())
        safeWrite(context)

    @apply
    def token_dict():
        def get(self):
            return self.annotations.get('token_dict', {})
        def set(self, value):
            self.annotations['token_dict'] = value
        return property(get, set)


@implementer(ITokenInfoSchema)
@adapter(ITokenRolesProviding)
class TokenInfoSchema(object):

    def __init__(self, context):
        self.context = context
        self.annotation = ITokenRolesAnnotate(self.context)

    def setter(self, name, value):
        if not self.annotation.token_dict:
            self.annotation.token_dict = PersistentDict()
        token_id = self.annotation.token_dict.setdefault(self.token_id, PersistentDict())
        token_id[name] = value

    @apply
    def token_id():
        def getter(self):
            return self.context.REQUEST.get('form.widgets.token_id')

        def setter(self, value):
            pass
        return property(getter, setter)

    @apply
    def token_end():
        def getter(self):
            return self.annotation.token_dict.get(self.token_id, {}).get('token_end')

        def setter(self, value):
            self.setter('token_end', value)
        return property(getter, setter)

    @apply
    def token_roles():
        def getter(self):
            return self.annotation.token_dict.get(self.token_id, {}).get('token_roles')

        def setter(self, value):
            self.setter('token_roles', value)
        return property(getter, setter)


@implementer(ILocalRoleProvider)
class TokenRolesLocalRolesProviderAdapter(object):

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal_id):
        """Returns the roles for the given principal in context"""
        request = getRequest()
        response = request.RESPONSE

        token = request.get('token', None)
        if not token:
            token = request.cookies.get('token', None)

        tr_annotate = ITokenRolesAnnotate(self.context, None)
        safeWrite(tr_annotate)
        if tr_annotate and token in tr_annotate.token_dict:
            expire_date = tr_annotate.token_dict[token].get('token_end')
            roles_to_assign = tr_annotate.token_dict[token].get('token_roles', ('Reader', ))
            if expire_date.replace(tzinfo=None) > datetime.now():
                if token not in request.cookies:
                    physical_path = self.context.getPhysicalPath()
                    url_path = urllib.quote('/' + '/'.join(request.physicalPathToVirtualPath(physical_path)))
                    response.setCookie(name='token',
                                       value=token,
                                       expires=DateTime(expire_date).toZone('GMT').rfc822(),
                                       path=url_path)
                return roles_to_assign
        return ()

    def getAllRoles(self):
        """Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])"""
        return ()
