import random
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import AstrBotConfig

# 注册插件，传入作者、描述和版本
@register("random_reply_demo", "YourName", "特定用户概率随机回复插件", "1.0.0")
class RandomReplyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config  # 保存配置对象以便后续读取

    # 监听所有群消息事件
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        # 1. 获取消息所在的群 ID 和发送者 ID
        # AstrBotMessage 对象中存储了 group_id
        current_group_id = event.message_obj.group_id
        # 使用 get_sender_id() 获取发送者 ID
        sender_id = event.get_sender_id()

        # 2. 读取配置
        target_groups = self.config.get("target_groups", [])
        target_users = self.config.get("target_users", [])
        probability = self.config.get("reply_probability", 0.0)
        reply_list = self.config.get("reply_list", [])

        # 3. 校验逻辑
        # 如果当前群不在目标群列表中，直接返回
        if current_group_id not in target_groups:
            return
        
        # 如果发送者不在目标用户列表中，直接返回
        if sender_id not in target_users:
            return

        # 如果回复列表为空，防止报错，直接返回
        if not reply_list:
            return

        # 4. 概率计算与发送
        # random.random() 返回 [0.0, 1.0) 之间的浮点数
        if random.random() < probability:
            # 随机抽取一句
            selected_reply = random.choice(reply_list)
            
            # 发送纯文本消息
            yield event.plain_result(selected_reply)
            
            # 注意：此处不需要 event.stop_event()，除非你想阻止其他插件处理这条消息