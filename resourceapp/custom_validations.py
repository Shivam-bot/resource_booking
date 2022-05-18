import re

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


def check_string(data: str):
    for my_str in data:
        if my_str.isdigit():
            return True,"Special Character or digits not allowed"
        if my_str.isspace():
            return True, "Space Not allowed"
    if regex.search(data):
        return True,"Special Character or digits not allowed"
    return False, ""

