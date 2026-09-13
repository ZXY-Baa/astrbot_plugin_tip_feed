from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star
from astrbot.api import logger


class TipFeedPlugin(Star):
    """识别自定义关键词并发送收款码"""

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        """监听所有消息，检测是否包含自定义关键词"""
        message_str = event.message_str

        # 跳过空消息
        if not message_str:
            return

        # 读取自定义触发关键词，默认为“投喂”
        keywords_str = self.config.get("trigger_keywords", "投喂")
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
        if not keywords:
            keywords = ["投喂"]

        # 检测是否包含任一关键词
        if not any(kw in message_str for kw in keywords):
            return

        logger.info(f"检测到投喂消息，来自: {event.get_sender_name()}")

        # 从配置中读取收款码图片路径
        image_path = self.config.get("qrcode_path", "")

        if not image_path:
            yield event.plain_result(
                "感谢投喂！但收款码还没配置好喵~ 请提醒管理员在插件配置中上传收款码图片。"
            )
            return

        # 发送收款码图片
        yield event.image_result(image_path)

    async def terminate(self):
        """插件卸载时调用"""
        pass
