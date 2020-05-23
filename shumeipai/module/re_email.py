import re


def validateEmail(email):  # 0为错 1为对
    if re.match('^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$', email) is not None:
        return '1'
    else:
        return '0'
