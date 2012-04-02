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
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

PMF = MessageFactory('plone')

class ItemsVocab(object):
    implements(IVocabularyFactory)

    def __init__(self, terms, pmf):
        self.TERMS = terms
        self.PMF = pmf

    @property
    def terms(self):
        return self.TERMS

    def __call__(self, context):
        request = aq_get(context, 'REQUEST', None)
        terms = [SimpleTerm(value, token, translate(self.PMF(title), context=request)) for value, token, title in self.terms]
        return SimpleVocabulary(terms)


RolesFactory = ItemsVocab([('Reader', 'Reader', 'title_can_view'), 
                           ('Contributor', 'Contributor', 'title_can_add'), 
                           ('Reviewer', 'Reviewer', 'title_can_review'), 
                           ('Editor', 'Editor', 'title_can_edit'),
                          ], 
                          PMF
                         )


