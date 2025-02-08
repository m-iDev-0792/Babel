import sys
import os
import logging
import uuid
from Translator import GTranslateManager
import datetime

class UserInfo:
    def __init__(self, userName, preferredLang = None):
        self.UserId = uuid.uuid4()
        self.UserName = userName
        self.PreferredLang = preferredLang


class ChatMessage:
    def __init__(self, senderName, content, language):
        self.SenderName = senderName
        self.OriginalContent = content
        self.Language = language
        self.Content = ''
        self.Time = datetime.datetime.now()

    def Translate(self):
        self.Content = GTranslateManager.Translate(self.OriginalContent, self.Language)
        pass

class ChatRoom:
    def __init__(self, Id):
        self.Id = Id
        self.History = []
        self.Users = set()


class BabelChatManager:
    def __init__(self):
        self.ChatRooms = {}
        self.UserInfo = {}

    def AddUserInfo(self, userName, preferredLang):
        if userName not in self.UserInfo:
            self.UserInfo[userName] = UserInfo(userName, preferredLang)
            return True
        return False

    def AddChatRoom(self, chatRoomId):
        if isinstance(chatRoomId, str) and chatRoomId not in self.ChatRooms:
            self.ChatRooms[chatRoomId] = ChatRoom(chatRoomId)
            return True
        return False

    def GetChatRooms(self):
        ret = []
        for chatRoomId in self.ChatRooms:
            userList = []
            for user in self.ChatRooms[chatRoomId].Users:
                userList.append(user)
            roomInfo = {"RoomId": chatRoomId, "UserList": userList}
            ret.append(roomInfo)
        return ret

    def AddMessage(self, chatRoomId, userName, message, targetLang = None):
        if chatRoomId not in self.ChatRooms:
            logging.log(logging.ERROR, f'AddMessage(): chatRoomId {chatRoomId} does not exist')
            return {}
        else:
            logging.log(logging.DEBUG, f'AddMessage(): chatRoomId {chatRoomId}, userName {userName}, message {message}, targetLang {targetLang}')
            lang = targetLang
            if userName in self.UserInfo:
                lang = self.UserInfo[userName].PreferredLang
            else:
                logging.log(logging.ERROR, f'AddMessage(): userName {userName} does not exist')
                return {}
            msg = ChatMessage(userName, message, lang)
            msg.Translate()
            self.ChatRooms[chatRoomId].History.append(msg)
            self.ChatRooms[chatRoomId].Users.add(userName)
            return self.GetHistory(chatRoomId)


    def GetHistory(self, chatRoomId): # todo. verify users
        if chatRoomId not in self.ChatRooms:
            return []
        else:
            history = self.ChatRooms[chatRoomId].History
            retHistory = []
            for msg in history:
                retHistory.append({"SenderName": msg.SenderName, "Content": msg.Content, "Language": msg.Language, "OriginalContent": msg.OriginalContent, "Time": f'{msg.Time}'})
            return retHistory

GBabelChatManager = BabelChatManager()