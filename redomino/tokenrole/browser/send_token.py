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


from smtplib import SMTPException

from zope.schema import TextLine
from zope.component import getMultiAdapter

from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE

from plone.app.z3cform import layout

from Products.MailHost.MailHost import MailHostError
from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from redomino.tokenrole import tokenroleMessageFactory as _
from redomino.tokenrole.browser.interfaces import ITokenSendForm
from redomino.tokenrole.interfaces import ITokenRolesAnnotate


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

    # Handler for the submit action
    @button.buttonAndHandler(_(u'label_send_token', default=u'Send'), name='send')
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('token_role_send_ko', default=u'An error has occurred')
            return

        #do something usefull, here we send the mail and
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
        # Collect mail settings
        context = self.getContent()
        message = _('token_message_text', default="""${text}s<br/>Date: ${date}s<br/>Url: <a href="${url}s">Access<a/> """)
        message = context.utranslate(message)
        portal = getMultiAdapter((context, self.request), name="plone_portal_state").portal()
        mailhost = getToolByName(context, 'MailHost')

        email_list = data['email_list']
        subject = safe_unicode(data['subject'])
        text = safe_unicode(data['text'])
        token_id = data['token_id']
        url = "%s?token=%s" % (context.absolute_url(), token_id)

        email_charset = portal.getProperty('email_charset')
        from_address = portal.getProperty('email_from_address')
        
        tr_annotate = ITokenRolesAnnotate(context)
        end_date = context.toLocalizedTime(tr_annotate.token_dict[token_id]['token_end'])


        message = message.replace('${text}s', text)
        message = message.replace('${date}s', str(end_date))
        message = message.replace('${url}s', url)

        try:
            for email_recipient in email_list:
                mailhost.secureSend(message, email_recipient, from_address,
                                    subject=subject, subtype='html',
                                    charset=email_charset, debug=False,
                                   )
        except (MailHostError, SMTPException):
            return _('token_role_send_ko_mail', default=u'Mail error')
        except Exception:
            return _('token_role_send_ko', default=u'An error has occurred')
        else:
            return _('token_role_send_ok', default=u'Token sent')

# wrap the form with plone.app.z3cform's Form wrapper
TokenSendFormView = layout.wrap_form(TokenSendForm)


