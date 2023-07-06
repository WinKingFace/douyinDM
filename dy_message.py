# -*- coding: utf-8 -*-
# @Time    : 2023/5/8 3:12 下午
# @Author  : CC
import gzip
import json
from google.protobuf import json_format


from test_cc.dy_pb2 import MatchAgainstScoreMessage
from test_cc.dy_pb2 import LikeMessage
from test_cc.dy_pb2 import MemberMessage
from test_cc.dy_pb2 import GiftMessage
from test_cc.dy_pb2 import ChatMessage
from test_cc.dy_pb2 import SocialMessage
from test_cc.dy_pb2 import RoomUserSeqMessage
from test_cc.dy_pb2 import UpdateFanTicketMessage
from test_cc.dy_pb2 import CommonTextMessage


class DYMessage:
    def __init__(self, liveRoomId):
        self.liveRoomId = liveRoomId
    def unPackWebcastCommonTextMessage(self, data):
        commonTextMessage = CommonTextMessage()
        commonTextMessage.ParseFromString(data)
        data = json_format.MessageToDict(commonTextMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastCommonTextMessage] [] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    def unPackWebcastUpdateFanTicketMessage(self, data):
        updateFanTicketMessage = UpdateFanTicketMessage()
        updateFanTicketMessage.ParseFromString(data)
        data = json_format.MessageToDict(updateFanTicketMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastUpdateFanTicketMessage] [] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    def unPackWebcastRoomUserSeqMessage(self, data):
        roomUserSeqMessage = RoomUserSeqMessage()
        roomUserSeqMessage.ParseFromString(data)
        data = json_format.MessageToDict(roomUserSeqMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastRoomUserSeqMessage] [] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    def unPackWebcastSocialMessage(self, data):
        socialMessage = SocialMessage()
        socialMessage.ParseFromString(data)
        data = json_format.MessageToDict(socialMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastSocialMessage] [➕直播间关注消息] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    # 普通消息
    def unPackWebcastChatMessage(self, data):
        chatMessage = ChatMessage()
        chatMessage.ParseFromString(data)
        data = json_format.MessageToDict(chatMessage, preserving_proto_field_name=True)
        # print('[unPackWebcastChatMessage] [📧直播间弹幕消息] [房间Id：' + self.liveRoomId + '] ｜ ' + data['content'])
        # print('[unPackWebcastChatMessage] [📧直播间弹幕消息] [房间Id：' + self.liveRoomId + '] ｜ ' + json.dumps(data))
        return data

    # 礼物消息
    def unPackWebcastGiftMessage(self, data):
        giftMessage = GiftMessage()
        giftMessage.ParseFromString(data)
        data = json_format.MessageToDict(giftMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastGiftMessage] [🎁直播间礼物消息] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    # xx成员进入直播间消息
    def unPackWebcastMemberMessage(self, data):
        memberMessage = MemberMessage()
        memberMessage.ParseFromString(data)
        data = json_format.MessageToDict(memberMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastMemberMessage] [🚹🚺直播间成员加入消息] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data

    # 点赞
    def unPackWebcastLikeMessage(self, data):
        likeMessage = LikeMessage()
        likeMessage.ParseFromString(data)
        data = json_format.MessageToDict(likeMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackWebcastLikeMessage] [👍直播间点赞消息] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return log

    # 解析WebcastMatchAgainstScoreMessage消息包体
    def unPackMatchAgainstScoreMessage(self, data):
        matchAgainstScoreMessage = MatchAgainstScoreMessage()
        matchAgainstScoreMessage.ParseFromString(data)
        data = json_format.MessageToDict(matchAgainstScoreMessage, preserving_proto_field_name=True)
        log = json.dumps(data, ensure_ascii=False)
        # print('[unPackMatchAgainstScoreMessage] [🤷不知道是啥的消息] [房间Id：' + self.liveRoomId + '] ｜ ' + log)
        return data
