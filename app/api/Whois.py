from . import api
from ..utils import *
from flask import request
import whois


@api.route('/whois')
def get_whois():
    target = str(request.args.get('target', ''))
    if target.startswith('http://') or target.startswith('https://'):
        domain = target.split('/')[2]
    else:
        domain = target.split('/')[0]
    return success(whois.whois(domain))

