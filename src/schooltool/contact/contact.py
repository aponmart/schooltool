#
#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2009 Shuttleworth Foundation
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
Contact objects
"""
from persistent import Persistent

from zope.component import adapter
from zope.interface import implementer
from zope.interface import implements
from zope.app.container.contained import Contained
from zope.app.container.btree import BTreeContainer
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from zc.catalog.catalogindex import ValueIndex
from zc.catalog.extentcatalog import Catalog
from zc.catalog.extentcatalog import FilterExtent

from schooltool.app.interfaces import ISchoolToolApplication
from schooltool.app.app import InitBase, StartUpBase
from schooltool.utility.utility import UtilitySetUp
from schooltool.contact.interfaces import IContactPersonInfo
from schooltool.contact.interfaces import IContactable
from schooltool.contact.interfaces import IContact, IContactContained
from schooltool.contact.interfaces import IContactContainer
from schooltool.contact.interfaces import IUniqueFormKey
from schooltool.relationship.uri import URIObject
from schooltool.relationship.relationship import BoundRelationshipProperty
from schooltool.relationship.relationship import RelationshipProperty
from schooltool.relationship.relationship import RelationshipSchema
from schooltool.securitypolicy import crowds
from schooltool.table.catalog import ConvertingIndex
from schooltool.table.catalog import FilterImplementing
from schooltool.table.table import simple_form_key
from schooltool.person.interfaces import IPerson
from schooltool.course.section import PersonInstructorsCrowd

from schooltool.common import SchoolToolMessage as _


CONTACT_CATALOG_KEY = 'schooltool.contact'

URIContactRelationship = URIObject('http://schooltool.org/ns/contact',
                                   'Contact relationship',
                                   'The contact relationship.')

URIContact = URIObject('http://schooltool.org/ns/contact/contact',
                       'Contact', 'A contact relationship contact record role.')

URIPerson = URIObject('http://schooltool.org/ns/contact/person',
                      'Person', 'A contact relationship person role.')

Contact = RelationshipSchema(URIContactRelationship,
                             contact=URIContact, person=URIPerson)


class ContactGroup(crowds.DescriptionGroup):

    title = _(u"Contacts")

    description = _(u"""
    All SchoolTool users have contact information, that includes home address,
    phone number, email address, etc.

    "External contacts" can be created - people who are not SchoolTool users,
    but may need to recieve notifications and information about the student
    or the school as a whole.
    """)


class ContactContainer(BTreeContainer):
    """Container of persons."""

    implements(IContactContainer)


class Contact(Persistent, Contained):
    """Contact."""

    implements(IContactContained)

    prefix = None
    first_name = None
    middle_name = None
    last_name = None
    suffix = None
    address_line_1 = None
    address_line_2 = None
    city = None
    state = None
    country = None
    postal_code = None
    email = None
    home_phone = None
    work_phone = None
    mobile_phone = None
    language = None

    persons = RelationshipProperty(URIContactRelationship,
                                   my_role=URIContact,
                                   other_role=URIPerson)


class ContactPersonInfo(Persistent, Contained):
    """Additional information about contact of a specific person."""

    implements(IContactPersonInfo)

    __parent__ = None
    relationship = None

    def getRelationshipTitle(self):
        vocabulary = IContactPersonInfo['relationship'].vocabulary
        try:
            term = vocabulary.getTerm(self.relationship)
        except LookupError:
            return u''
        return term.title


class ContextRelationshipProperty(RelationshipProperty):
    """Context relationship property."""

    def __get__(self, instance, owner):
        """Bind the property to the context of an instance."""
        if instance is None:
            return self
        else:
            return BoundRelationshipProperty(instance.context,
                                             self.rel_type,
                                             self.my_role,
                                             self.other_role)


class Contactable(object):
    implements(IContactable)

    contacts = ContextRelationshipProperty(URIContactRelationship,
                                           my_role=URIPerson,
                                           other_role=URIContact)

    def __init__(self, context):
        self.context = context


class ContactAppStartup(StartUpBase):
    def __call__(self):
        if 'schooltool.contact' not in self.app:
            self.app['schooltool.contact'] = ContactContainer()


class ContactInit(InitBase):
    def __call__(self):
        self.app['schooltool.contact'] = ContactContainer()


@implementer(IContactContainer)
@adapter(ISchoolToolApplication)
def getContactContainer(app):
    return app['schooltool.contact']


@adapter(IContact)
@implementer(IUniqueFormKey)
def getContactFormKey(contact):
    doc_id = getUtility(IIntIds).getId(contact)
    return 'contacts.%s%x' % (simple_form_key(contact), doc_id)


def catalogFactory():
    return Catalog(FilterExtent(FilterImplementing(IContact)))


def catalogSetUp(catalog):
    catalog['form_keys'] = ConvertingIndex(converter=IUniqueFormKey)
    catalog['first_name'] = ValueIndex('first_name')
    catalog['last_name'] = ValueIndex('last_name')


catalogSetUpSubscriber = UtilitySetUp(
    catalogFactory, ICatalog, CONTACT_CATALOG_KEY, setUp=catalogSetUp)


def getContactCatalog(container):
    return getUtility(ICatalog, CONTACT_CATALOG_KEY)


class ContactPersonInstructorsCrowd(PersonInstructorsCrowd):
    """Crowd of instructors of any of related persons to this contact."""

    title = _(u'Instructors')
    description = _(u'Instructors of student(s) related to this contact.')

    def contains(self, principal):
        user = IPerson(principal, None)
        for person in self.context.persons:
            sections = self._getSections(person)
            for section in sections:
                if user in section.instructors:
                    return True
        return False
