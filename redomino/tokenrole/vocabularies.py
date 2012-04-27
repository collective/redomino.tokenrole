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

from Acquisition import aq_get

from zope.interface import implements
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm


class ItemsVocab(object):
    implements(IVocabularyFactory)

    def __init__(self, terms):
        self.TERMS = terms

    @property
    def terms(self):
        return self.TERMS

    def __call__(self, context):
        request = aq_get(context, 'REQUEST', None)
        terms = [SimpleTerm(value, token, translate(title, domain="plone", context=request, default=default)) for value, token, title, default in self.terms]
        return SimpleVocabulary(terms)


RolesFactory = ItemsVocab([('Reader', 'Reader', 'title_can_view', u'Can view'), 
                           ('Contributor', 'Contributor', 'title_can_add', u'Can add'), 
                           ('Reviewer', 'Reviewer', 'title_can_review', u'Can review'), 
                           ('Editor', 'Editor', 'title_can_edit', u'Can edit'),
                          ]
                         )


