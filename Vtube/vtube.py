import asyncio
import websockets
import json
from asyncio import sleep
import os
import random
import numpy as np
import requests
import json

# import speech


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


async def test_control_model(authtoken, test_payload_data):
    global my_requestID, my_pluginName, my_apiVersion, ws_uri, pluginDeveloperIstars

    async with websockets.connect(ws_uri) as websocket:
        # 构建 API 请求
        authentication_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": my_apiVersion,
            "requestID": my_requestID,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": my_pluginName,
                "pluginDeveloper": pluginDeveloperIstars,
                "authenticationToken": authtoken,
            },
        }

        await websocket.send(json.dumps(authentication_payload))

        response_json_data = await websocket.recv()

        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]

        if auth_status == True:
            print(f"successfully authenticated with VTube Studio")
        else:
            print(f"Received response:\n{response_json_data}")

        test_payload = test_payload_data

        await websocket.send(json.dumps(test_payload))

        response = await websocket.recv()
        formatted_response = json.dumps(json.loads(response), indent=2)

        print(f"Received response:\n{formatted_response}")

async def control_talking_words(authtoken,num):
    async with websockets.connect(ws_uri) as websocket:
        # 构建 auth API 请求
        authentication_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": my_apiVersion,
            "requestID": my_requestID,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": my_pluginName,
                "pluginDeveloper": pluginDeveloperIstars,
                "authenticationToken": authtoken,
            },
        }

        await websocket.send(json.dumps(authentication_payload))

        response_json_data = await websocket.recv()

        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]

        if auth_status == True:
            pass
        else:
            print(f"Received response:\n{response_json_data}")

        control_talking_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": my_requestID,
            "messageType": "HotkeyTriggerRequest",
            "data": {
                "hotkeyID": "hotkey_talk",
                # "itemInstanceID": "Optional_ItemInstanceIdOfLive2DItemToTriggerThisHotkeyFor"
            },
        }
        for i in range(num):
            await websocket.send(json.dumps(control_talking_payload))


async def control_talking(authtoken):
    async with websockets.connect(ws_uri) as websocket:
        # 构建 auth API 请求
        authentication_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": my_apiVersion,
            "requestID": my_requestID,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": my_pluginName,
                "pluginDeveloper": pluginDeveloperIstars,
                "authenticationToken": authtoken,
            },
        }

        await websocket.send(json.dumps(authentication_payload))

        response_json_data = await websocket.recv()

        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]

        if auth_status == True:
            pass
        else:
            print(f"Received response:\n{response_json_data}")

        control_talking_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": my_requestID,
            "messageType": "HotkeyTriggerRequest",
            "data": {
                "hotkeyID": "hotkey_talk",
                # "itemInstanceID": "Optional_ItemInstanceIdOfLive2DItemToTriggerThisHotkeyFor"
            },
        }
        await websocket.send(json.dumps(control_talking_payload))


async def control_talkingbak(authtoken):
    global my_requestID, my_pluginName, my_apiVersion, ws_uri, pluginDeveloperIstars
    openn = 0
    async with websockets.connect(ws_uri) as websocket:
        # 构建 auth API 请求
        authentication_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": my_apiVersion,
            "requestID": my_requestID,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": my_pluginName,
                "pluginDeveloper": pluginDeveloperIstars,
                "authenticationToken": authtoken,
            },
        }

        await websocket.send(json.dumps(authentication_payload))

        response_json_data = await websocket.recv()

        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]

        if auth_status == True:
            pass
        else:
            print(f"Received response:\n{response_json_data}")

        for num in range(1, 10):
            await sleep(1)

            open = 1

            for i in np.arange(0.2, open, 0.2):

                control_talking_payload = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": my_apiVersion,
                    "requestID": my_requestID,
                    "messageType": "InjectParameterDataRequest",
                    "data": {
                        "mode": "set",
                        "parameterValues": [
                            {"id": "MouthOpen", "value": openn},
                        ],
                    },
                }
                openn = openn + 0.2
                await sleep(0.1)

                await websocket.send(json.dumps(control_talking_payload))

            for i in np.arange(open, 0.2, -0.2):

                control_talking_payload = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": my_apiVersion,
                    "requestID": my_requestID,
                    "messageType": "InjectParameterDataRequest",
                    "data": {
                        "mode": "set",
                        "parameterValues": [
                            {"id": "MouthOpen", "value": openn},
                        ],
                    },
                }

                openn = openn - 0.2
                await sleep(0.1)

                await websocket.send(json.dumps(control_talking_payload))


async def main():
    authtoken = await get_token()
    print(authtoken)

    test_payload_data = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": my_requestID,
        "messageType": "ModelLoadRequest",
        "data": {
            "modelID": "9130fba0d5ba4d9382c6bb9bdd074cb1"
            # "modelID": "16cb35b798894643a7f37a902ad640f9"
        },
    }

    # await test_control_model(authtoken, test_payload_data)

    await control_talking(authtoken)

    # speech.say("This is a very simple demo test.")

    # myol=await test_ollama()

    # speech.say(myol)


# Hiyori_A "9130fba0d5ba4d9382c6bb9bdd074cb1"
asyncio.get_event_loop().run_until_complete(main())
