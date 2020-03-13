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


class Monitor:

    checkouted = set()

    def __init__(self, cfg, ac):

        self.cookie = cfg["cookie"]
        self.ac = ac
        self.session = requests.session()
        self.session.headers = {
            "Cookie": self.cookie,
        }

        self.classes = cfg["classes"]

    def get_task_list(self):

        tasks = []
        for c in self.classes:
            url = base_url.format(courseId=c["courseId"], jclassId=c["jclassId"])

            res = self.session.get(url)
            soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")
            tasks_node = soup.select("#startList > div > div")

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
                file.write(str(datetime.now()) + self.ac + " 签到成功：" + task["courseName"] + "\n<br>")
            return True
        else:
            return False


    def check_expire(self):
        url = "http://i.mooc.chaoxing.com/space/index"

        return self.session.get(url, allow_redirects=False).status_code == 302

def account_task(account):
    monitor = Monitor(config[account], account)
    if monitor.check_expire():
        log("👮‍♀️ {}Cookie已过期，停止监控".format(account))
        return
    else:
        log("✅ {}账号Cookie正常".format(account))
    while True:
        tasks = monitor.get_task_list()
        log("✊ 检查账号签到任务：", account, tasks)
        for task in tasks:
            if monitor.checkout(task):
                log("✌️ 签到成功:", account, task["courseName"])

        time.sleep(10)

if __name__ == "__main__":
    for ac in config:
        log("📺 开始监控", ac)
        thr = Thread(target=account_task, args=(ac,))
        thr.start()

    log("👌 线程启动完毕！")








