import requests
import re
import sys
import time
import execjs
import threading
headers = {
    'Host': 'wechat.v2.traceint.com',
    'Referer': 'https://wechat.v2.traceint.com/index.php',
    'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x1700122f) NetType/4G Language/zh_CN',
    'X-Requested-With': 'XMLHttpRequest',
}
headers2 = {
    'Referer': '',
    'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x1700122f) NetType/4G Language/zh_CN',
    'X-Requested-With': 'XMLHttpRequest',
}

fcookie = {
"domain":".traceint.com",
"Hm_lpvt_7ecd21a13263a714793f376c18038a87":"1609938206",
"Hm_lvt_7ecd21a13263a714793f376c18038a87":"1609938206",
"wechatSESS_ID":"bf02e1a0049f4245584c0bd7fa6b673e9494c45242373a8f",
"FROM_TYPE":"weixin",
"SERVERID":"b9fc7bd86d2eed91b23d7347e0ee995e|1609938205|1609938204",
}
main_url = 'https://wechat.v2.traceint.com/index.php/reserve/index.html'
num_lou = [0,0,0,716,730,737,765,744,786,751,758,772,779]
apply_url = 'https://wechat.v2.traceint.com/index.php/reserve/get/libid='
lou_url1 = 'https://wechat.v2.traceint.com/index.php/reserve/layout/libid='
lou_url2 = '.html&1603766800'


def getdata(url,cookie):
    response = requests.get(url, headers=headers, cookies=cookie)
    # print(response.text.encode(response.encoding).decode(response.apparent_encoding))# 防止乱码
    return response.text
    # return response.text.encode(response.encoding).decode(response.apparent_encoding)

def read_lou(htdata):# change this
    pattern = re.compile(r'(\d{1,3})/\d{1,3}')
    result = pattern.findall(htdata)
    answ = []
    print(result)
    for i in range(9,-1,-1): # 9 -1 -1 ok 11 10 9 6 5
        if result[i] != str(0):
            answ.append(i+3)
            break
    return answ


def getnkey(jsdata):
    st = jsdata.find('AJAX_UR')
    st=st+4
    en = jsdata.find('&yzm=')
    print(jsdata[st:en])
    while jsdata[st] != '(':
        st = st+1
    while jsdata[en] != ')':
        en = en-1
    print(jsdata[st: en])
    while jsdata[st-1] != '+':
        st = st-1
    while jsdata[en+1] != '+':
        en = en+1
    print(jsdata[st:en+1])
    jsdata = jsdata[0:jsdata.find('T.ajax_get')] + "return " + jsdata[st:en+1] + "\n" + jsdata[jsdata.find('T.ajax_get'):]
    # print(jsdata)
    js = execjs.compile(jsdata)
    return js.call('reserve_seat')

def getweizhi(h,point,nkey,cookie):
    url = apply_url + str(h) + '&' + nkey + '=' + point+'&yzm='
    print(url)
    bb = getdata(url,cookie)
    return bb
def getdatajs(url,cookiee):
    cookie = {
        "Hm_lpvt_7ecd21a13263a714793f376c18038a87": cookiee['Hm_lpvt_7ecd21a13263a714793f376c18038a87'],
        "Hm_lvt_7ecd21a13263a714793f376c18038a87": cookiee['Hm_lvt_7ecd21a13263a714793f376c18038a87'],
        "wechatSESS_ID": cookiee['wechatSESS_ID'],
    }
    response = requests.get(url, headers=headers2, cookies=cookie)
    return response.text

def read_point(htdata):
    pattern = re.compile(r'<div.*? grid_1.*? data-key="(.*?)" s.*?>')
    result = pattern.findall(htdata)
    return result

def read_js(htdata):
    pattern = re.compile(r'src="(.*?.js)"')
    result = pattern.findall(htdata)
    return result[1]

def qiang(cookie,lou):
    # mhtml = getdata(main_url, cookie)
    lhtml = getdata(lou_url1 + str(num_lou[lou[0]]) + lou_url2,cookie)
    point = read_point(lhtml)
    js = read_js(lhtml)
    print(js)
    jsd = getdatajs(js, cookie)
    print(jsd)
    nkey = getnkey(jsd)
    print(nkey)
    print(lou[0])
    print(point)
    # print(lhtml)
    if len(num_lou) ==0 or len(point)==0:
        return
    bb = getweizhi(num_lou[lou[0]], point[0], nkey,cookie)
    print(bb)
    while bb.find('\u9009\u5ea7\u4e2d,\u8bf7\u7a0d\u540e') !=-1:
        bb = getweizhi(num_lou[lou[0]], point[0], nkey,cookie)
        print(bb)
    if bb.find('\u8be5\u5ea7\u4f4d\u4e0d\u5b58\u5728!\u6e05\u5c1d\u8bd5\u5237\u65b0\u9875\u9762') !=-1:
        qiang(cookie,lou)
    if bb.find('\u8be5\u5ea7\u4f4d\u5df2\u7ecf\u88ab\u4eba\u9884\u5b9a\u4e86!')!=-1:
        print(bb)
        return
    if bb.find('success') != -1:
        sys.exit(0)

def myqiang(cookie):
    ttt = 0
    ci = 0
    while True:
        mhtml = getdata(main_url, fcookie)
        lou = read_lou(mhtml)
        if len(lou) > 0:
            qiang(cookie, lou)
        ttt = ttt + 1
        if ttt > 90:
            mhtml = getdata(main_url, cookie)
            ttt = ttt - 90
        print(ci)
        ci = ci + 1
        time.sleep(0.3)


class qiangThread (threading.Thread):
    def __init__(self, cookie):
        threading.Thread.__init__(self)
        self.cookie = cookie
    def run(self):
        myqiang(self.cookie)


def qiang_by_cookies(cookie):
    main_html=getdata(main_url,cookie)
    # print(main_html)
    if len(main_html) < 100:
        return 0
    threads = qiangThread(cookie)
    threads.start()
    return 1