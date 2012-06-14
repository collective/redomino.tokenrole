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

from zope import schema
from zope.interface import Interface

from redomino.tokenrole.validators import isEmail

from redomino.tokenrole import tokenroleMessageFactory as _


class ITokenSendForm(Interface):
    """ Form invio token ad una lista di email """

    token_id = schema.ASCIILine(title = _(u'label_tokenrole_token_id', default=u'Token id'),
                                description = _(u'help_tokenrole_token_id', default=u'This token is going to be distributed.'),
                                required = True,
                               )
    subject = schema.TextLine(title = _(u'label_tokenrole_subject', default=u'Subject'),
                              description = _(u'help_tokenrole_subject', default=u'Please enter the subject of the message you want to send.'),
                              required = True,
                             )
    text = schema.Text(title = _(u'label_tokenrole_text', default=u'Text'),
                       description = _(u'help_tokenrole_text', default=u"Please enter here the message you want to send. Please, do not remove ${date} and ${url} tokens or the email won't be complete."),
                       default = u'Date: ${date}s\nUrl: ${url}s',
                       required = True,
                      )
    email_list = schema.List(title = _(u'label_tokenrole_email_list', default=u'List of emails'),
                             description = _(u'help_tokenrole_email_list', default=u'Please enter here the list of emails. One per line'),
                             required = True,
                             default = [],
                             value_type = schema.ASCIILine(title=_(u'label_email', default="Email"), constraint=isEmail),
                            )
