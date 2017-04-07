# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin

from redomino.tokenrole.config import PROJECTNAME
from redomino.tokenrole.plugins import tokenrole


registerMultiPlugin(tokenrole.TokenRole.meta_type)
tokenroleMessageFactory = MessageFactory(PROJECTNAME)


def initialize(context):
    context.registerClass(tokenrole.TokenRole,
                          permission=add_user_folders,
                          constructors=(tokenrole.manage_addTokenRoleForm,
                                        tokenrole.addTokenRole),
                          visibility=None)
