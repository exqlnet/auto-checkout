# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime
import time
import copy
import re


def getCourse(account,cookie):
    session = requests.session()
    session.headers = {
        "Cookie": cookie,
        "Host": "mooc1-1.chaoxing.com"
    }
    url = 'http://mooc1-1.chaoxing.com/visit/interaction'
    time_ = time.time()
    time_ = int(round(time_ * 1000))
    print(time_)
    html = session.get(url).text
    if "Sign in" in html:
        print("草！还未登录，请先填写cookie！")

    soup = BeautifulSoup(html, "html.parser")
    ss = soup.select('.ulDiv > ul > li')
    classes = []
    class_ = {}

    for i in range(0,15):
        # print (ss[i].find('input',attrs={'name':'courseId'}))
        class_["courseId"] = ss[i].find('input',attrs={'name':'courseId'}).get('value')
        class_["jclassId"] = ss[i].find('input',attrs={'name':'classId'}).get('value')
        class_["courseName"] = ss[i].find('h3').find('a').text
        classes.append(copy.deepcopy(class_))


    with open("./classes_"+ account +".json", "w") as file:
        file.write(json.dumps(classes))
    print ("获取课程id成功，愉快的签到去吧~")


    

if __name__ == "__main__":
    pass