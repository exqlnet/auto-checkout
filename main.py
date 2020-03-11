import requests
import json
from threading import Thread
from datetime import datetime
import time
from bs4 import BeautifulSoup


base_url = "https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId={courseId}&jclassId={jclassId}"

with open("./config.json", "r") as file:
    config = json.load(file)

def log(*args, **kwargs):
    print(datetime.now(), *args, **kwargs)


for i, k in enumerate(config):
    log("{}: {}".format(i, k))

# print("请选择需要监控的账号：", end="")
# account = input("")
# print(account)




class Monitor:

    checkouted = set()


    def __init__(self, cookie, classes):

        self.cookie = cookie

        self.session = requests.session()
        self.session.headers = {
            "Cookie": cookie,
        }

        self.classes = classes

    def get_task_list(self):


        for c in self.classes:
            url = base_url.format(courseId=c["courseId"], jclassId=c["jclassId"])

            res = self.session.get(url)

            soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")

            tasks_node = soup.select("#startList > div > div")

            tasks = []

            for node in tasks_node:
                task_type = node.select("[shape='rect']")[0].text.strip()
                endTime = node.select(".fr.pzt span")[0].text.strip()
                task_id = node.get("onclick").split("(")[1].split(",")[0]

                tasks.append({
                    "task_type": task_type,
                    "endTime": endTime,
                    "activeId": task_id,
                    "classId": c["jclassId"],
                    "courseId": c["courseId"],
                    "courseName": c.get("courseName"),
                })
            return tasks

    def checkout(self, task):
        if task["activeId"] in self.checkouted:
            return False

        res = self.session.get("https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/preSign" \
            "?activeId={activeId}&classId={classId}&fid=262&courseId={courseId}".format(activeId=task["activeId"], classId=task["classId"], courseId=task["courseId"]))

        if "签到成功" in res.text:
            self.checkouted.add(task["activeId"])
            with open("index.html", "a+") as file:
                file.write(str(datetime.now()) + " 签到成功：" + task["courseName"] + "\n<br>")
            return True
        else:
            return False

        return 





def account_task(account):

    monitor = Monitor(config[account]["cookie"], config[account]["classes"])

    while True:
        log("✊ 检查账号签到任务：", account)
        tasks = monitor.get_task_list()
        for task in tasks:
            if monitor.checkout(task):
                log("✌️ 签到成功:", task["courseName"])

        time.sleep(10)


for ac in config:
    log("📺 开始监控", ac)
    thr = Thread(target=account_task, args=(ac,))
    thr.start()

log("👌 线程启动完毕！")








