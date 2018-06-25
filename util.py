import re

'''
get_date_str(s) - 문자열 s 에서 "YYYY/MM" 문자열 추출
'''
def get_date_str(s):
    date_str = ''
    try:
        r = re.search("\d{4}/\d{2}", s)
    except TypeError:
        print(s)
        raise
    if r:
        date_str = r.group()
        date_str = date_str.replace('/', '-')

    return date_str
