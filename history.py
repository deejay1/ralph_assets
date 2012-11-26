#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def field_changes(instance, ignore=('last_seen',)):
    """
    Yield the name, original value and new value for each changed field. Skip
    all insignificant fields and those passed in ``ignore``.
    """
    for field, orig in instance.dirty_fields.iteritems():
        if field in ignore:
            continue
        if field in instance.insignificant_fields:
            continue
        if field.endswith('_id'):
            field = field[:-3]
            parent_model = instance._meta.get_field_by_name(
                field
            )[0].related.parent_model
            try:
                if orig is not None:
                    orig = parent_model.objects.get(pk=orig)
            except parent_model.DoesNotExist:
                orig = None
        try:
            new = getattr(instance, field)
        except AttributeError:
            continue
        yield field, orig, new