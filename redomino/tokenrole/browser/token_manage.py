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

import datetime

from zope.schema import TextLine

from z3c.form.form import applyChanges
from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import INPUT_MODE
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.app.z3cform import layout

from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from redomino.tokenrole import tokenroleMessageFactory as _
from redomino.tokenrole.interfaces import ITokenRolesAnnotate
from redomino.tokenrole.interfaces import ITokenInfoSchema
from redomino.tokenrole.config import DEFAULT_TOKEN_DAYS
from redomino.tokenrole.utils import make_uuid


class TokenManageView(BrowserView):

    def tokens_data(self):
        tr_annotate = ITokenRolesAnnotate(self.context)
        return tr_annotate.token_dict
        
    def token_ids(self):
        tr_annotate = ITokenRolesAnnotate(self.context)
        token_dict = tr_annotate.token_dict
        return token_dict.keys()



class TokenAddForm(form.AddForm):
    """ Token Add Form """

    # Defining the fields
    fields = field.Fields(ITokenInfoSchema)
    fields['token_id'].mode = HIDDEN_MODE
    fields['token_roles'].widgetFactory[INPUT_MODE] = CheckBoxFieldWidget

    label = _(u"heading_add_token", default="TokenRole: Add token")
    formErrorsMessage = _('form_errors', default='There were some errors.')
    noChangesMessage = _('no_changes', default='No changes were applied.')

    def updateWidgets(self):
        super(TokenAddForm, self).updateWidgets()
        self.widgets['token_id'].value = make_uuid(self.getContent().getId())

        end_date = datetime.datetime.now() + datetime.timedelta(DEFAULT_TOKEN_DAYS)
        self.widgets['token_end'].value = (end_date.year, end_date.month, end_date.day, 0, 0)

    def createAndAdd(self, data):
        context = self.getContent()
        applyChanges(self, context, data)
        return context

    def nextURL(self):
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')
        return "%s/%s" % (self.getContent().absolute_url(), '@@token_manage')

    def update(self):
        self.buttons.values()[0].title = _(u'add_token', default=u"Add token")
        super(TokenAddForm, self).update()


# wrap the form with plone.app.z3cform's Form wrapper
TokenAddFormView = layout.wrap_form(TokenAddForm)


class TokenEditForm(form.EditForm):
    """ Token Edit Form """

    # Defining the fields
    fields = field.Fields(TextLine(__name__='token_display',
                                   title=ITokenInfoSchema['token_id'].title,
                                   description=ITokenInfoSchema['token_id'].description)) + field.Fields(ITokenInfoSchema)
    fields['token_id'].mode = HIDDEN_MODE
    fields['token_display'].mode = DISPLAY_MODE
    fields['token_roles'].widgetFactory[INPUT_MODE] = CheckBoxFieldWidget

    label = _(u"heading_edit_token", default="TokenRole: Modify token")
    successMessage = _('data_saved', default='Data successfully updated.')
    noChangesMessage = _('no_changes', default='No changes were applied.')


    def updateWidgets(self):
        super(TokenEditForm, self).updateWidgets()
        self.widgets['token_display'].value = self.request.get('form.widgets.token_id')

    def nextURL(self):
        context = self.getContent()
        data, errors = self.extractData()
        return "%s/@@token_manage" % (context.absolute_url()) 

    @button.buttonAndHandler(_(u'modify_token', default=u"Modify token"), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage

        nextURL = self.nextURL()
        if nextURL:
            IStatusMessage(self.request).addStatusMessage(self.status, type='info')
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u'label_cancel', default=u'Cancel'), name='cancel')
    def handle_cancel(self, action):
        self.status = self.noChangesMessage
        self.request.response.redirect(self.nextURL())
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')
        return


# wrap the form with plone.app.z3cform's Form wrapper
TokenEditFormView = layout.wrap_form(TokenEditForm)


class TokenDeleteForm(form.Form):

    ignoreContext = True

    label = _(u"heading_delete_token", default="TokenRole: Delete token")
    successMessage = _('data_saved', default='Data successfully updated.')
    noChangesMessage = _('no_changes', default='No changes were applied.')
    
    # Defining the fields. You can add fields together.
    fields = field.Fields(TextLine(__name__='token_display',
                                   title=ITokenInfoSchema['token_id'].title,
                                   description=ITokenInfoSchema['token_id'].description)) + field.Fields(ITokenInfoSchema).select(*['token_id'])

    fields['token_id'].mode = HIDDEN_MODE
    fields['token_display'].mode = DISPLAY_MODE

    def updateWidgets(self):
        super(TokenDeleteForm, self).updateWidgets()
        self.widgets['token_display'].value = self.request.get('form.widgets.token_id')

    def nextURL(self):
        context = self.getContent()
        data, errors = self.extractData()
        return "%s/@@token_manage" % (context.absolute_url()) 

    # Handler for the submit action
    @button.buttonAndHandler(_(u'delete_token', default=u'Delete token'), name='delete')
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _(u"delete_error", default="An error has occurred")
            return

        context = self.getContent()
        tr_annotate = ITokenRolesAnnotate(context)
        if tr_annotate.token_dict.has_key(data['token_id']):
            del tr_annotate.token_dict[data['token_id']]

        self.status = _(u'delete_success', default=u"Token removed")
        self.request.response.redirect("%s/@@token_manage" % self.nextURL())
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')

    @button.buttonAndHandler(_(u'label_cancel', default=u'Cancel'), name='cancel')
    def handle_cancel(self, action):
        self.status = self.noChangesMessage
        self.request.response.redirect(self.nextURL())
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')


TokenDeleteFormView = layout.wrap_form(TokenDeleteForm)

