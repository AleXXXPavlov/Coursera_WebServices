import re
from regexp import calculate


def findall(regexp):
    text = """
    a=1
    a=+1
    a=-1
    a=b
    a=b+100
    a=b-100

    b+=10
    b+=+10
    b+=-10
    b+=b
    b+=b+100
    b+=b-100

    c-=101
    c-=+101
    c-=-101
    c-=b
    c-=b+101
    c-=b-101
    """

    return re.findall(regexp, text)


