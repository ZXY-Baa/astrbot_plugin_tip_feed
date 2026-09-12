from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star
from astrbot.api import logger


class TipFeedPlugin(Star):
    """识别消息中的“投喂”并发送收款码"""

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        """监听所有消息，检测是否包含“投喂”"""
        message_str = event.message_str

        # 跳过空消息
        if not message_str:
            return

        # 检测关键词“投喂”
        if "投喂" not in message_str:
            return

        logger.info(f"检测到投喂消息，来自: {event.get_sender_name()}")

        # 从配置中读取收款码图片路径
        image_path = self.config.get("qrcode_path", "")

        if not image_path:
            yield event.plain_result("感谢投喂！但收款码还没配置好喵~ 请提醒管理员在插件配置中上传收款码图片。")
            return

        # 发送收款码图片
        yield event.image_result(image_path)

    async def terminate(self):
        """插件卸载时调用"""
        pass
