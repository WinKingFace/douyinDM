# douyinDM

| 版本   | 更新内容                                                                             | 完成状态 | 更新时间       |
|------|---------------------------------------------------------------------------------------|--|------------|
| v1.0 | mitmproxy+ws完成了本地网络监控            | ✅ | 2023.07.06 |
| v1.1 | 准备基于Electron开发一个跨平台桌面版            | ❌ | 待定 |
### 安装依赖
```python
1. 安装python依赖
pip install -r requirements.txt -i https://pypi.douban.com/simple/
2. 生成proto
protoc -I . --python_out=. dy.proto
```
### 本地使用说明
```python
1. 启动服务
	python main.py
2.在当前路径会生成相对的证书
3.点击安装证书即可
4. 启动对应的客户端连接
5. 代理端口8081 ws端口2333 
```



### 目前使用的问题
- 不知道为啥 代理启动后抖音的直播页面打不开了，但是可以获取到数据
- 待补充


## 🧪私有化抖音
> 背景：考虑到 mitmproxy使用起来比较复杂，而且产考了很多网站，决定写一个线上版本的
> 开发语言：Go + WebSocket + Go-Zero

### 服务地址
> websocket地址：124.220.38.168:8899/v1/ws


![](https://www.showdoc.com.cn/server/api/attachment/visitFile?sign=57134260e33069bc518831f5d429b776&file=file.png)
### 召集小伙伴
- qq:931912343

![](https://www.showdoc.com.cn/server/api/attachment/visitFile?sign=40b039433a49f34136e1226ee0609957&file=file.png)

### 感谢一下项目
- https://github.com/YunzhiYike/douyin-live/tree/main
