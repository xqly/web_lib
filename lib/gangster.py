import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from lib.db import get_db

bp = Blueprint('gangster', __name__, url_prefix='/gangster')


cookie1 = {
"domain":".traceint.com",
"Hm_lpvt_7ecd21a13263a714793f376c18038a87":"1609931768",
"Hm_lvt_7ecd21a13263a714793f376c18038a87":"1609931768",
"wechatSESS_ID":"b799eb3c81f99780565561801ea4ca8b3ea5a933bd0064f1",
"FROM_TYPE":"weixin",
"SERVERID":"82967fec9605fac9a28c437e2a3ef1a4|1609931768|1609931766",
}


@bp.route('/getseat', methods=['GET','POST'])
def getseat():
    if request.method == 'POST':
        lpvt = request.form['lpvt']
        lvt = request.form['lvt']
        wechat_id = request.form['wechat_id']
        serverid = request.form['serverid']
        print(lpvt+lvt+wechat_id+serverid)
    return render_template('gangster/getseat1.html')



