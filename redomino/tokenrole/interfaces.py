# -*- coding: utf8 -*-
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


from zope.interface import Interface, Attribute
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.schema import TextLine
from zope.schema import Datetime
from zope.schema import Choice
from zope.schema import List

from redomino.tokenrole import tokenroleMessageFactory as _

class ITokenRolesProviding(IAttributeAnnotatable):
    """Mark objects able to dispatch 'token' roles, and therefor annotatable
    """
    
class ITokenInfoSchema(Interface):
    """info used to manage the token
    """

    token_id = TextLine(
                    title=_(u'label_token_value', default=u'Token Value'),
                    description=_(u'help_token_value', default=u'Value to assign to token'),
                    required=True)
    
    token_end = Datetime(
                    title=_(u'label_token_validity', default=u'Token Validity End'),
                    description=_(u'help_token_validity', default=u'End date to assign to token'),
                    required=True)

    token_roles= List(title=_(u'label_roles', default=u'Roles'),
                      description=_(u'help_roles', default=u'Roles to assing'),
                      required=True,
                      default=['Reader'],
                      value_type=Choice(vocabulary='redomino.tokenrole.Roles',)
                     )


class ITokenRolesAnnotate(Interface):
    """Provide access to annotated token roles infos token role dispatching.
    """
    
    token_dict = Attribute("dictionary with infos about tokens")


