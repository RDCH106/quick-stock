# -*- coding: utf-8 -*-


def stringifySotckToList(collection):
    list = ""
    for item in collection:
        list = list + str(item.id) + "  " + item.name + "\n"
    return list

def stringifyItemToList(collection):
    list = ""
    for item in collection:
        list = list + str(item.id) + "  " + item.name + " " + item.amount + "\n"
    return list

def validID(id, collection):
    valid = False
    for item in collection:
        if item.id == int(id):
            valid = True
            break
    return valid
