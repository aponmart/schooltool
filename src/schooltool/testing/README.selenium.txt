===================================
SchoolTool Selenium Testing Support
===================================

Browser extensions
==================

We can access Selenium browser extensions using the 'ui' attribute of
the browser object, like this:

    >>> browser.ui.EXTENSION_GOES_HERE

Most of the extensions are coded in the stesting.py modules in their
corresponding packages. Look for their functional tests in the
selenium_extensions.txt stest files.

We have browser extensions for:

Logging in
----------

* browser.ui.login()

  Required parameters:
    username
    password

Adding persons
--------------

* browser.ui.person.add()

  Required parameters:
    first_name
    last_name
    username
    password
  Optional keyword parameters:
    prefix
    middle_name
    suffix
    preferred_name
    gender: text of the option to select
    birth_date: YYYY-MM-DD date
    ID
    ethnicity: text of the option to select
    language
    placeofbirth
    citizenship
    group: text of the option to select
    advisor: text of the option to select

  NOTE: if ends is not set, the section will end in the starting term

Adding school years
------------------

* browser.ui.schoolyear.add()

  Required parameters:
    title
    first: YYYY-MM-DD date
    last: YYYY-MM-DD date
  Optional keyword parameters:
    copy_groups: list of non built-in group identifiers from previous year
    copy_members: list of non built-in group identifiers from previous year
    copy_courses: bool
    copy_timetables: bool

Adding terms
------------

* browser.ui.term.add()

  Required parameters:
    schoolyear: title of the school year
    title
    first: YYYY-MM-DD date
    last: YYYY-MM-DD date

Adding courses
--------------

* browser.ui.course.add()

  Required parameters:
    schoolyear: title of the school year
    title
  Optional keyword parameters:
    description
    course_id
    government_id
    credits

Adding sections
---------------

* browser.ui.section.add()

  Required parameters:
    schoolyear: title of the school year
    term: title of the term
    course: title of the course
  Optional keyword parameters:
    title
    description
    ends: title of the term when it ends

  NOTE: if ends is not set, the section will end in the starting term

Visiting a section
------------------

* browser.ui.section.go()

  Required parameters:
    schoolyear: title of the school year
    term: title of the term
    section: title of the section

Adding instructors to a section
-------------------------------

* browser.ui.section.instructors.add()

  Required parameters:
    schoolyear: title of the school year
    term: title of the term
    section: title of the section
    instructors: list with person usernames

    NOTE: it doesn't matter if some of the usernames are already
          instructors of the section

Adding students to a section
----------------------------

* browser.ui.section.students.add()

  Required parameters:
    schoolyear: title of the school year
    term: title of the term
    section: title of the section
    students: list with person usernames

    NOTE: it doesn't matter if some of the usernames are already
          students of the section

Adding groups
-------------

* browser.ui.group.add()

  Required parameters:
    schoolyear: title of the school year
    title
  Optional keyword parameters:
    description

Visiting a group
----------------

* browser.ui.group.go()

  Required parameters:
    schoolyear: title of the school year
    group: title of the group

Adding members to a group
-------------------------

* browser.ui.group.members.add()

  Required parameters:
    schoolyear: title of the school year
    group: title of the group
    members: list with person usernames

    NOTE: it doesn't matter if some of the usernames are already
          members of the group

Element extensions
==================

We can access Selenium element extensions using the 'ui' attribute of
the element object, like this:

    >>> element = browser.QUERY_THE_ELEMENT_SOMEHOW
    >>> element.ui.EXTENSION_GOES_HERE

The element extensions are coded in the stesting.py module of the
skin.flourish package.

We have element extensions for:

Entering dates
--------------

* element.ui.enter_date()

  Required parameters:
    date: YYYY-MM-DD date

Selecting an option in a menu
-----------------------------

* element.ui.select_option()

  Required parameters:
    option: text of the option to select

Setting the value of a field without caring about its type
----------------------------------------------------------

* element.ui.set_value

  Required parameters:

    value: text that can represent a regular text input, the content
    of a textarea (it's possible to set break lines using \n), a
    YYYY-MM-DD used in the datepicker widget or the text of an option
    in a menu