import functools
import lib.gangster_func as GF

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from lib.db import get_db

bp = Blueprint('gangster', __name__, url_prefix='/gangster')


cookie = {
"domain":".traceint.com",
"Hm_lpvt_7ecd21a13263a714793f376c18038a87":"1609938206",
"Hm_lvt_7ecd21a13263a714793f376c18038a87":"1609938206",
"wechatSESS_ID":"bf02e1a0049f4245584c0bd7fa6b673e9494c45242373a8f",
"FROM_TYPE":"weixin",
"SERVERID":"b9fc7bd86d2eed91b23d7347e0ee995e|1609938205|1609938204",
}


@bp.route('/getseat', methods=['GET','POST'])
def getseat():
    if request.method == 'POST':
        lpvt = request.form['lpvt']
        lvt = request.form['lvt']
        wechat_id = request.form['wechat_id']
        serverid = request.form['serverid']
        print(lpvt+lvt+wechat_id+serverid)
        cookie['Hm_lpvt_7ecd21a13263a714793f376c18038a87']=lpvt
        cookie['Hm_lvt_7ecd21a13263a714793f376c18038a87']=lvt
        cookie['wechatSESS_ID']=wechat_id
        cookie['SERVERID']=serverid
        dd = GF.qiang_by_cookies(cookie)
        if dd==0:
            return render_template('gangster/error.html')
    return render_template('gangster/getseat1.html')



