# -*- coding: utf-8 -*-


def stringifySotckToList(collection):
    list = ""
    for item in collection:
        list = list + str(item.id) + "  " + item.name + "\n"
    return list