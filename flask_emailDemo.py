#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Howard_Lee
import re
import time

from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
# app.config.update(
#     #  hotmail的設置
#     MAIL_SERVER='smtp.live.com',
#     MAIL_PROT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME='h9052300@hotmail.com',
#     MAIL_PASSWORD='h3141200770130'
# )


app.config.update(
    #  MMXtion_mail的設置
    MAIL_SERVER='mail.mmxtion.com.tw',
    MAIL_PROT=25,
    MAIL_USE_TLS=False,
    MAIL_USERNAME='mmx_devservice@mmxtion.com.tw',
    MAIL_PASSWORD='MMX83951011'
)

#  記得先設置參數再做實作mail
mail = Mail(app)


# 爬蟲抓取雲盤關鍵字列表最近發表紀錄
@app.route('/mail/')
def send_mail():
    content = reptile(2)
    today = time.strftime("%Y-%m-%d", time.localtime())

    #  主旨
    msg_title = f'雲盤精靈 {today} 快報'
    #  寄件者，若參數有設置就不需再另外設置
    msg_sender = 'mmx_devservice@mmxtion.com.tw'
    #  收件者，格式為list，否則報錯
    msg_recipients = ['howard.lee@mmxtion.com.tw', 'h9052300@gmail.com']
    #  郵件內容
    msg_body = content
    msg = Message(msg_title,
                  sender=msg_sender,
                  html=msg_body,
                  recipients=msg_recipients)
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'


def reptile(pageNum):
    from bs4 import BeautifulSoup
    import requests
    word = ['python', 'AWS', 'Golang', '破解', 'DOCKER', '树莓派', 'Flask',
            'Raspberry', 'Kubernetes', '自动', '渗透', '授信', '信贷', '瑞客论坛www.ruike1co',
            'pytorch', '漏洞', '识别', '预测', '清单']
    # word = ['Flask', '自动']
    linkURL = []
    for i in word:
        for pg in range(1, pageNum + 1):
            url = f'https://www.yunpanjingling.com/search/{i}?filter_time=latest_a_month&sort=share_time.desc&page={pg}'
            web_data = requests.get(url).text
            soup = BeautifulSoup(web_data, 'lxml')

            for x in range(1, 11):
                meaning = soup.select(
                    f"body > div.main > div.search-list > div:nth-child({x}) > div.wrapper > div.name > a")
                linkURL.append(meaning)
                iconText = re.findall(r'\d{1,2}[\u4e00-\u9fa5]{2,4}', str(
                    soup.select(f"body > div.main > div.search-list > div:nth-child({x}) > div.share > span")))
                linkURL.append(iconText)
        content = str(linkURL).replace(r'[<a href="/', r'[<a href="https://www.yunpanjingling.com/').replace("[[",
                                                                                                             "").replace(
            "]]", "").replace("], [", "\n").replace("</a>", "</a> <br/>").replace(r"'", "")
        time.sleep(2)
    return content


@app.route("/message")
def message():
    #  主旨
    msg_title = 'Hello It is Flask-Mail 早安，吃太多會變豬喔'
    #  寄件者，若參數有設置就不需再另外設置
    msg_sender = 'mmx_devservice@mmxtion.com.tw'

    #  收件者，格式為list，否則報錯
    # msg_recipients = ['tiger.liao@mmxtion.com.tw', 'aubrey.wung@mmxtion.com.tw', 'howard.lee@mmxtion.com.tw',
    #                   'nicho.chou@mmxtion.com.tw', 'jesschan@tiis.com.tw']

    meg_recipients = [("Howard", "howard.lee@mmxtion.com.tw"), ("JESS", "jesschan@tiis.com.tw"),
                      ("阿肥", "aubrey.wung@mmxtion.com.tw"), ("虎哥", "tiger.liao@mmxtion.com.tw"),
                      ("Nicho", "nicho.chou@mmxtion.com.tw")]
    #  郵件內容
    msg_body = '表單核准通知,表單資訊如下[表單資訊] 表單名稱:網路資源申請單 版本:13.00 表單單號:MIS200300001申請時間:2020/03/03 14:02 申請者:李冠興表單狀態:已結案申請結果:核准”'

    #  也可以使用html
    #  msg_html = '<h1>Hey,Flask-mail Can Use HTML</h1>'
    msg = Message(msg_title,
                  # sender=msg_sender,
                  sender=("MMXtion", "mmx_devservice@mmxtion.com.tw"),
                  # recipients=msg_recipients)
                  recipients=meg_recipients)
    msg.body = msg_body
    #  msg.html = msg_html

    #  mail.send:寄出郵件
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'


if __name__ == "__main__":
    app.run(debug=True)
