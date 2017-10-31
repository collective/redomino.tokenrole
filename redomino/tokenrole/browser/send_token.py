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
from zope.interface import implementer
from zope.schema import TextLine

from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE

from plone import api
from plone.app.z3cform import layout

from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage

from redomino.tokenrole import tokenroleMessageFactory as _
from redomino.tokenrole.browser.interfaces import ITokenSendForm
from redomino.tokenrole.interfaces import ITokenURL
from redomino.tokenrole.interfaces import ITokenInfoSchema


@implementer(ITokenURL)
class TokenURL(object):

    def __init__(self, context):
        self.context = context

    def __call__(self, token_id):
        return '{}?token={}'.format(self.context.absolute_url(), token_id)


class TokenSendForm(form.Form):
    """ A simple feedback form to send a message to the site admin """

    ignoreContext = True

    label = _('label_send_form', default=u'Send token form')
    successMessage = _('data_saved', default='Data successfully updated.')
    noChangesMessage = _('no_changes', default='No changes were applied.')

    # Defining the fields. You can add fields together.
    fields = field.Fields(TextLine(__name__='token_display',
                                   title=ITokenSendForm['token_id'].title,
                                   description=ITokenSendForm['token_id'].description)) + field.Fields(ITokenSendForm)
    fields['token_id'].mode = HIDDEN_MODE
    fields['token_display'].mode = DISPLAY_MODE

    def updateWidgets(self):
        super(TokenSendForm, self).updateWidgets()
        self.widgets['token_display'].value = self.request.get('form.widgets.token_id')
        # for some reasons this is not taken from the request otherwise
        self.widgets['token_id'].value = self.request.get('form.widgets.token_id')

    # Handler for the submit action
    @button.buttonAndHandler(_(u'label_send_token', default=u'Send'), name='send')
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('token_role_send_ko', default=u'An error has occurred')
            return

        # do something usefull, here we send the mail and
        # set the status message
        self.status = self.send_mail(data)
        self.request.response.redirect(self.nextURL())

    @button.buttonAndHandler(_(u'label_cancel', default=u'Cancel'), name='cancel')
    def handle_cancel(self, action):
        self.status = self.noChangesMessage
        self.request.response.redirect(self.nextURL())
        return

    def nextURL(self):
        IStatusMessage(self.request).addStatusMessage(self.status, type='info')
        return "%s/%s" % (self.getContent().absolute_url(), '@@token_manage')

    def send_mail(self, data):
        email_list = data['email_list']
        subject = safe_unicode(data['subject'])
        text = safe_unicode(data['text'])
        token_id = data['token_id']
        url = ITokenURL(self.context)(token_id)
        token_info = ITokenInfoSchema(self.context)
        loc_token_end = api.portal.get_localized_time(token_info.token_end)

        message = text.replace('${date}s', str(loc_token_end))
        message = message.replace('${url}s', url)

        try:
            for recipient in email_list:
                api.portal.send_email(
                    recipient=recipient, subject=subject, body=message)
        except ValueError:
            return _('token_role_send_ko_mail', default=u'Error sending email')

# wrap the form with plone.app.z3cform's Form wrapper
TokenSendFormView = layout.wrap_form(TokenSendForm)
