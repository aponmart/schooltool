#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2005 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Tests for scholltool.rest.app

$Id: __init__.py 3344 2005-03-30 22:36:28Z alga $
"""

from zope.app.testing.functional import HTTPCaller
from zope.publisher.http import HTTPRequest
from zope.app.publication.http import HTTPPublication


class RESTCaller(HTTPCaller):
    """An HTTP caller for REST functional page tests"""

    def chooseRequestClass(self, method, path, environment):
        """Always returns HTTPRequests regardless of methods and content"""
        return HTTPRequest, HTTPPublication


rest = RESTCaller()
