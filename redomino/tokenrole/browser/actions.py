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

import zope

from z3c.form import button
from z3c.form.interfaces import IAddForm

from redomino.tokenrole.interfaces import ITokenRolesProviding
from redomino.tokenrole import tokenroleMessageFactory as _


class CancelActions(button.ButtonActions):
    zope.component.adapts(
        IAddForm,
        zope.interface.Interface,
        ITokenRolesProviding)

    def update(self):
        self.form.buttons = button.Buttons(
            self.form.buttons,
            button.Button('cancel', _(u'Cancel')))
        super(CancelActions, self).update()


class AddActionHandler(button.ButtonActionHandler):

    zope.component.adapts(
        IAddForm,
        zope.interface.Interface,
        ITokenRolesProviding,
        button.ButtonAction)

    def __call__(self):
        if self.action.name == 'form.buttons.cancel':
            self.form._finishedAdd = True
            self.form.status = self.form.noChangesMessage
            return
        super(AddActionHandler, self).__call__()
