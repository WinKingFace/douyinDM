# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 1:59 下午
# @Author  : CC

import asyncio
import gzip
import json
import threading

import websockets
from mitmproxy import http, options, ctx
from mitmproxy.tools.dump import DumpMaster

from dy_message import DYMessage
from dy_pb2 import PushFrame
from dy_pb2 import Response


class WebSocketThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self.server = None

    async def handle_websocket(self, websocket, path):
        self.server = websocket
        while True:
            try:
                msg = await websocket.recv()
            except Exception:
                await websocket.close()

    async def run_websocket_server(self):
        async with websockets.serve(self.handle_websocket, "", 2333):
            await asyncio.Future()  # run forever

    def send_websocket_message(self, message: str):
        if self.server and self.server.open:
            try:
                message_dump = json.dumps(message)
                asyncio.run_coroutine_threadsafe(self.server.send(message_dump), self._loop).result()
            except Exception:
                return

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self.run_websocket_server())

    def stop(self):
        asyncio.get_event_loop().call_soon_threadsafe(self.server.close)


class MitmProxy:
    def __init__(self, port, addon):
        self.options = options.Options(listen_port=port,confdir="./")
        self.master = DumpMaster(self.options, with_termlog=False, with_dumper=False)
        self.master.addons.add(addon)

    async def start(self):
        try:
            await self.master.run()
        except Exception as e:
            print(f"Error: {e}")

    def stop(self):
        self.master.shutdown()


class MyAddon:
    def __init__(self):
        self.websocket_server = WebSocketThread()
        self.websocket_server.start()

    def request(self, flow: http.HTTPFlow):
        response_headers = flow.response.headers
        response_body = flow.response.content.decode("utf-8")
        response_info = {'headers': response_headers, 'body': response_body}

    def response(self, flow: http.HTTPFlow):
        response_headers = flow.response.headers
        response_body = flow.response.content.decode("utf-8")
        response_info = {'headers': response_headers, 'body': response_body}

    def websocket_message(self, flow):
        print(flow.request.url
              )
        if 'webcast3-ws' in flow.request.url or 'webcast100' in flow.request.url:
            room_id = flow.request.query.get('room_id')
            try:
                message = flow.websocket.messages[-1]
            except Exception as e:
                message = None
            self.handle_wss_package(message.content)

    def handle_wss_package(self, wss_package):
        dy_message = DYMessage("123456")
        wssPackage = PushFrame()
        wssPackage.ParseFromString(wss_package)
        logId = wssPackage.logId
        decompressed = gzip.decompress(wssPackage.payload)
        payloadPackage = Response()
        payloadPackage.ParseFromString(decompressed)

        for msg in payloadPackage.messagesList:
            if msg.method == 'WebcastMatchAgainstScoreMessage':
                # 未知消息
                roomMsg = dy_message.unPackMatchAgainstScoreMessage(msg.payload)
                # self.request_finished.emit(roomMsg)
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue
            if msg.method == 'WebcastLikeMessage':
                # 点亮了 爱心
                roomMsg = dy_message.unPackWebcastLikeMessage(msg.payload)
                nickname = roomMsg['user']['nickName']
                msg = '💗 <font color="green">' + nickname + '</font>: 点亮了爱心'
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue

            if msg.method == 'WebcastMemberMessage':
                # 成员进入直播间消息
                roomMsg = dy_message.unPackWebcastMemberMessage(msg.payload)
                nickname = roomMsg['user']['nickName']
                msg = '👏 <font color="red">' + nickname + '</font>: 进入直播间'
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue
            if msg.method == 'WebcastGiftMessage':
                # 礼物消息
                roomMsg = dy_message.unPackWebcastGiftMessage(msg.payload)
                describe = roomMsg['common']['describe']
                msg = '🎁 <font color="red">' + describe + '</font>'
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue
            if msg.method == 'WebcastChatMessage':
                # 用户普通评论
                roomMsg = dy_message.unPackWebcastChatMessage(msg.payload)
                nickname = roomMsg['user']['nickName']
                msg = '💬 <font color="pink">' + nickname + '</font>: ' + roomMsg['content']
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue

            if msg.method == 'WebcastSocialMessage':
                # 直播间关注消息
                roomMsg = dy_message.unPackWebcastSocialMessage(msg.payload)
                nickname = roomMsg['user']['nickName']
                msg = '➕ <font color="red">' + nickname + '</font> ' + roomMsg['msg']
                print(msg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue

            if msg.method == 'WebcastRoomUserSeqMessage':
                # 当前观看人数
                roomMsg = dy_message.unPackWebcastRoomUserSeqMessage(msg.payload)
                total = roomMsg['total']
                totalStr = roomMsg['totalStr']
                text = "👀当前观看人数：" + str(total) + " (" + totalStr + ")"
                print(text)
                self.websocket_server.send_websocket_message(roomMsg)
                continue

            if msg.method == 'WebcastUpdateFanTicketMessage':
                roomMsg = dy_message.unPackWebcastUpdateFanTicketMessage(msg.payload)
                # self.request_finished.emit(roomMsg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue

            if msg.method == 'WebcastCommonTextMessage':
                roomMsg = dy_message.unPackWebcastCommonTextMessage(msg.payload)
                # self.request_finished.emit(roomMsg)
                self.websocket_server.send_websocket_message(roomMsg)
                continue


class Run:
    def __init__(self):
        self.websocket_port = None
        self.websocket_server = None
        self.mitmproxy = None

    def _load_file(self):
        self.websocket_port = 2333
        self.mitmproxy = 8081

    async def start_mitmproxy(self, addon):
        try:
            self.mitmproxy = MitmProxy(8082, addon)
            await self.mitmproxy.start()
        except KeyboardInterrupt:
            self.stop_all()

    def stop_mitmproxy(self):
        if self.mitmproxy:
            self.mitmproxy.stop()

    def stop_websocket_server(self):
        if self.websocket_server:
            self.websocket_server.stop()

    def start_all(self):
        addon = MyAddon()
        asyncio.run(self.start_mitmproxy(addon))

    def stop_all(self):
        loop = asyncio.get_event_loop()
        tasks = asyncio.Task.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()


if __name__ == '__main__':
    print("启动程序...")
    r = Run()
    try:
        r.start_all()
    except KeyboardInterrupt:
        pass
    finally:
        del r
