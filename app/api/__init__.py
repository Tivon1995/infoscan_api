from flask import Blueprint

api=Blueprint('api',__name__)

import app.api.Whois
import app.api.subdomain
import app.api.portscan
import app.api.all_msg
import app.api.get_cdn
import app.api.ping
import app.api.dir
import app.api.title
import app.api.img