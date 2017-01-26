#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2017 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Bibcheck plugin to move values of fields matching some pattern
to a new field.

The new value is taken from the 'value' named group of 'pattern' (with the
'(?P<value>regexp)' construct), if it matches the value of source_field and put
into new_field. A subfield_filter can be specified to further restrict the
source field.

If there is a match, the original field is deleted. By default, the new field
is only created if it does not result in a duplicate value. This behavior can
be disabled by setting allow_duplicated to True.

Example rules:

"""


import re

from invenio.bibrecord import record_add_field, record_get_field_values

def check_record(record, source_field, new_field, pattern, subfield_filter,
                 allow_duplicates=False):
    assert len(source_field) == 6
    assert len(new_field) == 6
    delcount = 0
    regex = re.compile(pattern)
    existing_values = set(record_get_field_values(
        record, new_field[:3], new_field[3], new_field[4], new_field[5]))
    for pos, val in record.iterfield(source_field,
                                     subfield_filter=subfield_filter):
        if val:
            match = regex.match(val)
            if match:
                new_value = weblibmatch.group('value')
                if allow_duplicates or (
                        new_value != '' and new_value not in existing_values):
                    existing_values.add(new_value)
                    subfields_to_add = (new_field[5], new_value),
                    record_add_field(record, new_field[:3], new_field[3],
                                     new_field[4], new_field[5],
                                     subfields=subfields_to_add)
                record.delete_field((pos[0][0:3], pos[1] - delcount, None))
                delcount += 1
                record.set_amended(
                    "(re)moved field '%s' containing '%s'"
                    % (source_field, new_value))
            else:
                record.warn('no match for [%s] against [%s]' % (pattern, val))

