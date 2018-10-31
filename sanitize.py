# This module provides checks for various input fields.
special_characters = {
    '~',
    ':',
    "'",
    '+',
    '[',
    '\\',
    '@',
    '^',
    '{',
    '%',
    '(',
    '-',
    '"',
    '*',
    '|',
    ',',
    '&',
    '<',
    '`',
    '}',
    '.',
    '_',
    '=',
    ']',
    '!',
    '>',
    ';',
    '?',
    '#',
    '$',
    ')',
    '/'}


def clean(x):
    temp = ''
    for i in range(0, len(x)):
        if x[i] in special_characters:
            temp += 'X'
        else:
            temp += x[i]
    return temp

# this function checks if the given transaction amount is valid or not
# input is assumed to be of string type


def check_amount(x):
    flag = False
    if x > 0 and x < 999999999 and isinstance(x, int):
        flag = True
    return flag


def check_uname(x):
    x = clean(x)
    flag = False
    special = sum(1 for i in x if i in special_characters) > 0
    if not special:
        flag = True
    return flag


def check_pw(x):
    x = clean(x)
    flag = False
    upper = sum(1 for i in x if i.isupper()) > 0
    lower = sum(1 for i in x if i.islower()) > 0
    num = sum(1 for i in x if i.isnum()) > 0
    special = sum(1 for i in x if i in special_characters) > 0
    if upper and lower and num and special:
        flag = True
    return flag
