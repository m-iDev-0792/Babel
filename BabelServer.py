import os
import sys
import logging
import json

cmdpath = sys.argv[0]
basedir = os.path.dirname(cmdpath)
if basedir == '':
    basedir = os.curdir
pass
from Misc.ConfigIni import GConfig
GConfig.Load(basedir + "/BabelServer.ini")

import Misc.FileUtils as FileUtils
from flask import Flask, jsonify, request
from flask import send_from_directory, abort
from BabelChatManager import GBabelChatManager

logger = logging.getLogger()
logger.handlers.clear()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logPath = os.path.join(os.getcwd(), "Logs")
if not os.path.exists(logPath):
    os.mkdir(logPath)
file_handler = logging.FileHandler('Logs/BabelServer.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

app = Flask(__name__)

@app.route('/AddChatRoom', methods=['POST']) # ChatRoomId
def AddChatRoom():
    try:
        data = request.get_json()
        logging.log(logging.INFO, f'AddChatRoom(): received request = {data}')
        chatRoomId = data['ChatRoomId']
        ret = GBabelChatManager.AddChatRoom(chatRoomId)
        retJson = {"Result": ret}
        resStr = json.dumps(retJson)
        logging.log(logging.INFO, f'AddChatRoom(): Sending result <<<{resStr}>>>')
        return resStr
    except Exception as e:
        logging.log(logging.ERROR, f'AddChatRoom(): Exception {e}')
        return jsonify({})
@app.route('/AddMessage', methods=['POST']) # ChatRoomId
def AddMessage():
    try:
        data = request.get_json()
        logging.log(logging.INFO, f'AddMessage(): received request = {data}')
        chatRoomId = data['ChatRoomId']
        userName = data['UserName']
        message = data['Message']
        language = ''
        if "Language" in data:
            language = data['Language']
        retJson = GBabelChatManager.AddMessage(chatRoomId, userName, message, language)
        resStr = json.dumps(retJson)
        logging.log(logging.INFO, f'AddMessage(): Sending result <<<{resStr}>>>')
        return resStr
    except Exception as e:
        logging.log(logging.ERROR, f'AddMessage(): Exception {e}')
        return jsonify({})

@app.route('/GetHistory', methods=['POST']) # ChatRoomId
def GetHistory():
    try:
        data = request.get_json()
        logging.log(logging.INFO, f'GetHistory(): received request = {data}')
        chatRoomId = data['ChatRoomId']
        retJson = GBabelChatManager.GetHistory(chatRoomId)
        resStr = json.dumps(retJson)
        logging.log(logging.INFO, f'GetHistory(): Sending result <<<{resStr}>>>')
        return resStr
    except Exception as e:
        logging.log(logging.ERROR, f'GetHistory(): Exception {e}')
        return jsonify({})

@app.route('/AddUser', methods=['POST']) # ChatRoomId
def AddUser():
    try:
        data = request.get_json()
        logging.log(logging.INFO, f'AddUser(): received request = {data}')
        userName = data['UserName']
        preferredLanguage = data['PreferredLanguage']
        retJson = {"Result":GBabelChatManager.AddUserInfo(userName, preferredLanguage)}
        resStr = json.dumps(retJson)
        logging.log(logging.INFO, f'AddUser(): Sending result <<<{resStr}>>>')
        return resStr
    except Exception as e:
        logging.log(logging.ERROR, f'AddUser(): Exception {e}')
        return jsonify({})

@app.route('/GetChatRooms', methods=['POST'])
def GetChatRooms():
    try:
        data = request.get_json()
        logging.log(logging.INFO, f'GetChatRooms(): received request = {data}')
        retJson = GBabelChatManager.GetChatRooms()
        resStr = json.dumps(retJson)
        # logging.log(logging.INFO, f'Sending query result <<<{resStr}>>>')
        return resStr
    except Exception as e:
        logging.log(logging.ERROR, f'GetChatRooms(): Exception {e}')
        return jsonify({})

@app.route('/<path:filename>', methods=['GET'])
def ServeResourceFile(filename):
    try:
        logging.log(logging.INFO, f"request: {filename}")
        if not os.path.isfile(f'./Site/{filename}'):
            abort(404)
        if filename.endswith(".js") or filename.endswith(".html") or filename.endswith(".js"):
            result = FileUtils.ReadText(f'./Site/{filename}')
            return result
        else:
            return send_from_directory("./Site", f'{filename}')
    except Exception as e:
        logging.log(logging.ERROR, f"Error: {e}")
        abort(500)


if __name__ == '__main__':
    # port
    port = GConfig.GetItemValue("Default", "port")
    if port == '' : port = 18888
    else: port = int(port)
    if len(sys.argv) >=2:
        logging.log(logging.INFO, f'Read port {sys.argv[1]}')
        port = int(sys.argv[1])
    # host
    host = '0.0.0.0'

    # run
    ssl_context = (basedir + '/server.crt', basedir + '/server.key')
    
    # release
    app.run(host=host, ssl_context=ssl_context, port=port, threaded=True)
    pass