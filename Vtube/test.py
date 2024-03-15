import asyncio
import websockets
import json
from asyncio import sleep
import os
import json

my_requestID = "VTubeControlPlugin"
my_pluginName = "VTube模型控制插件"
my_apiVersion = "1.0"
ws_uri = "ws://localhost:8001"  # VTube Studio WebSocket服务器地址
pluginDeveloperIstars = "TArs"


async def get_token():
    global my_requestID, my_pluginName, my_apiVersion, ws_uri, pluginDeveloperIstars
    uri = "ws://localhost:8001"

    if os.path.exists("token.json"):
        with open("token.json", "r") as file:
            authtoken = file.read()

    else:

        async with websockets.connect(uri) as websocket:

            request_token_payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": my_apiVersion,
                "requestID": my_requestID,
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": my_pluginName,
                    "pluginDeveloper": pluginDeveloperIstars,
                },
            }

            await websocket.send(json.dumps(request_token_payload))

            json_data = await websocket.recv()
            pack = json.loads(json_data)
            authtoken = pack["data"]["authenticationToken"]

        with open("token.json", "w") as file:
            file.write(authtoken)

    return authtoken

async def testget_token():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:

            request_token_payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": my_apiVersion,
                "requestID": my_requestID,
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": my_pluginName,
                    "pluginDeveloper": pluginDeveloperIstars,
                },
            }

            await websocket.send(json.dumps(request_token_payload))

            json_data = await websocket.recv()
            pack = json.loads(json_data)
            authtoken = pack["data"]["authenticationToken"]
            print(authtoken)
    

async def main():
    #await testget_token()
    authtoken = await get_token()
    print(authtoken)

asyncio.get_event_loop().run_until_complete(main())
