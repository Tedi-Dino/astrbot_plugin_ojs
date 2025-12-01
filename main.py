import random
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import AstrBotConfig

@register("random_reply_demo", "YourName", "特定用户概率随机回复插件", "1.0.1")
class RandomReplyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config  # 根据文档，config 会被注入

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        # 1. 获取 ID 并强制转换为字符串，防止类型不匹配
        # group_id 位于 message_obj 中
        current_group_id = str(event.message_obj.group_id)
        sender_id = str(event.get_sender_id())

        # 2. 读取配置，并确保列表中的 ID 也是字符串
        # 即使 JSON 中写的是数字，这里也会处理成字符串进行比对
        raw_target_groups = self.config.get("target_groups", [])
        target_groups = [str(g) for g in raw_target_groups]

        raw_target_users = self.config.get("target_users", [])
        target_users = [str(u) for u in raw_target_users]

        probability = self.config.get("reply_probability", 0.0)
        reply_list = self.config.get("reply_list", [])

        # 3. 校验逻辑 (现在类型安全了)
        if current_group_id not in target_groups:
            return
        
        if sender_id not in target_users:
            return

        if not reply_list:
            return

        # 4. 概率计算与发送
        if random.random() < probability:
            selected_reply = random.choice(reply_list)
            yield event.plain_result(selected_reply)