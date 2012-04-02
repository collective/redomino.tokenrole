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

from random import random
from time import time
from md5 import md5
import socket

SEP = '-'
try:
    _v_network = str(socket.gethostbyname(socket.gethostname()))
except:
    _v_network = str(random() * 100000000000000000L)

def make_uuid(*args):
    
    t = str(time() * 1000L)
    r = str(random()*100000000000000000L)
    data = t + SEP + r + SEP + _v_network + SEP + str(args)
    uid = md5(data).hexdigest()
    return uid
