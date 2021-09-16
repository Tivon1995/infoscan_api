import sys
from . import api
from ..utils import *
from app.api.dirsearch.dirsearch import Program
from flask import request


@api.route('/dir')
def dir_search():
    target = str(request.args.get('target', ''))
    if target.startswith('http://') or target.startswith('https://'):
        domain = target.split('/')[2]
    else:
        domain = target.split('/')[0]
    # tmp = []
    # tmp.append(domain)
    # sys.argv= ['dirsearch.py', '-e', '*', '-u'] + tmp

    dirscan = Program(target)
    dirscan.output.arr.sort()
    dir_data = []
    for i in dirscan.output.arr:
        if (domain in i) == False:
            i = i + "  ->  " + (target + i[i.index("/"):])
            dir_data.append(i)
        else:
            dir_data.append(i)
    return success(dir_data)

