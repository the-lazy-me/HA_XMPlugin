from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类

from plugins.HA_XMPlugin.tools.services import services
from plugins.HA_XMPlugin.tools.states import states

from pathlib import Path
import yaml

"""
在收到私聊或群聊消息"hello"时，回复"hello, <发送者id>!"或"hello, everyone!"
"""

# 读取根目录下data/plugins/HA_XMPlugin/config.yaml配置文件
config_path = Path(__file__).resolve().parent.parent.parent / "data" / "plugins" / "HA_XMPlugin" / "config.yaml"
with config_path.open("r") as f:
    config = yaml.safe_load(f)

PERMITTED_USER = config["permitted_user"]  # 读取配置文件中的permit_user字段
BASE_URL = config["base_url"]  # 读取配置文件中的base_url字段
TOKEN = config["token"]  # 读取配置文件中的token字段


# 注册插件
@register(name="HA_XMPlugin", description="一个接入Home Assistant米家集成的插件", version="0.1", author="Lazy")
class HelloPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        self.ap.logger.info("HA_XMPlugin 插件已加载，版本0.1，作者Lazy，一个HomeAssistant插件，用于实现IoT智能化")
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        user_id = ctx.event.sender_id
        if user_id in PERMITTED_USER:
            if msg == "开启插座":
                url = BASE_URL + "/api/services/switch/turn_on"
                entity_id = "switch.cuco_cn_833407447_v3_on_p_2_1"

                response = services(url, TOKEN, entity_id)

                # 输出调试信息
                self.ap.logger.debug(response.json())

                # 回复已开启插座
                ctx.add_return("reply", ["已开启插座"])

                # 阻止该事件默认行为（向接口获取回复）
                ctx.prevent_default()

            elif msg == "关闭插座":
                url = BASE_URL + "/api/services/switch/turn_off"
                entity_id = "switch.cuco_cn_833407447_v3_on_p_2_1"

                response = services(url, TOKEN, entity_id)

                # 输出调试信息
                self.ap.logger.debug(response.json())

                # 回复已关闭插座
                ctx.add_return("reply", ["已关闭插座"])

                # 阻止该事件默认行为（向接口获取回复）
                ctx.prevent_default()

            elif msg == "插座状态":
                url = BASE_URL + "/api/states/switch.cuco_cn_833407447_v3_on_p_2_1"

                response = states(url, TOKEN)

                if response["state"] == "on":
                    ctx.add_return("reply", ["插座状态：开启"])

                else:
                    ctx.add_return("reply", ["插座状态：关闭"])

                ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
