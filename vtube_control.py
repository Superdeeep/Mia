import os
import json
import websockets
import asyncio

class VTubeControl:
    def __init__(
        self,
        ws_address,
        Vtube_id,
        Vtube_plugin_name,
        Vtube_plugin_developer,
        api_version="1.0",
        token_path="token.txt",
    ):
        self.ws_address = ws_address
        self.Vtube_id = Vtube_id
        self.Vtube_plugin_name = Vtube_plugin_name
        self.Vtube_plugin_developer = Vtube_plugin_developer
        self.api_version = api_version
        self.token_path = token_path

    async def get_token(self):
        """获取Vtube的token的值并保存"""

        uri = "ws://localhost:8001"

        # 判断是否存在已经获取的token
        if os.path.exists(self.token_path):
            with open(self.token_path, "r") as file:
                authtoken = file.read()
                print(f"已存在token,值为:{authtoken}")

        else:
            print("不存在token,尝试自动获取")
            # 发送验证控制载荷

            async with websockets.connect(uri) as websocket:

                request_token_payload = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": self.api_version,
                    "requestID": self.Vtube_id,
                    "messageType": "AuthenticationTokenRequest",
                    "data": {
                        "pluginName": self.Vtube_plugin_name,
                        "pluginDeveloper": self.Vtube_plugin_developer,
                    },
                }

                await websocket.send(json.dumps(request_token_payload))

                # 处理返回的数据
                json_data = await websocket.recv()
                pack = json.loads(json_data)

                # 如果拒绝插件访问
                if "errorID" in pack["data"]:
                    errorid = pack["data"]["errorID"]  # 解析data中的errorid
                    authtoken = None
                    print("获取token失败,请确保在vtube中允许插件访问")
                    print(f"错误ID:{errorid}")
                # 如果允许插件访问
                elif "authenticationToken" in pack["data"]:
                    authtoken = pack["data"]["authenticationToken"]
                    print(f"已获取token:{authtoken}\n并保存在了本地")

                    with open(self.token_path, "w") as file:
                        file.write(authtoken)
        # 返回获取到的token
        return authtoken

    async def control_talking(self, token): 
        """控制vtube模型的嘴巴说话的快捷键"""

        # 验证=========================
        async with websockets.connect(self.ws_address) as websocket:
            authentication_payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": self.api_version,
                "requestID": self.Vtube_id,
                "messageType": "AuthenticationRequest",
                "data": {
                    "pluginName": self.Vtube_plugin_name,
                    "pluginDeveloper": self.Vtube_plugin_developer,
                    "authenticationToken": token,
                },
            }
            await websocket.send(json.dumps(authentication_payload))
            # ============================

            # 处理接收的数据=================
            response_json_data = await websocket.recv()
            pack = json.loads(response_json_data)
            auth_status = pack["data"]["authenticated"]
            # ============================

            # 判断=========================
            if auth_status == True:  # 这里的判断可能是有问题的，应该为try catch

                # 发送快捷键数据
                hotkey_payload = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": self.Vtube_id,
                    "messageType": "HotkeyTriggerRequest",
                    "data": {
                        "hotkeyID": "hotkey_talk",
                    },
                }
                # 播放音频并报告状态
                #await tts_module.play_and_report_status(answer)

                # 持续发送控制命令，直到 TTS 完成播放
                #while tts_module.is_playing():
                await websocket.send(json.dumps(hotkey_payload))

            else:
                print(f"Received response:\n{response_json_data}")
