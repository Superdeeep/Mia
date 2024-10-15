import asyncio
from vtube_control import VTubeControl

async def main():
    vtube_control = VTubeControl(
        ws_address="ws://localhost:8001",
        Vtube_id="example_id",
        Vtube_plugin_name="example_plugin",
        Vtube_plugin_developer="example_developer"
    )

    # 获取token
    token = await vtube_control.get_token()
    await vtube_control.control_talking(token)


if __name__ == "__main__":
    asyncio.run(main())