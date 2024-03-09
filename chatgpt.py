import asyncio
import websockets
import json
from asyncio import sleep

async def connect_to_vtubestudio():
    uri = "ws://localhost:8001"  # VTube Studio WebSocket服务器地址

    async with websockets.connect(uri) as websocket:
        # 构建身份验证请求
        authentication_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "My Cool Plugin",
                "pluginDeveloper": "My Name",
                "authenticationToken": "329dba923a58f64f34c4c08321c16427f23fdd80b45ed195aa73536200466576",
            },
        }

        # 发送身份验证请求
        await websocket.send(json.dumps(authentication_request))

        # 接收身份验证响应
        response = await websocket.recv()
        print(f"Received authentication response: {response}")

        # 构建注入参数请求
        for headnum in range(-30, 30):
            await sleep(0.03)
            
            inject_parameter_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "mode": "set",
                    "parameterValues": [
                        {"id": "FaceAngleZ", "value": headnum},
                    ],
                },
            }

            # 发送注入参数请求
            await websocket.send(json.dumps(inject_parameter_request))

            # 接收注入参数响应
            response = await websocket.recv()
            formatted_response = json.dumps(json.loads(response), indent=2)
            print(f"Received inject parameter response:\n{formatted_response}")

# 运行连接函数
asyncio.get_event_loop().run_until_complete(connect_to_vtubestudio())
