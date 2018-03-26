"""
Item view helper functions
================

This module provides helper functions for all Item's views functions.
"""


def _organized_items_sequence(full_dict, done_items, superiors_items):
    """
    Function, that organized items ids according to their dependency from each other. First,
    the items that must be performed first

    :param full_dict: Dictionary, where keys are item ids, values are lists with items ids
                      on which they depend
    :type full_dict: dictionary

    :param done_items: Items ids, which have no dependency with other items
    :type done_items: list

    :param superiors_items: Items ids, which have dependency with other items
    :type superiors_items: list

    :return: list of ids
    """
    if not superiors_items:
        return done_items
    done_list = done_items
    item_list = superiors_items
    for item in item_list:
        if not set(full_dict[item]).difference(set(done_list)):
            done_list.append(item)
            item_list.remove(item)
    done_list = _organized_items_sequence(full_dict, done_list, item_list)
    return done_list


def organized_items_sequence(items_superiors_dict):
    """
    Function, that organized items ids according to their dependency from each other.

    :param items_superiors_dict: Dictionary, where keys are item ids, values are lists with items
                                 ids on which they depend
    :type items_superiors_dict: dictionary

    :return: list of ids
    """
    done_items = []
    superiors_items = []
    for key in items_superiors_dict:
        if not items_superiors_dict[key]:
            done_items.append(key)
        else:
            superiors_items.append(key)
    return _organized_items_sequence(items_superiors_dict, done_items, superiors_items)
