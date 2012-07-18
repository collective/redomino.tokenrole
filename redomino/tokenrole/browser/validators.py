# Copyright (c) 2012 Redomino srl (http://redomino.com)
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

from zope.interface import Invalid

from z3c.form import validator

from redomino.tokenrole.interfaces import ITokenInfoSchema

class SampleValidator(validator.SimpleFieldValidator):
    
    def validate(self, value):
        super(SampleValidator, self).validate(value)

        if value < datetime.datetime.now():
            raise Invalid('Date not valid')
        
validator.WidgetValidatorDiscriminators(SampleValidator, field=ITokenInfoSchema['token_end'],)
