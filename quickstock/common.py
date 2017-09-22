# -*- coding: utf-8 -*-


def stringifySotckToList(collection):
    list = ""
    for item in collection:
        list = list + str(item.id) + "  " + item.name + "\n"
    return list

def stringifyItemToList(collection):
    list = ""
    for item in collection:
        if item.amount == 0:
            list = list + '**{:03d}'.format(item.id) + "  " + item.name + " " + str(item.amount) + "**\n"
        else:
            if item.amount == 1:
                list = list + '__{:03d}'.format(item.id) + "  " + item.name + " " + str(item.amount) + "__\n"
            else:
                list = list + '{:03d}'.format(item.id) + "  " + item.name + " " + str(item.amount) + "\n"
    return list

def validID(id, collection):
    valid = False
    for item in collection:
        if item.id == int(id):
            valid = True
            break
    return valid

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'