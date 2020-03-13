# 超星自动签到

## 使用说明

* 克隆代码到本地

```
git clone https://github.com/exqlnet/auto-checkout
```

* 安装依赖

```
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

* 填写配置文件
  * 登录超星网站
  * 从浏览器获得超星学习通网站cookie
  * 每个科目都对应一个jClassId（或者classId）和courseId
  * 将上述获取到的信息按格式填入config.json


* 启动

```
python main.py
```
