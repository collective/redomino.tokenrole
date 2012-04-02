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

from zope import interface
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
from redomino.tokenrole.interfaces import ITokenRolesProviding
from redomino.tokenrole.interfaces import ITokenRolesAnnotate
from redomino.tokenrole.interfaces import ITokenInfoSchema
from redomino.tokenrole.interfaces import ITokenRoleSupport
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
        return "%s/@@token_edit?form.widgets.token_id=%s" % (context.absolute_url(), data['token_id']) 

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
                                   description=ITokenInfoSchema['token_id'].description)) + field.Fields(ITokenInfoSchema)

    fields['token_id'].mode = HIDDEN_MODE
    fields['token_display'].mode = DISPLAY_MODE
    fields['token_roles'].mode = DISPLAY_MODE
    fields['token_end'].mode = DISPLAY_MODE

    def updateWidgets(self):
        super(TokenDeleteForm, self).updateWidgets()
        self.widgets['token_display'].value = self.request.get('form.widgets.token_id')

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
        self.request.response.redirect("%s/@@token_manage" % self.context.absolute_url())
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')


TokenDeleteFormView = layout.wrap_form(TokenDeleteForm)


class TokenRoleSupport(BrowserView):
    
    interface.implements(ITokenRoleSupport)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    @property
    def tokenrole_enabled(self):
        """return if token role is enabled on the context.
        """
        return ITokenRolesProviding.providedBy(self.context)
        
    def enable_tokenrole(self):
        """enable token role management on context
        """
        if not self.tokenrole_enabled:
            interface.alsoProvides(self.context, (ITokenRolesProviding,))
            IStatusMessage(self.request).addStatusMessage(_("token_enabled", default="Token Role enabled"))
            url = "%s/@@token_manage" % self.context.absolute_url()
            self.request.response.redirect(url)

    def disable_tokenrole(self):
        """disable token role mnagement on context
        """
        if self.tokenrole_enabled:
            provided = interface.directlyProvidedBy(self.context)
            interface.directlyProvides(self.context, provided - ITokenRolesProviding)
            IStatusMessage(self.request).addStatusMessage(_("token_disabled", default="Token Role disabled"))
            url = "%s/view" % self.context.absolute_url()
            self.request.response.redirect(url)
            




